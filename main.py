import pygame
from pygame.locals import *

import math
import os
import random
import sys
import time

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

def get_config_dir():
    confdir = os.path.join(os.path.expanduser("~"), '.config')
    game_confdir = os.path.join(confdir, "best_game")
    try:
        os.makedirs(game_confdir)
    except OSError as e:
        pass
    return game_confdir

class Score:
    # Highest score file
    def __init__(self):
        self.HIGHEST_SCORE_PATH = os.path.join(get_config_dir(), 'highest_score')
        if not os.path.exists(self.HIGHEST_SCORE_PATH):
            with open(self.HIGHEST_SCORE_PATH, 'w') as highest_score_file:
                highest_score_file.write('0')
        # Load highest score
        self.high_score = self.highest_score = self.load_highest_score()
        self.points = 0

    def load_highest_score(self):
        with open(self.HIGHEST_SCORE_PATH, 'r') as highest_score_file:
            highest_score = int(highest_score_file.readlines()[0])
        return highest_score

    def save_highest_score(self):
        with open(self.HIGHEST_SCORE_PATH, 'w') as highest_score_file:
            highest_score_file.write(str(self.high_score))

def draw_text(text, font, color, screen, x, y):  # Функция отрисовки текста
    texobj = font.render(text, 1, color)
    textrect = texobj.get_rect()
    textrect.center = (x, y)
    screen.blit(texobj, textrect)

def draw_repeating_background(background_img):
    new_image = pygame.transform.scale(background_img, (res_width, res_height))
    background_rect = new_image.get_rect(bottomright=(res_width, res_height))
    screen.blit(background_img, background_rect)

def main_menu(screen):  # Функция окна "Главное меню"
    pygame.mixer_music.load('main menu melody.mp3')
    pygame.mixer_music.play()
    while True:
        screen.fill(black)  # Заполнение экрана черным фоном
        draw_text('main menu', font, white, screen, res_width / 2, 20)  # Отрисовка белого текста

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
    global score
    time_score, time_pause = 0, 0
    paused = False
    score = Score()
    start_time = time.time()
    mx, my = pygame.mouse.get_pos()
    square = Block()
    background_surf = pygame.image.load('background.png')
    draw_repeating_background(background_surf)
    screen.blit(square.img, square.rect)
    pygame.display.update()
    shuffle()
    while True:  # Пока запущено
        pause_mx, pause_my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == KEYDOWN:  # Условие на нажатие любой кнопки
                if event.key == K_s:
                    pygame.mixer_music.stop()# Условие на нажатие кнопки S
                if (event.key == pygame.K_SPACE) and (mx-20 <= pause_mx <= mx+20) and (my-20 <= pause_my <= my+20):
                    paused = False
                    start_time = start_time + time_pause
                if event.key == K_ESCAPE:  # Условие на нажатие кнопки Escapezz
                    main_menu(screen)  # Возвращение в главное меню
        pygame.time.Clock().tick(60)
        pygame.display.update()
        if not paused:
            time_pause = 0
            time_score = time.time() - start_time
            mx, my = pygame.mouse.get_pos()
            pygame.mouse.set_visible(False)
            draw_repeating_background(background_surf)
            draw_text('{}  points'.format(score.points), font, white, screen, 70, 20)
            draw_text('Record: {}'.format(score.high_score), font, white, screen, 70, 50)
            draw_text('Time: {}'.format(round(time_score, 2)), font, white, screen, 100, 80)
            screen.blit(square.img, (mx - 15, my - 15))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = True
                        if paused:
                            transp_surf = pygame.Surface((res_width, res_height))
                            transp_surf.set_alpha(150)
                            screen.blit(transp_surf, transp_surf.get_rect())
                            pygame.mouse.set_visible(True)
                            draw_text('Нажмите ESC чтобы выйти', font, white, screen, res_width/2, res_height/2)
                            draw_text('Нажмите SPACE чтобы продолжить', font, white, screen, res_width/2,
                                      (res_height/2+40))
        else: time_pause = time.time() - start_time - time_score



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
