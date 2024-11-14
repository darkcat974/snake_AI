import pygame
import random

# Initialize the game
pygame.init()

# set screen's size
screen_width = 800
screen_height = 800

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the player
player = pygame.Rect(screen_width / 20, screen_height / 20, screen_width / 20, screen_height / 20)

# set up the fruit
fruit = pygame.Rect(200, 200, screen_width / 20, screen_height / 20)

# Set up the player's tail
tail = [pygame.Rect(player.x - screen_width / 20, player.y, screen_width / 20, screen_height / 20)]

# Set up the clock
clock = pygame.time.Clock()

# set up the player's movement
player_dx, player_dy = 0, 0
block_size = screen_width / 20

# set up the player's tail movement
tail_dx, tail_dy = player_dx, player_dy

# Set up the end game
def end_game():
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2)
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(1500)
    pygame.quit()

# add a new block to the player's tail
def add_tail():
    tail.append(pygame.Rect(tail[-1].x, tail[-1].y, 50, 50))

# Set up the player's tail movement
def move_tail():
    if len(tail) > 0:
        for i in range(len(tail) - 1, 0, -1):
            tail[i] = tail[i - 1].copy()
        tail[0].x = player.x - player_dx
        tail[0].y = player.y - player_dy

# Set up the player's movement
def move_player():
    global player_dx, player_dy, tail_dx, tail_dy
    tail_dx, tail_dy = player_dx, player_dy
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player_dx <= 0:
            player_dx = -block_size
            player_dy = 0
    if keys[pygame.K_RIGHT]:
        if player_dx >= 0:
            player_dx = block_size
            player_dy = 0
    if keys[pygame.K_UP]:
        if player_dy >= 0:
            player_dy = -block_size
            player_dx = 0
    if keys[pygame.K_DOWN]:
        if player_dy <= 0:
            player_dy = block_size
            player_dx = 0
    player.x += player_dx
    player.y += player_dy

# set up the fruit's position
def position_fruit():
    fruit_col = screen_width // block_size
    fruit_row = screen_height // block_size
    fruit.x = random.randint(1, fruit_col - 1) * block_size
    fruit.y = random.randint(1, fruit_row - 1) * block_size
    print(fruit_col, fruit_row)

# set up the colisions with the tail
def colisions_tail():
    for i in tail[1:]:
        if player.x == i.x and player.y == i.y:
            end_game()

# set up the colisions with the fruit
def colisions_fruit():
    if player.colliderect(fruit):
        position_fruit()
        add_tail()

# Set up the colisions with the walls
def colisions_wall():
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

def colisions_player():
    colisions_wall()
    colisions_fruit()
    colisions_tail()

# Draw all the objects
def draw_object():
    pygame.draw.rect(screen, RED, fruit)
    pygame.draw.rect(screen, WHITE, player)
    for i in tail:
        pygame.draw.rect(screen, GREEN, i)
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
        clock.tick(6)
    pygame.quit()

if __name__ == "__main__":
    main()