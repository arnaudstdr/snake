# snake_game.py

import pygame
import time
import random
import os

# Initialisation de Pygame et du mixer
pygame.init()
pygame.mixer.init()

# Charger les sons
eat_sound = pygame.mixer.Sound("eat_sound.wav")
game_over_sound = pygame.mixer.Sound("game_over_sound.wav")

# Définir les couleurs
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Définir les dimensions de l'écran
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_displace])


def read_high_scores(file_name):
    if not os.path.exists(file_name):
        return []
    with open(file_name, 'r') as file:
        scores = file.readlines()
    scores = [int(score.strip()) for score in scores]
    return scores


def write_high_scores(file_name, scores):
    with open(file_name, 'w') as file:
        for score in scores:
            file.write(f"{score}\n")


def update_high_scores(scores, new_score, max_scores=1):
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:max_scores]
    return scores

def flash_screen():
    flash_color = (255, 0, 0)
    for _ in range(3):
        dis.fill(flash_color)
        pygame.display.update()
        time.sleep(0.1)
        dis.fill(blue)
        pygame.display.update()
        time.sleep(0.1)

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    high_scores = read_high_scores("high_scores.txt")

    while not game_over:

        while game_close:
            dis.fill(blue)
            score = Length_of_snake - 1

            message("You Lost! Press Q-Quit or C-Play Again", red)
            message(f"Your Score: {score}", yellow, 40)

            high_scores = update_high_scores(high_scores, score)
            write_high_scores("high_scores.txt", high_scores)

            message("High Scores:", yellow, 80)
            for i, high_score in enumerate(high_scores):
                message(f"{i + 1}. {high_score}", yellow, 120 + i * 20)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_over_sound.play()
            flash_screen()
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_over_sound.play()
                flash_screen()
                game_close = True

        our_snake(snake_block, snake_List)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            eat_sound.play()
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
