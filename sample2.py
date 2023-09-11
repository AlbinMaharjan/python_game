import pygame
import random
import math
from pygame import mixer
import time


pygame.init()                   # Initialize Pygame
mixer.init()                    # Initialize mixer
# Constants
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Welcome To The Space Shooter Game')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
font = pygame.font.SysFont('Arial', 32)

# Function to display text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to display the main menu
def main_menu():
    mixer.music.load('background.wav')
    mixer.music.play(-1)

    level_selected = None
    input_method = None

    while level_selected is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0, 0, 0))
        draw_text('Welcome To The Space Shooter Game', font, (255, 255, 255), 100, 200)
        draw_text('Choose a Level:', font, (255, 255, 255), 100, 300)
        draw_text('1 - Level 1', font, (255, 255, 255), 100, 350)
        draw_text('2 - Level 2 (Coming Soon)', font, (255, 255, 255), 100, 400)
        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            level_selected = 1
        elif keys[pygame.K_2]:
            # Add code for Level 2 if available
            pass

    while input_method is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0, 0, 0))
        draw_text('Choose Input Method:', font, (255, 255, 255), 100, 200)
        draw_text('1 - Keyboard', font, (255, 255, 255), 100, 350)
        draw_text('2 - Mouse', font, (255, 255, 255), 100, 400)
        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            input_method = 'keyboard'
        elif keys[pygame.K_2]:
            input_method = 'mouse'

    return level_selected, input_method

# Your game logic and functions here...
# Make sure to pass the selected level and input method to the game_loop function

# Main game loop
def game_loop(level, input_method):
    # Your game code here...
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
            explosion_sound = mixer.Sound('explosion.wav')      #sound overwrite nahos bhanera
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
        if score >= 50 and current_level == 1:
            current_level = 2
        level2_started = False
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
pass

if __name__ == '__main__':
    selected_level, selected_input = main_menu()
    game_loop(selected_level, selected_input)
