import pygame
from pygame.locals import *

import math
import os
import random
import sys

width = [1920, 1600, 1280]
heigh = [1080, 900, 720]
res_width, res_height = width[2], heigh[2]
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 70, 225)
green = (0, 255, 0)
red = (255, 0, 0)
speed = 1

# Инициализация pygame
pygame.init()
main_Clock = pygame.time.Clock()  # Добавляем таймер, своего рода FPS - количество кадров в секунду
screen = pygame.display.set_mode((res_width, res_height))  # Создаем окно с размерами 1920x1080
flags = screen.get_flags()

pygame.display.set_caption("Dodge this")  # Задаем название окна
font = pygame.font.SysFont(None, 40)  # Задаем размер шрифта
player_color = (255, 0, 255)
bonus_color = (255, 0, 0)

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super(Block, self).__init__()
        self.img = pygame.Surface((30, 30))
        self.img.fill(player_color)
        self.rect = self.img.get_rect()
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

    def set_pos(self, x, y):
        'Positions the block center in x and y location'
        self.rect.x = x - self.centerx
        self.rect.y = y - self.centery

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite


class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bonus, self).__init__()
        self.image = pygame.Surface((15, 15))
        # self.image.fill(bonus_color)
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.centerx
        self.rect.y = y - self.rect.centery


class Bullet(pygame.sprite.Sprite):

    def __init__(self, xpos, ypos, hspeed, vspeed):
        super(Bullet, self).__init__()
        self.image = pygame.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.hspeed = hspeed
        self.vspeed = vspeed

        self.set_direction()

    def update(self):
        self.rect.x += self.hspeed
        self.rect.y += self.vspeed
        if self.collide():
            self.kill()

    def collide(self):
        if self.rect.x < 0 - self.rect.height or self.rect.x > res_width:
            return True
        elif self.rect.y < 0 - self.rect.height or self.rect.y > res_height:
            return True

    def set_direction(self):
        if self.hspeed > 0:
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.hspeed < 0:
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.vspeed > 0:
            self.image = pygame.transform.rotate(self.image, 180)


def draw_text(text, font, color, surface, x, y):  # Функция отрисовки текста
    texobj = font.render(text, 1, color)
    textrect = texobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(texobj, textrect)

def draw_repeating_background(background_img):
    new_image = pygame.transform.scale(background_img, (res_width, res_height))
    background_rect = new_image.get_rect(bottomright=(res_width, res_height))
    screen.blit(background_img, background_rect)

def main_menu(screen):  # Функция окна "Главное меню"
    pygame.mixer_music.load('main menu melody.mp3')
    pygame.mixer_music.play()
    while True:
        screen.fill(black)  # Заполнение экрана черным фоном
        draw_text('main menu', font, white, screen, 20, 20)  # Отрисовка белого текста

        mx, my = pygame.mouse.get_pos()  # переменные для хранения позиции мыши

        play_button = pygame.Rect(50, 100, 200, 50)  # Параметры прямоугольника для кнопки
        settings_button = pygame.Rect(50, 200, 200, 50)  # Параметры прямоугольника для кнопки
        exit_button = pygame.Rect(50, 300, 200, 50)
        pygame.draw.rect(screen, red, play_button)  # Отрисовка кнопки
        draw_text('Game', font, white, screen, 50, 100)  # Отрисовка текста кнопки
        pygame.draw.rect(screen, red, settings_button)  # Отрисовка кнопки
        draw_text('Options', font, white, screen, 50, 200)  # Отрисовка текста кнопки
        pygame.draw.rect(screen, red, exit_button)  # Отрисовка кнопки
        draw_text('Exit', font, white, screen, 50, 300)  # Отрисовка текста кнопки

        click = False  # Флаг нажатия левой кнопки мыши
        for event in pygame.event.get():  # Считывание всех действий мыши и клавиатуры
            if event.type == QUIT:  # Условие на закрытие программы при помощи креста
                exit()
            if event.type == KEYDOWN:  # Условие на нажатие любой кнопки
                if event.key == K_ESCAPE:  # Условие на нажатие кнопки Escape
                    exit()
            if event.type == MOUSEBUTTONDOWN:  # Условие на нажатие левой кнопки мыши
                if event.button == 1:  # Если нажата
                    click = True  # инвертируем флаг

        if play_button.collidepoint(mx, my) and click:  # Условие на положение мыши над кнопкой и ее нажатие
            game()  # Перейти в окно "Играть"
            pygame.mixer_music.stop()
        if settings_button.collidepoint(mx, my) and click:  # Условие на положение мыши над кнопкой и ее нажатие
            options(screen)  # Перейти в окно "Настройки"
        if exit_button.collidepoint(mx, my) and click:  # Условие на положение мыши над кнопкой и ее нажатие
            exit()

        pygame.display.update()  # Обновление экрана


def game():  # Функция окна "Играть"
    paused = False
    click = False
    mx, my = pygame.mouse.get_pos()
    screen.fill(black)
    square = Block()
    draw_text('game', font, (255, 255, 255), screen, 20, 20)
    background_surf = pygame.image.load('background.png')

    background_rect = background_surf.get_rect(bottomright=(res_height, res_width))
    screen.blit(background_surf, background_rect)
    screen.blit(square.img, square.rect)

    pygame.display.update()
    shuffle()
    while True:  # Пока запущено
        for event in pygame.event.get():
            if event.type == KEYDOWN:  # Условие на нажатие любой кнопки
                if event.key == K_ESCAPE:
                    pygame.mixer_music.stop()# Условие на нажатие кнопки Escape
                    main_menu(screen)  # Возвращение в главное меню
            if event.type == MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] <= 10:
                    pygame.mouse.set_pos(res_width - 10, mouse_pos[1])
                elif mouse_pos[0] >= res_width - 10:
                    pygame.mouse.set_pos(0 + 10, mouse_pos[1])
                elif mouse_pos[1] <= 10:
                    pygame.mouse.set_pos(mouse_pos[0], res_height - 10)
                elif mouse_pos[1] >= res_height - 10:
                    pygame.mouse.set_pos(mouse_pos[0], 0 + 10)
                square.set_pos(*mouse_pos)
        #     # if event.type == pygame.MOUSEBUTTONDOWN:
        #     #     random_x = random.randint(0, x_player)
        #     #     random_y = random.randint(0, y_player)
        #     #     square.set_pos(random_x, random_y)
        #     #     pygame.mouse.set_pos([random_x, random_y])
        pygame.display.update()
        if not paused:
            draw_repeating_background(background_surf)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == MOUSEBUTTONDOWN:  # Условие на нажатие левой кнопки мыши
                        if event.button == 1:  # Если нажата
                            click = True  # инвертируем флаг
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                        if paused:
                            transp_surf = pygame.Surface((res_width, res_height))
                            transp_surf.set_alpha(150)
                            screen.blit(transp_surf, transp_surf.get_rect())
                            pygame.mouse.set_visible(True)
                            exit_butt = pygame.Rect(50, 200, 200, 50)  # Параметры прямоугольника для кнопки
                            pygame.draw.rect(screen, red, exit_butt)  # Отрисовка кнопки
                            draw_text('EXIT', font, white, screen, 50, 200)  # Отрисовка текста кнопки
                            if exit_butt.collidepoint(mx, my) and click:
                                main_menu(screen)




def options(screen):  # Функция окна "Настройки"
    global res_width, res_height, flags
    screen.fill(black)  # Пока запущено
    while True:
        mx, my = pygame.mouse.get_pos()  # переменные для хранения позиции мыши
        click = False
        draw_text('options', font, (255, 255, 255), screen, 20, 20)  # Отрисовка белого текста
        resolution = pygame.Rect(100, 100, 200, 50)  # Параметры прямоугольника для кнопки
        full_screen = pygame.Rect(100, 200, 200, 50)  # Параметры прямоугольника для кнопки
        full_hd = pygame.Rect(350, 100, 200, 50)  # Параметры прямоугольника для кнопки
        wxga = pygame.Rect(600, 100, 200, 50)  # Параметры прямоугольника для кнопки
        hd = pygame.Rect(850, 100, 200, 50)  # Параметры прямоугольника для кнопки
        back = pygame.Rect(100, 300, 200, 50)  # Параметры прямоугольника для кнопки

        pygame.draw.rect(screen, red, resolution)  # Отрисовка кнопки
        draw_text('Resolution', font, white, screen, 100, 100)  # Отрисовка текста кнопки
        pygame.draw.rect(screen, red, full_screen)  # Отрисовка кнопки
        draw_text('Full screen', font, white, screen, 100, 200)  # Отрисовка текста кнопки
        pygame.draw.rect(screen, red, back)
        draw_text('Back', font, white, screen, 100, 300)

        for event in pygame.event.get():  # Считывание всех действий мыши и клавиатуры
            if event.type == KEYDOWN:  # Условие на нажатие любой кнопки
                if event.key == K_ESCAPE:  # Условие на нажатие кнопки Escape
                    main_menu(screen)  # Возвращение в главное меню
            if event.type == MOUSEBUTTONDOWN:  # Условие на нажатие левой кнопки мыши
                if event.button == 1:  # Если нажата
                    click = True  # инвертируем флаг

        if full_screen.collidepoint(mx, my) and click:
            if flags & FULLSCREEN == False:
                flags |= FULLSCREEN
                pygame.display.set_mode((width[0], heigh[0]), flags)
                res_width, res_height = width[0], heigh[0]
            else:
                flags ^= FULLSCREEN
                pygame.display.set_mode((res_width, res_height), flags)
        if resolution.collidepoint(mx, my) and click:
            screen.fill(black)  # Пока запущено
            pygame.draw.rect(screen, red, full_hd)  # Отрисовка кнопки
            draw_text('1920x1080', font, white, screen, 350, 100)  # Отрисовка текста кнопки
            pygame.draw.rect(screen, red, wxga)  # Отрисовка кнопки
            draw_text('1600x900', font, white, screen, 600, 100)  # Отрисовка текста кнопки
            pygame.draw.rect(screen, red, hd)  # Отрисовка кнопки
            draw_text('1280x720', font, white, screen, 850, 100)  # Отрисовка текста кнопки
            pygame.display.update()
        if back.collidepoint(mx, my) and click:
            main_menu(screen)
        if full_hd.collidepoint(mx, my) and click:
            screen = pygame.display.set_mode((width[0], heigh[0]))
            res_height = heigh[0]
            res_width = width[0]
        if wxga.collidepoint(mx, my) and click:
            screen = pygame.display.set_mode((width[1], heigh[1]))
            res_height = heigh[1]
            res_width = width[1]
        if hd.collidepoint(mx, my) and click:
            screen = pygame.display.set_mode((width[2], heigh[2]))
            res_height = heigh[2]
            res_width = width[2]
        pygame.display.update()  # Обновление экрана


songs = ['song1.mp3', 'song2.mp3', 'song3.mp3']
song_end = pygame.USEREVENT + 1
current_song = None
pygame.mixer_music.set_volume(0.05)


def shuffle():
    global current_song, song_end
    next_song = random.choice(songs)
    while next_song == current_song:
        next_song = random.choice(songs)
    current_song = next_song
    pygame.mixer_music.load(next_song)
    pygame.mixer_music.play()


main_menu(screen)  # Вызов функции главного меню
main_Clock.tick(60)  # Количество кадров в секунду
