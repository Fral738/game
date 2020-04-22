import pygame
from pygame.locals import *
# Инициализация pygame
pygame.init()

# Создаем окно с размерами 1920x1080
screen = pygame.display.set_mode((1280, 920), 0, 32)


pygame.display.set_caption("Fral's game")  # Задаем название окна
font = pygame.font.SysFont(None, 20)  # Задаем размер шрифта

def draw_text(text, font, color, surface, x, y):
    texobj = font.render(text, 1, color)
    textrect = texobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(texobj, textrect)

click = False

def main_menu():
    while True:
        screen.fill((0,0,0))
        draw_text('main menu', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        play_button = pygame.Rect(50, 100, 200, 50)
        settings_button = pygame.Rect(50, 200, 200, 50)
        if play_button.collidepoint((mx, my)):
            if click:
                game()
        if settings_button.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (255, 0, 0), play_button)
        pygame.draw.rect(screen, (255, 0, 0), settings_button)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def game():
    running = True
    while running:
        screen.fill((0,0,0))
        draw_text('game', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        back_button = pygame.Rect(50, 200, 200, 50)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()

        pygame.display.update()


def options():
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_text('options', font, (255, 255, 255), screen, 20, 20)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()

        pygame.display.update()

main_menu()