import pygame
import random

pygame.init()

# Set up the screen
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 50)
BLACK = (0, 0, 0)

# Load images (make sure these files exist)
player1_image = pygame.image.load('spaceinv_c.png')
player2_image = pygame.image.load('spaceinv.png')
powerup_image = pygame.image.load('Powerup.png')
player_width, player_height = 100, 60
player1_image = pygame.transform.scale(player1_image, (player_width, player_height))
player2_image = pygame.transform.scale(player2_image, (player_width, player_height))

enemy_image = pygame.image.load('Enemy.png')
enemy_width, enemy_height = 170, 110
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))

# Player attributes
player_speed = 7
player1_rect = player1_image.get_rect()
player2_rect = player2_image.get_rect()
player1_rect.center = (screen_width // 4, screen_height // 2)
player2_rect.center = (3 * screen_width // 4, screen_height // 2)

# Enemy attributes
enemy_speed = 5
enemy_direction = random.choice([-1, 1])
enemy_rect = enemy_image.get_rect()
enemy_rect.center = (random.randint(enemy_width // 2, screen_width - enemy_width // 2), 50)

# Bullet attributes
bullet_speed = 10
player1_bullets = []  # move right
player2_bullets = []  # move left
enemy_bullets = []    # move down
enemy_bullet_timer = random.randint(50, 150)  # initial cooldown

# Health attributes
player1_health = 100
player2_health = 100

# Player shooting cooldown time (in milliseconds)
shoot_cooldown = 4000

# Variables to keep track of the last shoot time for each player
player1_last_shot_time = -shoot_cooldown
player2_last_shot_time = -shoot_cooldown

# Ball attributes
ball_radius = 20
ball_x = random.randint(ball_radius, screen_width - ball_radius)
ball_y = random.randint(ball_radius, screen_height - ball_radius)
ball_speed_x = random.choice([-5, 5])
ball_speed_y = random.choice([-5, 5])

# Function to draw health bars
def draw_health_bars():
    # Draw player 1 health bar (clamped to 0..100 for width)
    p1_w = max(0, min(100, player1_health))
    pygame.draw.rect(screen, RED, (10, 10, p1_w * 2, 25))  # *2 to make it visible
    # Draw player 2 health bar
    p2_w = max(0, min(100, player2_health))
    pygame.draw.rect(screen, BLUE, (screen_width - (p2_w * 2) - 10, 10, p2_w * 2, 25))

# Function to display game over message
def game_over(winner):
    font = pygame.font.Font(None, 60)
    if winner == "Player 1":
        text = font.render("Player 1 wins! Game Over!", True, RED)
    else:
        text = font.render("Player 2 wins! Game Over!", True, BLUE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # Cap the frame rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Player 1 controls
    if keys[pygame.K_w]:
        player1_rect.y = max(player1_rect.y - player_speed, 0)
    if keys[pygame.K_s]:
        player1_rect.y = min(player1_rect.y + player_speed, screen_height - player1_rect.height)
    if keys[pygame.K_a]:
        player1_rect.x = max(player1_rect.x - player_speed, 0)
    if keys[pygame.K_d]:
        player1_rect.x = min(player1_rect.x + player_speed, screen_width // 2 - player1_rect.width)

    # Player 2 controls
    if keys[pygame.K_UP]:
        player2_rect.y = max(player2_rect.y - player_speed, 0)
    if keys[pygame.K_DOWN]:
        player2_rect.y = min(player2_rect.y + player_speed, screen_height - player2_rect.height)
    if keys[pygame.K_LEFT]:
        player2_rect.x = max(player2_rect.x - player_speed, screen_width // 2)
    if keys[pygame.K_RIGHT]:
        player2_rect.x = min(player2_rect.x + player_speed, screen_width - player2_rect.width)

    # Player 1 shooting (right)
    if keys[pygame.K_v] and pygame.time.get_ticks() - player1_last_shot_time >= shoot_cooldown:
        # Create bullet at right side of player1
        b_rect = pygame.Rect(player1_rect.right, player1_rect.centery - 2, 12, 4)
        player1_bullets.append(b_rect)
        player1_last_shot_time = pygame.time.get_ticks()

    # Player 2 shooting (left)
    if keys[pygame.K_RETURN] and pygame.time.get_ticks() - player2_last_shot_time >= shoot_cooldown:
        b_rect = pygame.Rect(player2_rect.left - 12, player2_rect.centery - 2, 12, 4)
        player2_bullets.append(b_rect)
        player2_last_shot_time = pygame.time.get_ticks()

    # Enemy movement
    enemy_rect.x += enemy_speed * enemy_direction
    # Reverse enemy direction if it reaches screen boundaries (respecting sprite edges)
    if enemy_rect.left <= 0:
        enemy_rect.left = 0
        enemy_direction = 1
    elif enemy_rect.right >= screen_width:
        enemy_rect.right = screen_width
        enemy_direction = -1

    # Enemy shooting logic (timer decreases each frame)
    if enemy_bullet_timer <= 0:
        enemy_bullet = pygame.Rect(enemy_rect.centerx - 5, enemy_rect.bottom, 10, 20)
        enemy_bullets.append(enemy_bullet)
        enemy_bullet_timer = random.randint(50, 150)
    else:
        # decrease timer each frame (scaled to feel proper)
        enemy_bullet_timer -= 1

    # Move bullets and remove off-screen bullets safely by building new lists
    new_p1_bullets = []
    for b in player1_bullets:
        b = b.move(bullet_speed, 0)  # move right
        if b.left < screen_width:
            new_p1_bullets.append(b)
    player1_bullets = new_p1_bullets

    new_p2_bullets = []
    for b in player2_bullets:
        b = b.move(-bullet_speed, 0)  # move left
        if b.right > 0:
            new_p2_bullets.append(b)
    player2_bullets = new_p2_bullets

    new_enemy_bullets = []
    for b in enemy_bullets:
        b = b.move(0, bullet_speed)  # move down
        if b.top < screen_height:
            new_enemy_bullets.append(b)
    enemy_bullets = new_enemy_bullets

    # Collision detection - iterate over copies to avoid modifying lists while iterating
    # Enemy bullets hit player2
    for b in enemy_bullets[:]:
        if player2_rect.colliderect(b):
            player2_health -= 10
            if b in enemy_bullets:
                enemy_bullets.remove(b)

    # Enemy bullets hit player1
    for b in enemy_bullets[:]:
        if player1_rect.colliderect(b):
            player1_health -= 10
            if b in enemy_bullets:
                enemy_bullets.remove(b)

    # Player1 bullets hit player2
    for b in player1_bullets[:]:
        if player2_rect.colliderect(b):
            player2_health -= 25
            if b in player1_bullets:
                player1_bullets.remove(b)

    # Player2 bullets hit player1
    for b in player2_bullets[:]:
        if player1_rect.colliderect(b):
            player1_health -= 25
            if b in player2_bullets:
                player2_bullets.remove(b)

    # Check for win condition
    if player1_health <= 0:
        game_over("Player 2")
        break
    elif player2_health <= 0:
        game_over("Player 1")
        break

    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Bounce the ball off the screen edges
    if ball_x <= ball_radius or ball_x >= screen_width - ball_radius:
        ball_speed_x = -ball_speed_x
        ball_x = max(ball_radius, min(ball_x, screen_width - ball_radius))
    if ball_y <= ball_radius or ball_y >= screen_height - ball_radius:
        ball_speed_y = -ball_speed_y
        ball_y = max(ball_radius, min(ball_y, screen_height - ball_radius))

    # Clear the screen
    screen.fill(BLACK)

    # Blit player images onto the screen
    screen.blit(player1_image, player1_rect)
    screen.blit(player2_image, player2_rect)
    screen.blit(enemy_image, enemy_rect)

    # Draw the bouncing yellow ball (cast positions to int)
    pygame.draw.circle(screen, YELLOW, (int(ball_x), int(ball_y)), ball_radius)

    # Draw bullets
    for bullet in player1_bullets:
        pygame.draw.rect(screen, RED, bullet)
    for bullet in player2_bullets:
        pygame.draw.rect(screen, BLUE, bullet)
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

    # Draw health bars
    draw_health_bars()

    # Calculate and display cooldown text
    current_time = pygame.time.get_ticks()
    player1_cooldown_remaining = max(0, shoot_cooldown - (current_time - player1_last_shot_time))
    player2_cooldown_remaining = max(0, shoot_cooldown - (current_time - player2_last_shot_time))

    player1_cooldown_seconds = player1_cooldown_remaining // 1000
    player2_cooldown_seconds = player2_cooldown_remaining // 1000

    font = pygame.font.Font(None, 37)
    player1_cooldown_text = font.render(f"P1 Cooldown: {player1_cooldown_seconds} s", True, WHITE)
    player2_cooldown_text = font.render(f"P2 Cooldown: {player2_cooldown_seconds} s", True, WHITE)
    screen.blit(player1_cooldown_text, (10, screen_height - 650))
    screen.blit(player2_cooldown_text, (screen_width - 250, screen_height - 650))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
