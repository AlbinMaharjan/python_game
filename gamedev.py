import pygame
import random
import math
from pygame import mixer
import time

mixer.init()
pygame.init()

mixer.music.load('background.wav')
mixer.music.play(-1)      

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Welcome To The Space Shooter Game')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Load background, player, and enemy images
background = pygame.image.load('background.png')
player_img = pygame.image.load('khiladi.png')
enemy_img = []
enemyX = []
enemyY = []
enemy_speedX = []
enemy_speedY = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemy_img.append(pygame.image.load('dushman.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(30, 150))
    enemy_speedX.append(-1)
    enemy_speedY.append(40)

# Player spaceship
spaceship_img = pygame.image.load('khiladi.png')
spaceshipX = 370
spaceshipY = 470
spaceship_changeX = 0

# Bullet
bullet_img = pygame.image.load('goli.png')
bulletX = 0
bulletY = 490
bullet_state = "ready"  # The bullet is ready to fire

score = 0

# Game over variables
game_over_font = pygame.font.SysFont('Arial', 64,'red')
game_over_animation_time = 5  # seconds
game_over_time = None

# Level control
current_level = 1
level2_started = False

# Mouse control variables
mouse_control = False

# Load and display the player's score
try:
    with open('highscore.txt', 'r') as file:
        high_score = int(file.read())
except FileNotFoundError:  # First time
    high_score = 0

font = pygame.font.SysFont('Arial', 32)

def show_score(x, y):
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    high_score_text = font.render(f'High Score: {high_score}', True, (255, 255, 255))
    screen.blit(score_text, (x, y))
    screen.blit(high_score_text, (x, y + 40))

def update_high_score():
    if score > high_score:
        with open('highscore.txt', 'w') as file:
            file.write(str(score))

# Create a function to store the player's score in a file
def store_score():
    update_high_score()
    with open('score.txt', 'a') as file:
        file.write(f'Score: {score}\n')

def is_collision(x1, y1, x2, y2):
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance < 27

def is_game_over(y_values):
    return any(y >= 420 for y in y_values)

def show_game_over():
    game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
    screen.blit(game_over_text, (200, 250))

def reset_game():
    global score, spaceshipX, bulletX, bulletY, bullet_state, enemyX, enemyY, current_level
    score = 0
    spaceshipX = 370
    bulletX = 0
    bulletY = 490
    bullet_state = "ready"
    enemyX = [random.randint(0, 736) for _ in range(no_of_enemies)]
    enemyY = [random.randint(30, 150) for _ in range(no_of_enemies)]
    current_level = 1

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

# Main game loop
running = True
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceship_changeX = -5
            if event.key == pygame.K_RIGHT:
                spaceship_changeX = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = spaceshipX + 16
                    fire_bullet(bulletX, bulletY)
                    bullet_state = "fire"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceship_changeX = 0

    # Mouse control
    if mouse_control:
        mouse_x, _ = pygame.mouse.get_pos()
        spaceshipX = mouse_x - 32

    spaceshipX += spaceship_changeX

    # Keep the spaceship within the screen boundaries
    if spaceshipX <= 0:
        spaceshipX = 0
    elif spaceshipX >= 736:
        spaceshipX = 736

    # Enemy movement and collision
    for i in range(no_of_enemies):
        enemyX[i] += enemy_speedX[i]
        if enemyX[i] <= 0:
            enemy_speedX[i] = 1
            enemyY[i] += enemy_speedY[i]
        elif enemyX[i] >= 736:
            enemy_speedX[i] = -1
            enemyY[i] += enemy_speedY[i]

        # Check for collision
        if is_collision(enemyX[i], enemyY[i], bulletX, bulletY):
            explosion_sound = mixer.Sound('explosion.wav')  # sound overwrite nahos bhanera
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 5
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(30, 150)

        screen.blit(enemy_img[i], (enemyX[i], enemyY[i]))

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= 5

    # Display the player's spaceship and score
    screen.blit(player_img, (spaceshipX, spaceshipY))
    show_score(10, 10)

    if current_level == 2 and not level2_started:
        # Add new enemy types for level 2
        enemy_img.append(pygame.image.load('level2_enemy.png'))
        enemy_speedX.append(-2)
        enemy_speedY.append(20)
        level2_started = True

    # Check for level completion
    if current_level == 1 and score >= 50:
        current_level = 2
        level2_started = True
        time.sleep(2)  # Give a short break between levels

    if is_game_over(enemyY):
        if game_over_time is None:
            game_over_time = time.time() + game_over_animation_time
        elif time.time() >= game_over_time:
            show_game_over()
            time.sleep(5)  # Display game over message for 5 seconds
            store_score()  # Store the player's score
            reset_game()
            game_over_time = None

    pygame.display.update()

pygame.quit()
