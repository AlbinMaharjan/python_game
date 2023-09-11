import pygame
import random
import math
import sys
from pygame import mixer

# Initialize Pygame and Mixer
mixer.init()
pygame.init()

# Create the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Shooter Game')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Load background music and play it in a loop
mixer.music.load('background.wav')
mixer.music.play(-1)

# Load game assets (images and sounds)
background = pygame.image.load('background.png')
player_img = pygame.image.load('khiladi.png')
bullet_img = pygame.image.load('goli.png')

# Initialize game variables
spaceshipX = 370
spaceshipY = 470
player_speed = 5
score = 0
level = 1
no_of_enemies = 6
enemies = []

# Initialize enemy data
for _ in range(no_of_enemies):
    enemy = {
        'img': pygame.image.load('dushman.png'),
        'x': random.randint(0, 736),
        'y': random.randint(30, 150),
        'speed_x': -1,
        'speed_y': 40
    }
    enemies.append(enemy)

# Bullet data
bullet = {
    'x': 0,
    'y': 490,
    'speed_y': 5,
    'fired': False
}

# Font for displaying text
font = pygame.font.Font(None, 36)

# Game over font
font_gameover = pygame.font.Font(None, 72)

# High score variable
high_score = 0

# Game state variables
game_active = True
game_over = False

# Function to display player on the screen
def display_player(x, y):
    screen.blit(player_img, (x, y))

# Function to display the score on the screen
def display_score():
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

# Function to display the high score on the screen
def display_high_score():
    high_score_text = font.render(f'High Score: {high_score}', True, (255, 255, 255))
    screen.blit(high_score_text, (600, 10))

# Function to display game over message
def game_over_message():
    game_over_text = font_gameover.render('Game Over', True, (255, 0, 0))
    screen.blit(game_over_text, (250, 250))
    restart_text = font.render('Press R to Restart', True, (255, 255, 255))
    screen.blit(restart_text, (250, 350))

# Function to handle collisions and updates
def update_game():
    global level, score, spaceshipX, game_over, game_active, high_score  # Declare necessary variables as global

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True  # Signal to exit the game

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        spaceshipX -= player_speed
    if keys[pygame.K_RIGHT]:
        spaceshipX += player_speed

    # Fire bullet
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not bullet['fired']:
        bullet['fired'] = True
        bullet['x'] = spaceshipX + 16
        bullet_sound = mixer.Sound('laser.wav')
        bullet_sound.play()

    # Update bullet position
    if bullet['fired']:
        screen.blit(bullet_img, (bullet['x'], bullet['y']))
        bullet['y'] -= bullet['speed_y']
        if bullet['y'] <= 0:
            bullet['y'] = 490
            bullet['fired'] = False

    # Update enemy positions
    for enemy in enemies:
        if enemy['y'] >= 420:
            game_active = False  # Signal that the game is over
            if score > high_score:
                high_score = score  # Update high score
            return False  # Signal to end the game

        enemy['x'] += enemy['speed_x']
        if enemy['x'] <= 0:
            enemy['speed_x'] = 1
            enemy['y'] += enemy['speed_y']
        if enemy['x'] >= 736:
            enemy['speed_x'] = -1
            enemy['y'] += enemy['speed_y']

        # Check for collisions
        distance = math.sqrt(math.pow(bullet['x'] - enemy['x'], 2) + math.pow(bullet['y'] - enemy['y'], 2))
        if distance < 27:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet['y'] = 490
            bullet['fired'] = False
            enemy['x'] = random.randint(0, 736)
            enemy['y'] = random.randint(30, 150)
            score += 5

        screen.blit(enemy['img'], (enemy['x'], enemy['y']))

    # Display player and score
    display_player(spaceshipX, spaceshipY)
    display_score()
    display_high_score()

    return False  # Continue the game

# Main game loop
running = True

while running:
    if game_active:
        screen.blit(background, (0, 0))
        game_over = update_game()

    if game_over:
        game_over_message()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset the game if 'R' is pressed
            game_over = False
            level = 1
            score = 0
            spaceshipX = 370
            bullet['fired'] = False
            enemies.clear()
            for _ in range(no_of_enemies):
                enemy = {
                    'img': pygame.image.load('dushman.png'),
                    'x': random.randint(0, 736),
                    'y': random.randint(30, 150),
                    'speed_x': -1,
                    'speed_y': 40
                }
                enemies.append(enemy)
            game_active = True  # Ensure the game is active when restarting

    pygame.display.update()

# Save the high score to a file
with open('highscore.txt', 'w') as f:
    f.write(str(high_score))

pygame.quit()
sys.exit()
