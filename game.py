import pygame
import random
from enum import Enum

# Initialize the game
pygame.init()

class Game:
    def __init__(self, w=800, h=800):
        # set screen's size
        self.screen_width = w
        self.screen_height = h
        # Set up the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # Set up the colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.reset()

    def reset(self):
        # Set up the player
        self.player = pygame.Rect(self.screen_width / 20, self.screen_height / 20, self.screen_width / 20, self.screen_height / 20)
        # set up the fruit
        self.fruit = pygame.Rect(200, 200, self.screen_width / 20, self.screen_height / 20)
        # Set up the player's tail
        self.tail = [pygame.Rect(self.screen_width / 20, self.player.y, self.screen_width / 20, self.screen_height / 20)]
        # Set up the clock
        self.clock = pygame.time.Clock()
        # set up the player's movement
        self.player_dx, self.player_dy = 0, 0
        self.block_size = self.screen_width / 20
        # set up the player's tail movement
        self.tail_dx, self.tail_dy = self.player_dx, self.player_dy
        # set up the player's score
        self.score = 0

    # Set up the end game
    def end_game(self):
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, self.WHITE)
        text_rect = text.get_rect()
        text_rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1500)
        self.reset()
        self.loop

    # add a new block to the player's tail
    def add_tail(self):
        self.tail.append(pygame.Rect(self.tail[-1].x, self.tail[-1].y, 50, 50))

    # Set up the player's tail movement
    def move_tail(self):
        if len(self.tail) > 0:
            for i in range(len(self.tail) - 1, 0, -1):
                self.tail[i] = self.tail[i - 1].copy()
            self.tail[0].x = self.player.x - self.player_dx
            self.tail[0].y = self.player.y - self.player_dy

    # Set up the player's movement
    def move_player(self, event=None):
        self.tail_dx, self.tail_dy = self.player_dx, self.player_dy
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.player_dx <= 0:
                    self.player_dx = -self.block_size
                    self.player_dy = 0
            elif event.key == pygame.K_RIGHT:
                if self.player_dx >= 0:
                    self.player_dx = self.block_size
                    self.player_dy = 0
            elif event.key == pygame.K_UP:
                if self.player_dy >= 0:
                    self.player_dy = -self.block_size
                    self.player_dx = 0
            elif event.key == pygame.K_DOWN:
                if self.player_dy <= 0:
                    self.player_dy = self.block_size
                    self.player_dx = 0
        self.player.x += self.player_dx
        self.player.y += self.player_dy

    # set up the fruit's position
    def position_fruit(self):
        fruit_col = self.screen_width // self.block_size
        fruit_row = self.screen_height // self.block_size
        self.fruit.x = random.randint(1, fruit_col - 1) * self.block_size
        self.fruit.y = random.randint(1, fruit_row - 1) * self.block_size
        for t in self.tail:
            if self.fruit.x == t.x and self.fruit.y == t.y:
                self.position_fruit()

    # set up the colisions with the tail
    def colisions_tail(self):
        for i in self.tail[1:]:
            if self.player.x == i.x and self.player.y == i.y:
                self.end_game()

    # set up the colisions with the fruit
    def colisions_fruit(self):
        if self.player.colliderect(self.fruit):
            self.position_fruit()
            self.add_tail()
            self.score += 1

    # Set up the colisions with the walls
    def colisions_wall(self):
        if self.player.x < 0:
            self.player.x = 0
            self.end_game()
        if self.player.x > self.screen_width - self.player.width:
            self.player.x = self.screen_width - self.player.width
            self.end_game()
        if self.player.y < 0:
            self.player.y = 0
            self.end_game()
        if self.player.y > self.screen_height - self.player.height:
            self.player.y = self.screen_height - self.player.height
            self.end_game()

    # call all the colision's functions related to the player
    def colisions_player(self):
        self.colisions_wall()
        self.colisions_fruit()
        self.colisions_tail()

    # Draw the player's score
    def draw_score(self):
        pygame.font.init()
        font = pygame.font.Font(None, int(self.block_size))
        text = font.render(f"Score : {self.score}", True, self.WHITE)
        text_rect = text.get_rect()
        text_rect.center = (self.screen_width // 2, self.screen_height // int(self.block_size))
        self.screen.blit(text, text_rect)

    # Draw all the objects
    def draw_object(self):
        pygame.draw.rect(self.screen, self.RED, self.fruit)
        pygame.draw.rect(self.screen, self.WHITE, self.player)
        for i in self.tail:
            pygame.draw.rect(self.screen, self.GREEN, i)
        self.draw_score()
        pygame.display.flip()

    def player_interactions(self, event):
        self.move_player(event)
        self.move_tail()
        self.colisions_player()

    # Run the game
    def loop(self):
        running = True
        while running:
            self.screen.fill(self.BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return
            self.player_interactions(event)
            self.draw_object()
            self.clock.tick(10)

if __name__ == "__main__":
    game = Game()
    game.loop()
