import pygame
import random
import numpy as np

from ai_agent import AIAgentGame

import os

# Construct the absolute path to the image file
image_path = lambda name: os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'flappy_bird', 'assets', 'sprites', name))

# -- Global constants
# Colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
LIGHTBLUE = (0, 200, 255)
GREEN = (0, 150, 0)
YELLOW = (255, 200, 0)

# Screen dimensions
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 800

pygame.init()

# Before the Player class definition
bird_images = [
    pygame.image.load(image_path('yellowbird-downflap.png')),
    pygame.image.load(image_path('yellowbird-downflap.png')),
    pygame.image.load(image_path('yellowbird-midflap.png')),
]

background_image = pygame.image.load(image_path('background-day.png'))

pipe_images = pygame.image.load(image_path('pipe-green.png'))
pipe_images_top = pygame.image.load(image_path('pipe-green-top.png'))


class Player(pygame.sprite.Sprite):
    """ This class represents the bird that the player controls. """

    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        # self.image = pygame.Surface([30, 30])
        # self.image.fill(YELLOW)

        # Use one of the bird images for the player
        self.image = pygame.transform.scale(bird_images[0], (34, 24))
        self.current_image = 0

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.pipes = None

        self.score = 0

        # List of sprites we can bump against
        self.level = None
        self.hit = False

        self.distance = 0  # Add a new attribute for distance

    def change_speed(self, x, y):
        """ Change the speed of the player. """
        self.change_x += x
        self.change_y += y

        # self.current_image = (self.current_image + 1) % 3
        # self.image = bird_images[self.current_image]

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .20

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.hit = True
        elif self.rect.y <= 0:
            self.hit = True

    def jump(self):
        """ Called when user hits 'jump' button. """
        self.change_y = -3

    def update(self):
        # Gravity
        self.calc_grav()

        """ Update the player position. """
        # Move left/right
        self.rect.x += self.change_x

        # Move up/down
        self.rect.y += self.change_y

        # Update distance traveled
        self.distance += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.pipes, False)
        for block in block_hit_list:

            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
            self.rect.y = 50
            self.rect.x = 50
            self.score = 0
            self.distance = 0
            self.hit = True


class Pipe(pygame.sprite.Sprite):
    """ Pipe the player can fly into. """

    def __init__(self, x, y, width, height, top: bool):
        """ Constructor for the pipe that the player can run into. """
        # Call the parent's constructor
        super().__init__()

        # Make a green pipe, of the size specified in the parameters
        # self.image = pygame.Surface([width, height])
        # self.image.fill(GREEN)

        image = None

        if top:
            image = pygame.transform.scale(pipe_images_top, (width, height))
        else:
            image = pygame.transform.scale(pipe_images, (width, height))

        self.image = image
        # self.top_image = pygame.Surface([width, SCREEN_HEIGHT - height - 50])
        # self.top_image.fill(GREEN)

        # self.top_image = pygame.transform.scale(pipe_images_top, (width, SCREEN_HEIGHT - height - 50))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # self.top_rect = self.top_image.get_rect()
        # self.top_rect.y = 0
        # self.top_rect.x = x

        self.change_x = 2

    def update(self):
        """ Update the pipe position. """
        self.rect.x -= self.change_x
        # self.top_rect.x -= self.change_x


class FlappyBirdGame(AIAgentGame):
    def __init__(self, main_window=None):
        super().__init__(output_size=2, input_size=6, main_window=main_window)

        self.distance = 0
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('FlappySquare')

        self.background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.all_pipes = []
        self.pipe_count = 0
        self.reward = 0.
        self.done = False
        self.clock = None
        self.font = None
        self.player = None
        self.pipe_list = None
        self.all_sprite_list = None
        self.state = None
        self.text = None
        self.pipe_hole = None
        self.h = None
        self.pipe = None

        self.reset()

    def reset(self):
        self.all_pipes = []
        self.state = None
        self.pipe_count = 0
        self.all_sprite_list = pygame.sprite.Group()
        self.pipe_list = pygame.sprite.Group()
        self.player = Player(50, 300)

        self.pipe_count = 0
        self.distance = 0

        self.all_sprite_list.add(self.player)

        self.pipe_creation()

        self.font = pygame.font.SysFont('Calibri', 25, True, False)

        self.clock = pygame.time.Clock()

    def _move(self, action):

        # print(f"action: {action}")
        max_index = np.array(action).argmax()

        if max_index == 0:
            self.player.jump()

        self.all_sprite_list.update()

    def play_step(self, action):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.main_window is not None:
                    self.main_window()
                # else:
                #     pygame.quit()
                #     quit()
                pygame.quit()
                quit()

        # 2. move
        self.reward = 0
        self._move(action)

        if self.all_pipes[-1].rect.x <= random.randrange(50, 100, 2):
            self.pipe_creation()

        # Reward for survival (being alive)
        self.reward = 1
        self.distance += 1

        self.render()

        # 3. check if game over
        if not self.player.hit:
            done = False
        else:
            done = True
            # self.distance = 0
            self.reward = -10  # Penalty for hitting an obstacle

        # 4.

        if self.all_pipes[self.pipe_count].rect.x + 70 <= self.player.rect.x:  # +70 -> pipe width
            self.player.score += 1
            self.pipe_count += 1
            self.reward = 10  # Reward for passing a pipe

        return self.reward, done, self.distance

    def render(self, fps=60):
        self.all_sprite_list.update()
        # self.screen.fill(LIGHTBLUE)
        self.screen.blit(self.background, (0, 0))
        self.all_sprite_list.draw(self.screen)
        # self.text = self.font.render("Score: " + str(self.player.score), True, WHITE)
        # self.screen.blit(self.text, [50, 50])
        self.text = self.font.render(f"Pipes: {self.player.score} Distance: {self.distance}", True, WHITE)
        self.screen.blit(self.text, [50, 50])

        pygame.display.flip()
        self.clock.tick(fps)

    def pipe_creation(self):
        self.pipe_hole = 200
        self.h = random.randrange(200, 700)

        self.pipe = Pipe(SCREEN_WIDTH, self.h, 70, SCREEN_HEIGHT - self.h, False)
        self.pipe_list.add(self.pipe)
        self.player.pipes = self.pipe_list
        self.all_sprite_list.add(self.pipe)

        self.all_pipes.append(self.pipe)

        self.pipe = Pipe(SCREEN_WIDTH, 0, 70, self.h - self.pipe_hole, True)
        self.pipe_list.add(self.pipe)
        self.player.pipes = self.pipe_list
        self.all_sprite_list.add(self.pipe)

    def get_state(self):
        """Get the current state of the environment."""
        player_x = self.player.rect.x
        player_y = self.player.rect.y

        pipe_x = self.all_pipes[self.pipe_count].rect.x + 70  # pipe x position + 70 (pipe width)

        pipe_y_bot = self.all_pipes[self.pipe_count].rect.y - player_y  # range to bottom pipe
        pipe_y_top = pipe_y_bot - self.pipe_hole  # range to top pipe

        player_to_pipe_distance = pipe_x - player_x
        player_y_vel = self.player.change_y

        state = [player_y, pipe_x, pipe_y_bot, pipe_y_top, player_to_pipe_distance, player_y_vel]

        x = np.array(state, dtype=float)
        return (x - np.min(x)) / (np.max(x) - np.min(x))
