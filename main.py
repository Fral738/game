import pygame
from pygame.locals import *
import os
import random

# --------------------------------------- Разрешения экрана ----------------------------------------------------
width = [1920, 1600, 1280]
heigh = [1080, 900, 720]
res_width, res_height = width[2], heigh[2]
# --------------------------------------------------------------------------------------------------------------

# ---------------------------------------- Константные цвета --------------------------------------------------
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
player_color = (255, 0, 255)
bonus_color = (255, 0, 0)
speed = 1
# ----------------------------------------------------------------------------------------------------------------

# ------------------------------------- Инициализация плеера ---------------------------------------------------
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
songs = ['song1.mp3', 'song2.mp3', 'song3.mp3']
song_end = pygame.USEREVENT + 1
current_song = None
pygame.mixer_music.set_endevent(song_end)
pygame.mixer_music.set_volume(0.05)
# -------------------------------------------------------------------------------------------------------------
# Инициализация pygame
pygame.init()
main_Clock = pygame.time.Clock()  # Добавляем таймер, своего рода FPS - количество кадров в секунду
screen = pygame.display.set_mode((res_width, res_height))  # Создаем окно с размерами 1920x1080
flags = screen.get_flags()

pygame.display.set_caption("Dodge this")  # Задаем название окна
font = pygame.font.SysFont(None, 40)  # Задаем размер шрифта


class Block(pygame.sprite.Sprite):  # Класс блок (игрок) с функциями соприкосновения и позиционирования
    def __init__(self):
        super(Block, self).__init__()
        self.img = pygame.image.load('Assets/char/Spaceship_dodge-PC.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

    def set_pos(self, x, y):
        # Ставит блок в центре координат x и y
        self.rect.x = x - self.centerx
        self.rect.y = y - self.centery

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite


class Bonus(pygame.sprite.Sprite):  # Класс бонуса (элемент игры, дающий доп. очки)
    def __init__(self, x, y):
        super(Bonus, self).__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(bonus_color)
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.centerx
        self.rect.y = y - self.rect.centery


class Bullet(pygame.sprite.Sprite):  # Класс пули с функциями обновления, соприкосновения, рандомного появления и
    # установки направления
    def __init__(self, xpos, ypos, hspeed, vspeed):
        super(Bullet, self).__init__()
        self.image = pygame.image.load('Assets/char/bullet.png')
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


def random_bullet(speed):
    random_or = random.randint(1, 4)
    if random_or == 1:  # Сверху -> Вниз
        return Bullet(random.randint(0, res_width), 0, 0, speed)
    elif random_or == 2:  # Справа -> Налево
        return Bullet(res_width, random.randint(0, res_height), -speed, 0)
    elif random_or == 3:  # Снизу -> Вверх
        return Bullet(random.randint(0, res_width), res_height, 0, -speed)
    elif random_or == 4:  # Слева -> Направо
        return Bullet(0, random.randint(0, res_height), speed, 0)


def get_config_dir():  # Функция создания папки игры для сохранения
    confdir = os.path.join(os.path.expanduser("~"), '.config')
    game_confdir = os.path.join(confdir, "best_game")
    try:
        os.makedirs(game_confdir)
    except OSError:
        pass
    return game_confdir


class Score:  # Класс "Очки" с функциями сохранения и загрузки в виде файла
    def __init__(self):
        self.HIGHEST_SCORE_PATH = os.path.join(get_config_dir(), 'highest_score')
        if not os.path.exists(self.HIGHEST_SCORE_PATH):
            with open(self.HIGHEST_SCORE_PATH, 'w') as highest_score_file:
                highest_score_file.write('0')
        self.high_score = self.highest_score = self.load_highest_score()
        self.points = 0

    def load_highest_score(self):
        with open(self.HIGHEST_SCORE_PATH, 'r') as highest_score_file:
            highest_score = int(highest_score_file.readlines()[0])
        return highest_score

    def save_highest_score(self):
        print("123")
        with open(self.HIGHEST_SCORE_PATH, 'w') as highest_score_file:
            highest_score_file.write(str(self.high_score))


def draw_text(text, font, color, screen, x, y):  # Функция отрисовки текста
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_obj, text_rect)


def draw_repeating_background(background_img):
    new_image = pygame.transform.scale(background_img, (res_width, res_height))
    background_rect = new_image.get_rect(bottomright=(res_width, res_height))
    screen.blit(background_img, background_rect)


def game_over_screen():  # Функция окна смерти
    # -------------------------------- Создание прозрачного экрана --------------------------------------------------
    transp_surf = pygame.Surface((res_width, res_height))
    transp_surf.set_alpha(200)
    screen.blit(transp_surf, transp_surf.get_rect())
    pygame.mouse.set_visible(True)
    # --------------------------------------------------------------------------------------------------------------

    # ------------------------------------ Отрисовка текста --------------------------------------------------------
    draw_text('Рекорд: {}'.format(score.high_score), font, white, screen, res_width / 2, res_height / 2 - 80)
    draw_text('Вы проиграли', font, white, screen, res_width / 2, res_height / 2 - 120)
    draw_text('Нажмите на ПРОБЕЛ для рестарта ', font, white, screen, res_width / 2, res_height / 2 - 40)
    draw_text('Нажмите ESC, чтобы выйти', font, white, screen, res_width / 2, res_height / 2)
    # -------------------------------------------------------------------------------------------------------------
    pygame.display.update()
    pygame.mixer_music.load('death song.mp3')
    pygame.mixer_music.play()
    # --------------------------------- Проверка условий нажатий кнопок -------------------------------------------
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu(screen)
                elif event.key == K_SPACE:
                    game()
    # ------------------------------------------------------------------------------------------------------------


def main_menu(screen):  # Функция окна "Главное меню"
    info_object = pygame.display.Info()
    # print(info_object)  #  для дебага

    if pygame.mixer_music.get_busy():  # Проверка на проигрывание музыки
        pass
    else:
        pygame.mixer_music.load('main menu melody.mp3')
        pygame.mixer_music.play()

    # -------------------- Блок с отрисовкой кнопок ------------------------------------------
    menu_image = pygame.image.load("Assets/menu/Menu Button.png")
    menu_image = pygame.transform.scale(menu_image, (300, 100))  # Задание размера "Меню"
    menu_rect = menu_image.get_rect()

    play_image = pygame.image.load("Assets/menu/Play Button.png")
    play_image = pygame.transform.scale(play_image, (200, 67))  # Задание размеров кнопок
    play_button = play_image.get_rect()  # Задание такого же размера для остальных кнопок

    settings_image = pygame.image.load("Assets/menu/Settings Button.png")
    settings_image = pygame.transform.scale(settings_image, (200, 67))
    settings_button = settings_image.get_rect()

    exit_image = pygame.image.load("Assets/menu/Exit Button.png")
    exit_image = pygame.transform.scale(exit_image, (200, 67))
    exit_button = exit_image.get_rect()
    # --------------------------------------------------------------------------------------------
    while True:
        screen.fill(black)  # Заполнение экрана черным фоном
        screen.blit(menu_image, ((info_object.current_w / 2) - menu_rect.centerx,
                                 (info_object.current_h / 10) - menu_rect.centery))

        mx, my = pygame.mouse.get_pos()  # переменные для хранения позиции мыши

        play_button.move_ip((info_object.current_w / 2) - play_button.centerx,
                            (info_object.current_h / 4) - play_button.centery)
        screen.blit(play_image, play_button)

        settings_button.move_ip((info_object.current_w / 2) - settings_button.centerx,
                                (info_object.current_h / 2.8 - settings_button.centery))
        screen.blit(settings_image, settings_button)

        exit_button.move_ip((info_object.current_w / 2) - exit_button.centerx,
                            (info_object.current_h / 2.15 - exit_button.centery))
        screen.blit(exit_image, exit_button)

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
    start_time = pygame.time.get_ticks()
    mx, my = pygame.mouse.get_pos()
    square = Block()
    bullets = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()
    throw = 15  # Вероятность срабатывания
    min_bullet_speed = 1  # Минимальная скорость снаряядов
    max_bullet_speed = 2  # Максимальная скорость снарядов
    bullets_per_tick = 3  # Кол-во ракет за тик
    background_surf = pygame.image.load('Assets/background/background.png')
    draw_repeating_background(background_surf)
    pygame.display.update()
    shuffle()
    while True:  # Пока запущено
        pause_mx, pause_my = pygame.mouse.get_pos()
        pygame.time.Clock().tick(60)
        pygame.display.update()
        if not paused:
            pygame.mixer_music.unpause()
            time_score = pygame.time.get_ticks() - start_time
            seconds = int(time_score / 1000 % 60)
            minutes = int(time_score / 60000 % 24)
            mx, my = pygame.mouse.get_pos()
            pygame.mouse.set_visible(False)
            draw_repeating_background(background_surf)
            draw_text('Кол-во очков: {}'.format(score.points), font, white, screen, res_width / 4, 20)
            draw_text('Рекорд: {}'.format(score.high_score), font, white, screen, res_width / 1.25, 20)
            draw_text("Время: {0:02}:{1:02}".format(minutes, seconds), font, white, screen, res_width / 2, 20)

            if 15 <= round(time_score / 1000) <= 30:
                throw = 12
                max_bullet_speed = 3
            elif 30 <= round(time_score / 1000) <= 45:
                throw = 10
                max_bullet_speed = 5
                bullets_per_tick = 4
            elif 45 <= round(time_score / 1000) <= 60:
                throw = 7
                max_bullet_speed = 6
                min_bullet_speed = 2
            elif 60 <= round(time_score / 1000) <= 75:
                throw = 6
                max_bullet_speed = 5
            elif 75 <= round(time_score / 1000) <= 90:
                max_bullet_speed = 7
                bullets_per_tick = 5
            elif 90 <= round(time_score / 1000) <= 105:
                min_bullet_speed = 4
            elif 105 <= round(time_score / 1000) <= 120:
                bullets_per_tick = 6
                max_bullet_speed = 10
            elif 120 <= round(time_score / 1000) <= 135:
                max_bullet_speed = 12
            elif 135 <= round(time_score / 1000) >= 150:
                bullets_per_tick = 7
                min_bullet_speed = 6
                max_bullet_speed = 13
            elif 150 <= round(time_score / 1000) >= 165:
                bullets_per_tick = 8
                max_bullet_speed = 115

            if random.randint(1, throw) == 1:
                if random.randint(1, throw * 10) == 1:
                    bonus = Bonus(random.randint(30, res_width - 30),
                                  random.randint(30, res_height - 30))
                    bonuses.add(bonus)
                for i in range(bullets_per_tick):
                    bullets.add(random_bullet(random.randint(min_bullet_speed,
                                                             max_bullet_speed)))
                    score.points += 1
            bullets.update()
            bonuses.update()
            bullets.draw(screen)
            bonuses.draw(screen)
            bonus = square.collide(bonuses)

            if square.collide(bullets):  # Тут еще надо добавить Очки и время чтоб сохранялись.
                pygame.mixer_music.stop()
                if score.high_score > score.highest_score:
                    score.save_highest_score()
                game_over_screen()
            if bonus:
                score.points += 10
                bonus.kill()

            if score.points > score.high_score:
                score.high_score = score.points

            square.set_pos(mx - 15, my - 15)
            screen.blit(square.img, square.rect)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = True
                        if paused:
                            pygame.mixer_music.pause()
                            transp_surf = pygame.Surface((res_width, res_height))
                            transp_surf.set_alpha(150)
                            screen.blit(transp_surf, transp_surf.get_rect())
                            pygame.mouse.set_visible(True)
                            draw_text('Пауза', font, white, screen, res_width / 2, res_height / 2 - 120)
                            draw_text('Для того, чтобы продолжить, наведите мышку на квадрат', font, white, screen,
                                      res_width / 2, res_height / 2 + 120)
                            draw_text('Нажмите ESC чтобы выйти', font, white, screen, res_width / 2,
                                      res_height / 2 )
                            draw_text('Нажмите ПРОБЕЛ чтобы продолжить', font, white, screen, res_width / 2,
                                      (res_height / 2 + 40))

                if event.type == song_end:
                    shuffle()
        else:
            time_pause = pygame.time.get_ticks() - start_time - time_score
            for event in pygame.event.get():
                if event.type == KEYDOWN:  # Условие на нажатие любой кнопки
                    if event.key == K_s:
                        pygame.mixer_music.stop()  # Условие на нажатие кнопки S

                    if (event.key == pygame.K_SPACE) and (mx - 20 <= pause_mx <= mx + 20) and (
                            my - 20 <= pause_my <= my + 20):
                        paused = False
                        start_time = start_time + time_pause

                    if event.key == K_ESCAPE:  # Условие на нажатие кнопки Escape
                        if score.high_score > score.highest_score:
                            score.save_highest_score()
                        main_menu(screen)  # Возвращение в главное меню


def options(screen):  # Функция окна "Настройки"
    info_object = pygame.display.Info()
    # print(info_object)  #  для дебага
    global res_width, res_height, flags
    screen.fill(black)  # Пока запущено

    option_image = pygame.image.load("Assets/menu/Options Button.png")
    option_image = pygame.transform.scale(option_image, (300, 100))  # Задание размера "Меню"
    option_rect = option_image.get_rect()

    back_image = pygame.image.load("Assets/menu/Back Button.png")
    back_image = pygame.transform.scale(back_image, (200, 67))
    back_rect = back_image.get_rect()

    res_image = pygame.image.load("Assets/menu/Resolution Button.png")
    res_image = pygame.transform.scale(res_image, (200, 67))
    res_rect = res_image.get_rect()

    fullres_image = pygame.image.load("Assets/menu/Fullscreen Button.png")
    fullres_image = pygame.transform.scale(fullres_image, (200, 67))
    fullres_rect = fullres_image.get_rect()

    fullhd_image = pygame.image.load("Assets/menu/1980x1024 Button.png")
    fullhd_image = pygame.transform.scale(fullhd_image, (200, 67))
    fullhd_rect = fullhd_image.get_rect()

    hd_image = pygame.image.load("Assets/menu/1600x900 Button.png")
    hd_image = pygame.transform.scale(hd_image,(200, 67))
    hd_rect = hd_image.get_rect()

    wxga_image = pygame.image.load("Assets/menu/1280x720 Button.png")
    wxga_image = pygame.transform.scale(wxga_image, (200, 67))
    wxga_rect = wxga_image.get_rect()

    while True:
        mx, my = pygame.mouse.get_pos()  # переменные для хранения позиции мыши
        click = False

        screen.blit(option_image, ((info_object.current_w / 2) - option_rect.centerx,
                                 (info_object.current_h / 10) - option_rect.centery))

        res_rect.move_ip((info_object.current_w / 2) - res_rect.centerx,
                            (info_object.current_h / 4) - res_rect.centery)
        screen.blit(res_image, res_rect)

        fullhd_rect.move_ip((info_object.current_w / 3) - fullhd_rect.centerx,
                          (info_object.current_h / 2.8 - fullhd_rect.centery))
        screen.blit(fullhd_image, fullhd_rect)

        hd_rect.move_ip((info_object.current_w / 2) - hd_rect.centerx,
                            (info_object.current_h / 2.8 - hd_rect.centery))
        screen.blit(hd_image, hd_rect)

        wxga_rect.move_ip((info_object.current_w / 1.5) - wxga_rect.centerx,
                        (info_object.current_h / 2.8 - wxga_rect.centery))
        screen.blit(wxga_image, wxga_rect)

        fullres_rect.move_ip((info_object.current_w / 2) - fullres_rect.centerx,
                                (info_object.current_h / 2.15 - fullres_rect.centery))
        screen.blit(fullres_image, fullres_rect)

        back_rect.move_ip((info_object.current_w / 2) - back_rect.centerx,
                            (info_object.current_h / 1.75 - back_rect.centery))
        screen.blit(back_image, back_rect)

        for event in pygame.event.get():  # Считывание всех действий мыши и клавиатуры
            if event.type == KEYDOWN:  # Условие на нажатие любой кнопки
                if event.key == K_ESCAPE:  # Условие на нажатие кнопки Escape
                    main_menu(screen)  # Возвращение в главное меню

            if event.type == MOUSEBUTTONDOWN:  # Условие на нажатие левой кнопки мыши
                if event.button == 1:  # Если нажата
                    click = True  # инвертируем флаг

        if fullres_rect.collidepoint(mx, my) and click:
            if flags & FULLSCREEN == False:
                flags |= FULLSCREEN
                screen = pygame.display.set_mode((width[0], heigh[0]), flags)
                res_width, res_height = width[0], heigh[0]
            else:

                flags ^= FULLSCREEN
                screen = pygame.display.set_mode((res_width, res_height), flags)

        if res_rect.collidepoint(mx, my) and click:
            screen.fill(black)  # Пока запущено
            pygame.draw.rect(screen, red, fullhd_rect)  # Отрисовка кнопки
            draw_text('1920x1080', font, white, screen, 350, 100)  # Отрисовка текста кнопки
            pygame.draw.rect(screen, red, wxga_rect)  # Отрисовка кнопки
            draw_text('1600x900', font, white, screen, 600, 100)  # Отрисовка текста кнопки
            pygame.draw.rect(screen, red, hd_rect)  # Отрисовка кнопки
            draw_text('1280x720', font, white, screen, 850, 100)  # Отрисовка текста кнопки
            pygame.display.update()
        if back_rect.collidepoint(mx, my) and click:
            main_menu(screen)

        if fullhd_rect.collidepoint(mx, my) and click:
            screen = pygame.display.set_mode((width[0], heigh[0]))
            res_height = heigh[0]
            res_width = width[0]

        if hd_rect.collidepoint(mx, my) and click:
            screen = pygame.display.set_mode((width[1], heigh[1]))
            res_height = heigh[1]
            res_width = width[1]

        if wxga_rect.collidepoint(mx, my) and click:
            screen = pygame.display.set_mode((width[2], heigh[2]))
            res_height = heigh[2]
            res_width = width[2]
        pygame.display.update()  # Обновление экрана


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
