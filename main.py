import pygame
from pygame.locals import *

# Инициализация pygame
pygame.init()
main_Clock = pygame.time.Clock()  # Добавляем таймер, своего рода FPS - количество кадров в секунду


screen = pygame.display.set_mode((1280, 920), 0, 32)  # Создаем окно с размерами 1920x1080

pygame.display.set_caption("Fral's game")  # Задаем название окна
font = pygame.font.SysFont(None, 20)  # Задаем размер шрифта


def draw_text(text, font, color, surface, x, y):  # Функция отрисовки текста
    texobj = font.render(text, 1, color)
    textrect = texobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(texobj, textrect)


def main_menu():  # Функция окна "Главное меню"
    while True:
        screen.fill((0, 0, 0))  # Заполнение экрана черным фоном
        draw_text('main menu', font, (255, 255, 255), screen, 20, 20)  # Отрисовка белого текста

        mx, my = pygame.mouse.get_pos()  # переменные для хранения позиции мыши

        play_button = pygame.Rect(50, 100, 200, 50)  # Параметры прямоугольника для кнопки
        settings_button = pygame.Rect(50, 200, 200, 50) # Параметры прямоугольника для кнопки
        exit_button = pygame.Rect(50, 300, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), play_button)  # Отрисовка кнопки
        pygame.draw.rect(screen, (255, 0, 0), settings_button)  # Отрисовка кнопки
        pygame.draw.rect(screen, (255, 0, 0), exit_button) # Отрисовка кнопки

        click = False  # Флаг нажатия левой кнопки мыши
        for event in pygame.event.get(): # Считывание всех действий мыши и клавиатуры
            if event.type == QUIT:  # Условие на закрытие программы при помощи креста
                pygame.quit()
            if event.type == KEYDOWN:  # Условие на нажатие любой кнопки
                if event.key == K_ESCAPE:  # Условие на нажатие кнопки Escape
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:  # Условие на нажатие левой кнопки мыши
                if event.button == 1:  # Если нажата
                    click = True  # инвертируем флаг

        if play_button.collidepoint(mx, my) and click:  # Условие на положение мыши над кнопкой и ее нажатие
            game()  # Перейти в окно "Играть"
        if settings_button.collidepoint(mx, my) and click: # Условие на положение мыши над кнопкой и ее нажатие
            options()  # Перейти в окно "Настройки"
        if exit_button.collidepoint(mx, my) and click:  # Условие на положение мыши над кнопкой и ее нажатие
            pygame.quit()  # Закрыть окно

        pygame.display.update()  # Обновление экрана


def game():  # Функция окна "Играть"
    while True:  # Пока запущено
        screen.fill((0, 0, 0))  # Заполнение экрана черным фоном
        draw_text('game', font, (255, 255, 255), screen, 20, 20)  # Отрисовка белого текста

        for event in pygame.event.get():  # Считывание всех действий мыши и клавиатуры
            if event.type == KEYDOWN:  # Условие на нажатие любой кнопки
                if event.key == K_ESCAPE:  # Условие на нажатие кнопки Escape
                    main_menu()  # Возвращение в главное меню

        pygame.display.update()  # Обновление экрана


def options():  # Функция окна "Настройки"
    while True:
        screen.fill((0, 0, 0))  # Пока запущено
        draw_text('options', font, (255, 255, 255), screen, 20, 20)  # Отрисовка белого текста

        for event in pygame.event.get():  # Считывание всех действий мыши и клавиатуры
            if event.type == KEYDOWN:  # Условие на нажатие любой кнопки
                if event.key == K_ESCAPE:  # Условие на нажатие кнопки Escape
                    main_menu()  # Возвращение в главное меню

        pygame.display.update()  # Обновление экрана


main_menu()  # Вызов функции главного меню
main_Clock.tick(60)  # Количество кадров в секунду
