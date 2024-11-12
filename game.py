import pygame
import random

# Initialize the game
pygame.init()

# set screen's size
screen_width = 800
screen_height = 600

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the player
player = pygame.Rect(50, 50, 50, 50)

# set up the fruit
fruit = pygame.Rect(200, 200, 50, 50)

# Set up the player's tail
tail = [pygame.Rect(player.x - 50, player.y, 50, 50)]

# Set up the clock
clock = pygame.time.Clock()

#set up the player's movement
player_dx, player_dy = 0, 0

# Set up the end game
def end_game():
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2)
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()

# Set up the player's tail movement
def move_tail():
    if len(tail) > 0:
        for i in range(len(tail) - 1, 0, -1):
            tail[i] = (tail[i - 1][0], tail[i - 1][1])
        tail[0] = (tail[0][0] + player_dx, tail[0][1] + player_dy)

# Set up the player's movement
def move_player():
    player_speed = 5
    global player_dx, player_dy
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_dx = -player_speed
        player_dy = 0
    if keys[pygame.K_RIGHT]:
        player_dx = player_speed
        player_dy = 0
    if keys[pygame.K_UP]:
        player_dy = -player_speed
        player_dx = 0
    if keys[pygame.K_DOWN]:
        player_dy = player_speed
        player_dx = 0
    player.x += player_dx
    player.y += player_dy

# set up the fruit's position
def position_fruit():
    fruit.x = random.randint(0, screen_width - 50)
    fruit.y = random.randint(0, screen_height - 50)

def colisions_player():
    if player.x < 0:
        player.x = 0
        end_game()
    if player.x > screen_width - player.width:
        player.x = screen_width - player.width
        end_game()
    if player.y < 0:
        player.y = 0
        end_game()
    if player.y > screen_height - player.height:
        player.y = screen_height - player.height
        end_game()
    if player.colliderect(fruit):
        position_fruit()

# Draw all the objects
def draw_object():
    pygame.draw.rect(screen, RED, fruit)
    pygame.draw.rect(screen, WHITE, player)
    for i in tail:
        pygame.draw.rect(screen, GREEN, (i[0], i[1], 50, 50))
    pygame.display.flip()

# Run the game
def main():
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        move_player()
        move_tail()
        colisions_player()
        draw_object()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
