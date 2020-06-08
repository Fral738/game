import pygame
from pygame.locals import *
import os
import random

width = [1920, 1600, 1280]
heigh = [1080, 900, 720]
res_width, res_height = width[2], heigh[2]

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 70, 225)
green = (0, 255, 0)
red = (255, 0, 0)
speed = 1

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
songs = ['song1.mp3', 'song2.mp3', 'song3.mp3']
song_end = pygame.USEREVENT + 1
current_song = None
pygame.mixer_music.set_endevent(song_end)
pygame.mixer_music.set_volume(0.05)

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
        'Ставит блок в центре координат x и y'
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
        self.image.fill(bonus_color)
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


def random_bullet(speed):
    random_or = random.randint(1, 4)
    if random_or == 1:  # Up -> Down
        return Bullet(random.randint(0, res_width), 0, 0, speed)
    elif random_or == 2:  # Right -> Left
        return Bullet(res_width, random.randint(0, res_height), -speed, 0)
    elif random_or == 3:  # Down -> Up
        return Bullet(random.randint(0, res_width), res_height, 0, -speed)
    elif random_or == 4:  # Left -> Right
        return Bullet(0, random.randint(0, res_height), speed, 0)


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


def game_over_screen():
    transp_surf = pygame.Surface((res_width, res_height))
    transp_surf.set_alpha(200)
    screen.blit(transp_surf, transp_surf.get_rect())
    pygame.mouse.set_visible(True)
    draw_text('Вы проиграли', font, white, screen, res_width / 2, res_height / 2 - 80)
    draw_text('Нажмите на ПРОБЕЛ для рестарта ', font, white, screen, res_width / 2, res_height / 2 - 40)
    draw_text('Нажмите ESC, чтобы выйти', font, white, screen, res_width / 2, res_height / 2)
    pygame.display.update()
    pygame.mixer_music.load('death song.mp3')
    pygame.mixer_music.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu(screen)
                elif event.key == K_SPACE:
                    game()


def main_menu(screen):  # Функция окна "Главное меню"
    infoObject = pygame.display.Info()
    print(infoObject)
    pygame.mixer_music.load('main menu melody.mp3')
    pygame.mixer_music.play()

    menu_image = pygame.image.load("Assets/menu/Menu Button.png")
    menu_image = pygame.transform.scale(menu_image, (300, 100))  # that's just half our menu image
    menu_rect = menu_image.get_rect()

    play_image = pygame.image.load("Assets/menu/Play Button.png")
    play_image = pygame.transform.scale(play_image, (200, 67))  # same as menu image, but divided by 3 instead of 2
    play_button = play_image.get_rect()  # this rectangular size will be uniform for the rest of the buttons

    settings_image = pygame.image.load("Assets/menu/Settings Button.png")
    settings_image = pygame.transform.scale(settings_image, (200, 67))
    settings_button = settings_image.get_rect()

    exit_image = pygame.image.load("Assets/menu/Exit Button.png")
    exit_image = pygame.transform.scale(exit_image, (200, 67))
    exit_button = exit_image.get_rect()

    while True:
        screen.fill(black)  # Заполнение экрана черным фоном
        screen.blit(menu_image, ((infoObject.current_w / 2) - menu_rect.centerx,
                                 (infoObject.current_h / 10) - menu_rect.centery))

        mx, my = pygame.mouse.get_pos()  # переменные для хранения позиции мыши

        play_button.move_ip((infoObject.current_w / 2) - play_button.centerx,
                            (infoObject.current_h / 4) - play_button.centery)
        screen.blit(play_image, play_button)

        settings_button.move_ip((infoObject.current_w / 2) - settings_button.centerx,
                                (infoObject.current_h / 2.8 - settings_button.centery))
        screen.blit(settings_image, settings_button)

        exit_button.move_ip((infoObject.current_w / 2) - exit_button.centerx,
                            (infoObject.current_h / 2.15 - exit_button.centery))
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
    min_bullet_speed = 1
    max_bullet_speed = 1
    bullets_per_gust = 1
    odds = 12
    background_surf = pygame.image.load('background.png')
    draw_repeating_background(background_surf)
    pygame.display.update()
    shuffle()
    while True:  # Пока запущено
        time_pause = 0
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
            draw_text('Кол-во очков: {}'.format(score.points), font, white, screen, 110, 20)
            draw_text('Рекорд: {}'.format(score.high_score), font, white, screen, 70, 50)
            draw_text("Время: {0:02}:{1:02}".format(minutes, seconds), font, white, screen, 90, 80)
            if time_score >= 15:
                odds = 11
                max_bullet_speed = 2
            elif time_score >= 30:
                odds = 10
                max_bullet_speed = 3
            elif time_score >= 45:
                odds = 9
                max_bullet_speed = 4
            elif time_score >= 60:
                odds = 8
                max_bullet_speed = 5
            elif time_score >= 75:
                max_bullet_speed = 8
            elif time_score >= 90:
                min_bullet_speed = 2
            elif time_score >= 105:
                bullets_per_gust = 2
                max_bullet_speed = 10
            elif time_score >= 120:
                max_bullet_speed = 20
            elif time_score >= 135:
                bullets_per_gust = 3
                min_bullet_speed = 3
                max_bullet_speed = 15
            elif time_score >= 150:
                bullets_per_gust = 3000
                max_bullet_speed = 80

            if random.randint(1, odds) == 1:
                if random.randint(1, odds * 10) == 1:
                    bonus = Bonus(random.randint(30, res_width - 30),
                                  random.randint(30, res_height - 30))
                    bonuses.add(bonus)
                for i in range(bullets_per_gust):
                    bullets.add(random_bullet(random.randint(min_bullet_speed,
                                                             max_bullet_speed)))
                    score.points += 1
            bullets.update()
            bonuses.update()
            bullets.draw(screen)
            bonuses.draw(screen)
            bonus = square.collide(bonuses)
            # if square.collide(bullets): #Тут еще надо добавить Очки и время чтоб сохранялись.
            #     pygame.mixer_music.stop()
            #     game_over_screen()
            # if bonus:
            #     score.points += 10
            #     bonus.kill()
            square.set_pos(mx-15, my-15)
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
                            draw_text('Нажмите ESC чтобы выйти', font, white, screen, res_width/2, res_height/2+40)
                            draw_text('Нажмите ПРОБЕЛ чтобы продолжить', font, white, screen, res_width/2,
                                      (res_height/2))
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
                    if event.key == K_ESCAPE:  # Условие на нажатие кнопки Escapezz
                        main_menu(screen)  # Возвращение в главное меню


def options(screen):  # Функция окна "Настройки"
    global res_width, res_height, flags
    screen.fill(black)  # Пока запущено
    while True:
        mx, my = pygame.mouse.get_pos()  # переменные для хранения позиции мыши
        click = False
        draw_text('Опции', font, (255, 255, 255), screen, res_width / 2, 20)  # Отрисовка белого текста
        resolution = pygame.Rect(100, 100, 200, 50)  # Параметры прямоугольника для кнопки
        full_screen = pygame.Rect(100, 200, 200, 50)  # Параметры прямоугольника для кнопки
        full_hd = pygame.Rect(350, 100, 200, 50)  # Параметры прямоугольника для кнопки
        wxga = pygame.Rect(600, 100, 200, 50)  # Параметры прямоугольника для кнопки
        hd = pygame.Rect(850, 100, 200, 50)  # Параметры прямоугольника для кнопки
        back = pygame.Rect(100, 300, 200, 50)  # Параметры прямоугольника для кнопки

        pygame.draw.rect(screen, red, resolution)  # Отрисовка кнопки
        draw_text('Разрешение экрана', font, white, screen, 100, 100)  # Отрисовка текста кнопки
        pygame.draw.rect(screen, red, full_screen)  # Отрисовка кнопки
        draw_text('Полноэкранный режим', font, white, screen, 100, 200)  # Отрисовка текста кнопки
        pygame.draw.rect(screen, red, back)
        draw_text('Назад', font, white, screen, 100, 300)

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
