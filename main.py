import pygame
from pygame.locals import *

heigh = [1920, 1600, 1280]
width = [1080, 900, 720]
res_heigh, res_width = heigh[2], width[2]
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 70, 225)
green = (0, 255, 0)
red = (255, 0, 0)
right = "to the right"
left = "to the left"
up = "to the up"
down = "to the down"
stop = "stop"
speed = 1

# Инициализация pygame
pygame.init()
main_Clock = pygame.time.Clock()  # Добавляем таймер, своего рода FPS - количество кадров в секунду
screen = pygame.display.set_mode((res_heigh, res_width))  # Создаем окно с размерами 1920x1080
flags = screen.get_flags()

pygame.display.set_caption("Fral's game")  # Задаем название окна
font = pygame.font.SysFont(None, 40)  # Задаем размер шрифта

# координаты и радиус круга (человечка)
x_player = 100
y_player = 200
r_player = 25
motion = stop  # движение игрока


def draw_text(text, font, color, surface, x, y):  # Функция отрисовки текста
    texobj = font.render(text, 1, color)
    textrect = texobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(texobj, textrect)


def main_menu(screen):  # Функция окна "Главное меню"
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
            game(x_player, y_player, motion)  # Перейти в окно "Играть"
        if settings_button.collidepoint(mx, my) and click:  # Условие на положение мыши над кнопкой и ее нажатие
            options(screen)  # Перейти в окно "Настройки"
        if exit_button.collidepoint(mx, my) and click:  # Условие на положение мыши над кнопкой и ее нажатие
            exit()

        pygame.display.update()  # Обновление экрана


def game(x_player, y_player, motion):  # Функция окна "Играть"
    global res_width, res_heigh
    while True:  # Пока запущено
        screen.fill(black)  # Заполнение экрана черным фоном
        draw_text('game', font, (255, 255, 255), screen, 20, 20)  # Отрисовка белого текста
        pygame.draw.circle(screen, blue, (x_player, y_player), r_player)

        for event in pygame.event.get():  # Считывание всех действий мыши и клавиатуры
            if event.type == KEYDOWN:  # Условие на нажатие любой кнопки
                if event.key == K_ESCAPE:  # Условие на нажатие кнопки Escape
                    main_menu(screen)  # Возвращение в главное меню
                elif event.key == pygame.K_LEFT:
                    motion = left
                elif event.key == pygame.K_RIGHT:
                    motion = right
                elif event.key == pygame.K_UP:
                    motion = up
                elif event.key == pygame.K_DOWN:
                    motion = down
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    motion = stop

        if motion == left:
            if (x_player - r_player) > 0:
                x_player -= speed
            else:
                motion = stop
        elif motion == right:
            if (x_player + r_player) < res_heigh:
                x_player += speed
            else:
                motion = stop
        elif motion == up:
            if (y_player - r_player) > 0:
                y_player -= speed
            else:
                motion = stop
        elif motion == down:
            if (y_player + r_player) < res_width:
                y_player += speed
            else:
                motion = stop
        pygame.display.update()  # Обновление экрана


def options(screen):  # Функция окна "Настройки"
    global res_width, res_heigh, flags
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

        pygame.draw.rect(screen, red, resolution)  # Отрисовка кнопки
        draw_text('Resolution', font, white, screen, 100, 100)  # Отрисовка текста кнопки
        pygame.draw.rect(screen, red, full_screen)  # Отрисовка кнопки
        draw_text('Full screen', font, white, screen, 100, 200)  # Отрисовка текста кнопки
        count = 0 # пока что счетчик для проверки вкл или вылк full screen

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
                pygame.display.set_mode((heigh[0], width[0]), flags)
                res_heigh, res_width = heigh[0], width[0]
            else:
                flags ^= FULLSCREEN
                pygame.display.set_mode((res_heigh, res_width), flags)
        if resolution.collidepoint(mx, my) and click:
            screen.fill(black)  # Пока запущено
            pygame.draw.rect(screen, red, full_hd)  # Отрисовка кнопки
            draw_text('1920x1080', font, white, screen, 350, 100)  # Отрисовка текста кнопки
            pygame.draw.rect(screen, red, wxga)  # Отрисовка кнопки
            draw_text('1600x900', font, white, screen, 600, 100)  # Отрисовка текста кнопки
            pygame.draw.rect(screen, red, hd)  # Отрисовка кнопки
            draw_text('1280x720', font, white, screen, 850, 100)  # Отрисовка текста кнопки
            pygame.display.update()
        if full_hd.collidepoint(mx, my) and click:
            screen = pygame.display.set_mode((heigh[0], width[0]))
            res_heigh = heigh[0]
            res_width = width[0]
        if wxga.collidepoint(mx, my) and click:
            screen = pygame.display.set_mode((heigh[1], width[1]))
            res_heigh = heigh[1]
            res_width = width[1]
        if hd.collidepoint(mx, my) and click:
            screen = pygame.display.set_mode((heigh[2], width[2]))
            res_heigh = heigh[2]
            res_width = width[2]
        pygame.display.update()  # Обновление экрана


main_menu(screen)  # Вызов функции главного меню
main_Clock.tick(60)  # Количество кадров в секунду
