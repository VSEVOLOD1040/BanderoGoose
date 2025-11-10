import random
import time

import pygame
from pygame. constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_f, K_w, K_a, K_s, K_d
from os import listdir


PINK = 204, 12, 255
ORANGE = 255, 127, 12
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0


Colors = [BLUE, ORANGE, PINK, GREEN, RED]
pygame.init()
font = pygame.font.SysFont("Comic Sans MS", 30)
color = random.choice(Colors)

screen = width, height = 800, 600
main_surface = pygame.display.set_mode(screen)
FPS = pygame.time.Clock()
score = 0
bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3
pygame.display.set_caption('Bandero Goose')
pygame.display.set_icon(pygame.image.load('logo.png'))


IMGS_PATH = 'goose'

player_img = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
ball = player_img[0]
ball_rect = ball.get_rect()
ball_speed = 4

is_working = True


def create_enemy():
    sr = random.randint(15, 50)
    size = sr * 3, sr
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), size)

    enemy_rect = pygame.Rect(width + 175, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(1, 5)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    size = 100, 150
    bonus = pygame.transform.scale((pygame.image.load('bonus.png').convert_alpha()), size)

    bonus_rect = pygame.Rect(random.randint(0, width), -175, *bonus.get_size())
    bonus_speed = random.randint(1, 5)
    return [bonus, bonus_rect, bonus_speed]

img_index = 0

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, random.randint(1000, 2000))
enemies = []

CREATE_BONUS = pygame.USEREVENT + 3
pygame.time.set_timer(CREATE_BONUS, random.randint(2000, 5000))
bonuses = []

CHANGE_IMG = pygame.USEREVENT + 4
pygame.time.set_timer(CHANGE_IMG, 125)

DAY_NIGHT = pygame.USEREVENT + 5
pygame.time.set_timer(DAY_NIGHT, 10000)

skip = True
zo = 0

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:

            is_working = False
            skip = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_img):
                img_index = 0
            ball = player_img[img_index]
        if event.type == DAY_NIGHT:
            zo += 1
            if zo == 2:
                zo = 0
            if zo == 0:
                bg = pygame.transform.scale(pygame.image.load('bg_n.n.jpg').convert(), screen)
            else:
                bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)


    pressed_key = pygame.key.get_pressed()




    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()
    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))


    # main_surface.blit(bg, (0, 0))
    main_surface.blit(ball, ball_rect)



    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        if bonus[1].bottom > height + 175:
            bonuses.pop(bonuses.index(bonus))
        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score = score + 1

            color = random.choice(Colors)

    main_surface.blit(font.render(str(score), True, color), (width - 40, 10))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])
        if enemy[1].left < -175:
            enemies.pop(enemies.index(enemy))
        if ball_rect.colliderect(enemy[1]):
            is_working = False


    if pressed_key[K_DOWN] and not ball_rect.bottom >= height:
        ball_rect = ball_rect.move(0, ball_speed)
    if pressed_key[K_UP] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move(0, -ball_speed)
    if pressed_key[K_LEFT] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move(-ball_speed, 0)
    if pressed_key[K_RIGHT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed, 0)

    # WASD

    if pressed_key[K_s] and not ball_rect.bottom >= height:
        ball_rect = ball_rect.move(0, ball_speed)
    if pressed_key[K_w] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move(0, -ball_speed)
    if pressed_key[K_a] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move(-ball_speed, 0)
    if pressed_key[K_d] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed, 0)


    if pressed_key[K_f]:
        pygame.display.toggle_fullscreen()

    #main_surface.fill((155, 155, 155))
    pygame.display.flip()

if skip == True:
    main_surface.fill(BLACK)
    pygame.display.flip()
    font = pygame.font.SysFont("Comic Sans MS", 50)
    main_surface.blit(font.render(str(f"Your score is: {score}"), True, color), (210, 400))
    font = pygame.font.SysFont("Comic Sans MS", 60)
    main_surface.blit(font.render(str("GAME OVER!"), True, color), (210, 200))
    pygame.display.flip()
    print("Your score is", score)
    time.sleep(2)
