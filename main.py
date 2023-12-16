import random
import sys
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

bonus_sound = pygame.mixer.Sound('sounds/bonus.mp3')
enemy_hit_sound = pygame.mixer.Sound('sounds/enemy_hit.mp3')
bg_music = 'sounds/bg_music.mp3'
pygame.mixer.music.load(bg_music)
pygame.mixer.music.play(-1)

FPS = pygame.time.Clock()
HEIGHT = 700
WIDTH = 1200
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)
FONT = pygame.font.SysFont('Verdana', 30)
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.transform.scale(pygame.image.load('images/background.png'), (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3
player_size = (20, 20)
player = pygame.image.load('images/player.png').convert_alpha()
player_rect = player.get_rect(midbottom=(WIDTH // 2, HEIGHT))

player_move_down = [0, 6]
player_move_up = [0, -6]
player_move_right = [6, 0]
player_move_left = [-6, 0]

def create_enemy():
    enemy_size = (40, 80)
    enemy = pygame.image.load('images/enemy.png').convert_alpha()
    enemy = pygame.transform.scale(enemy, enemy_size)
    enemy_rect = pygame.Rect(random.randint(100, WIDTH - 100), -enemy_size[1], *enemy_size)
    enemy_move = [0, random.randint(4, 8)]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (80, 80)
    bonus = pygame.image.load('images/bonus.png').convert_alpha()
    bonus = pygame.transform.scale(bonus, bonus_size)
    bonus_rect = pygame.Rect(random.randint(100, WIDTH - 100), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

def game_over_modal():
    modal = True
    restart_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 20, 100, 30)
    exit_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 60, 100, 30)

    while modal:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if restart_button_rect.collidepoint(event.pos):
                        reset_game()
                        modal = False
                    elif exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        modal_surface = pygame.Surface((WIDTH, HEIGHT))
        modal_surface.set_alpha(150)
        modal_surface.fill((0, 0, 0))

        game_over_label = FONT.render("GAME OVER", True, COLOR_WHITE)
        label_rect = game_over_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))

        restart_button = FONT.render("Restart", True, COLOR_GREEN)
        exit_button = FONT.render("Exit", True, COLOR_RED)

        modal_surface.blit(game_over_label, label_rect)
        modal_surface.blit(restart_button, restart_button_rect.topleft)
        modal_surface.blit(exit_button, exit_button_rect.topleft)

        main_display.blit(modal_surface, (0, 0))
        pygame.display.flip()

def reset_game():
    global player_rect, score, enemies, bonuses
    player_rect = player.get_rect(midbottom=(WIDTH // 2, HEIGHT))
    score = 0
    enemies = []
    bonuses = []


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []
score = 0
image_index = 0
playing = True

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
    bg_x1 -= bg_move
    bg_x2 -= bg_move
    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()
    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()
    main_display.blit(bg, (bg_x1, 0))
    main_display.blit(bg, (bg_x2, 0))
    keys = pygame.key.get_pressed()
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        if player_rect.colliderect(enemy[1]):
            enemy_hit_sound.play()
            if score > 0:
                score -= 1
                enemies.pop(enemies.index(enemy))
            elif score == 0:
                pygame.mixer.music.stop()
                game_over_modal()
                pygame.mixer.music.play(-1)
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])
        if player_rect.colliderect(bonus[1]):
            bonus_sound.play()
            score += 1
            bonuses.pop(bonuses.index(bonus))
    main_display.blit(FONT.render(str(score), True, COLOR_GREEN), (WIDTH-50, 20))
    main_display.blit(player, player_rect)
    pygame.display.flip()
    for enemy in enemies:
        if enemy[1].top > HEIGHT:
            enemies.pop(enemies.index(enemy))
    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
