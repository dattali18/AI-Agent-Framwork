import pygame
import random
import numpy as np
from ai_agent.game import AIAgentGame

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


class Player(pygame.sprite.Sprite):
    """ This class represents the bird that the player controls. """

    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([30, 30])
        self.image.fill(YELLOW)

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

    def change_speed(self, x, y):
        """ Change the speed of the player. """
        self.change_x += x
        self.change_y += y

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
        self.change_y = -6

    def update(self):
        # Gravity
        self.calc_grav()

        """ Update the player position. """
        # Move left/right
        self.rect.x += self.change_x

        # Move up/down
        self.rect.y += self.change_y

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
            self.hit = True


class Pipe(pygame.sprite.Sprite):
    """ Pipe the player can fly into. """

    def __init__(self, x, y, width, height):
        """ Constructor for the pipe that the player can run into. """
        # Call the parent's constructor
        super().__init__()

        # Make a green pipe, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.top_image = pygame.Surface([width, SCREEN_HEIGHT - height - 50])
        self.top_image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.top_rect = self.top_image.get_rect()
        self.top_rect.y = 0
        self.top_rect.x = x

        self.change_x = 2

    def update(self):
        """ Update the pipe position. """
        self.rect.x -= self.change_x
        self.top_rect.x -= self.change_x


class FlappyBirdGame(AIAgentGame):
    def __init__(self):
        super().__init__(output_size=2, input_size=5)
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('FlappySquare')

        self.all_pipes = []
        self.pipe_count = 0
        self.reward = 0.
        self.done = False

        self.reset()

    def reset(self):
        self.all_pipes = []
        self.state = None
        self.pipe_count = 0
        self.all_sprite_list = pygame.sprite.Group()
        self.pipe_list = pygame.sprite.Group()
        self.player = Player(50, 300)

        self.pipe_count = 0

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
                pygame.quit()
                quit()

        # 2. move
        self.reward = 0
        self._move(action)

        if self.all_pipes[-1].rect.x <= random.randrange(50, 100, 2):
            self.pipe_creation()

        if self.all_pipes[self.pipe_count].rect.x + 70 <= self.player.rect.x:  # +70 -> pipe width
            self.player.score += 1
            self.pipe_count += 1
            self.reward += 10

        self.render()

        # 3. check if game over
        if not self.player.hit:
            done = False
            self.reward -= 10
        else:
            done = True
            self.reward += 1

        return self.reward, done, self.player.score

    def render(self, fps=120):
        self.all_sprite_list.update()
        self.screen.fill(LIGHTBLUE)
        self.all_sprite_list.draw(self.screen)
        self.text = self.font.render("Score: " + str(self.player.score), True, WHITE)
        self.screen.blit(self.text, [50, 50])

        pygame.display.flip()
        self.clock.tick(fps)

    def pipe_creation(self):
        self.pipe_hole = 200
        self.h = random.randrange(200, 700)
        self.pipe = Pipe(SCREEN_WIDTH, self.h, 70, SCREEN_HEIGHT - self.h)
        self.pipe_list.add(self.pipe)
        self.player.pipes = self.pipe_list
        self.all_sprite_list.add(self.pipe)

        self.all_pipes.append(self.pipe)

        self.pipe = Pipe(SCREEN_WIDTH, 0, 70, self.h - self.pipe_hole)
        self.pipe_list.add(self.pipe)
        self.player.pipes = self.pipe_list
        self.all_sprite_list.add(self.pipe)

    def get_state(self):
        """Get the current state of the environment."""
        player_x = self.player.rect.x
        player_y = self.player.rect.y
        pipe_x = self.all_pipes[self.pipe_count].rect.x + 70  # pipe x position + 70 (pipe width)
        pipe_y_bot = self.all_pipes[self.pipe_count].rect.y - player_y  # range to bot pipe
        pipe_y_top = pipe_y_bot - self.pipe_hole  # range to top pipe
        player_to_pipe_distance = pipe_x - player_x
        player_y_vel = self.player.change_y / 10

        return [player_y, player_to_pipe_distance, pipe_y_bot, pipe_y_top, player_y_vel]