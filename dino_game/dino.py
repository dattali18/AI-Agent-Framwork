import pygame
import os
import random

import numpy as np
from ai_agent import AIAgentGame, Agent

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100

FLOOR = 300

# SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

fps = 30

image_path = lambda name: os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'dino_game', 'assets', name))

RUNNING = [
    pygame.image.load(image_path("Dino/DinoRun1.png")),
    pygame.image.load(image_path("Dino/DinoRun2.png")),
]

JUMPING = pygame.image.load(image_path("Dino/DinoJump.png"))

DUCKING = [
    pygame.image.load(image_path("Dino/DinoDuck1.png")),
    pygame.image.load(image_path("Dino/DinoDuck2.png")),
]

SMALL_CACTUS = [
    pygame.image.load(image_path("Cactus/SmallCactus1.png")),
    pygame.image.load(image_path("Cactus/SmallCactus2.png")),
    pygame.image.load(image_path("Cactus/SmallCactus3.png")),
]

LARGE_CACTUS = [
    pygame.image.load(image_path("Cactus/LargeCactus1.png")),
    pygame.image.load(image_path("Cactus/LargeCactus2.png")),
    pygame.image.load(image_path("Cactus/LargeCactus3.png")),
]

BIRD = [
    pygame.image.load(image_path("Bird/Bird1.png")),
    pygame.image.load(image_path("Bird/Bird2.png")),
]

BG = pygame.image.load(image_path("Other/Track.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.step_index = 0

        self.image = self.run_img[0]

        self.dino_rect = self.image.get_rect()

        self.dino_rect.y = self.Y_POS
        self.dino_rect.x = 80

        self.dy = 0
        self.gravity = 1.5
        self.is_jumping = False

        self.image_idx = 0

    def update(self, action):
        action = action.index(1)

        if action == 0:
            self.jump()

        self.dy += self.gravity
        self.dino_rect.y += self.dy

        # checking if the dino is on the floor
        if self.dino_rect.y > SCREEN_HEIGHT - FLOOR:
            self.dino_rect.y = SCREEN_HEIGHT - FLOOR
            self.dy = 0
            self.is_jumping = False
            self.image_idx = (self.image_idx + 1) % len(self.run_img)
            self.image = self.run_img[self.image_idx]

    def jump(self):
        if not self.is_jumping:
            self.image = self.jump_img
            self.is_jumping = True
            self.dy = -28

    # Draw the dinosaur
    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Obstacle:
    # This is the parent class for all the
    def __init__(self, image, type_, game_speed, obstacles):
        self.image = image
        self.type = type_
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.game_speed = game_speed
        self.obstacles = obstacles

    # This is the update method for the obstacles
    # if the obstacle is off the screen, it will be removed from the list
    # and if the obstacle is on the screen, it will be moved to the left
    def update(self):
        self.rect.x -= self.game_speed
        if self.rect.x < -self.rect.width:
            self.obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)


# This is the class for the small cactus
class SmallCactus(Obstacle):
    def __init__(self, image, game_speed, obstacles):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type, game_speed, obstacles)
        self.rect.y = 325
        self.width = self.image[self.type].get_width()
        self.height = self.image[self.type].get_height()


class LargeCactus(Obstacle):
    def __init__(self, image, game_speed, obstacles):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type, game_speed, obstacles)
        self.rect.y = 300
        self.width = self.image[self.type].get_width()
        self.height = self.image[self.type].get_height()


class Bird(Obstacle):
    def __init__(self, image, game_speed, obstacles):
        self.type = 0
        super().__init__(image, self.type, game_speed, obstacles)
        self.rect.y = 180
        self.index = 0
        self.width = self.image[self.type].get_width()
        self.height = self.image[self.type].get_height()

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1


class DinoAI(AIAgentGame):
    def __init__(self, main_window=None):
        super().__init__(input_size=6, output_size=2, main_window=main_window)
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.game_speed = 15
        self.x_pos_bg = 0
        self.y_pos_bg = FLOOR + 80
        self.points = 0
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.obstacles = []
        self.death_count = 0
        self.player = Dinosaur()

    def reset(self):
        self.clock.tick(fps // 10)

        self.game_speed = 15
        self.x_pos_bg = 0
        self.y_pos_bg = FLOOR + 80
        self.points = 0
        self.obstacles = []
        self.death_count = 0

    def get_state(self):
        """
        Get the current state of the Dino game environment.
        """

        """
        state = [
            player_y,
            enemy_x,
            enemy_height,
            enemy_width
        ]
        """

        dino_x, dino_y = self.player.dino_rect.x, self.player.dino_rect.y
        obstacle_x, obstacle_y = 0, 0
        #obstacle_type = 0
        distance_to_obstacle = 0
        #dino_y_velocity = 0
        obstacle_width = 0
        obstacle_height = 0

        if len(self.obstacles) > 0:
            obstacle_x = self.obstacles[0].rect.x
            obstacle_y = self.obstacles[0].rect.y
            #obstacle_type = self.obstacles[0].type
            distance_to_obstacle = obstacle_x - dino_x
            #dino_y_velocity = self.player.dy
            obstacle_width = self.obstacles[0].width
            obstacle_height = self.obstacles[0].height


        # Normalize state values
        #state = [dino_x, dino_y, obstacle_x, obstacle_y, obstacle_type, distance_to_obstacle, dino_y_velocity]
        state = [dino_y, obstacle_x, obstacle_y, distance_to_obstacle, obstacle_width, obstacle_height]
        state = np.array(state, dtype=float)
        return (state - np.min(state)) / (np.max(state) - np.min(state))

    def play_step(self, action):
        """
        Take an action in the Dino game environment.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.main_window is not None:
                    self.main_window()
                pygame.quit()
                quit()

        reward = 0
        game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        self.player.update(action)

        self.screen.fill((255, 255, 255))
        self.player.draw(self.screen)

        # This is where the obstacles are created
        if len(self.obstacles) == 0:
            if random.randint(0, 2) == 0:
                self.obstacles.append(SmallCactus(SMALL_CACTUS, self.game_speed, self.obstacles))
            elif random.randint(0, 2) == 1:
                self.obstacles.append(LargeCactus(LARGE_CACTUS, self.game_speed, self.obstacles))
            elif random.randint(0, 2) == 2:
                self.obstacles.append(Bird(BIRD, self.game_speed, self.obstacles))

        # This is where the obstacles are drawn and updated
        # If the player collides with an obstacle, the game is over
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
            obstacle.update()
            if self.player.dino_rect.colliderect(obstacle.rect):
                reward = -1
                game_over = True
            else:
                reward += 1

        self.background()
        self.score()

        self.clock.tick(fps)
        pygame.display.update()

        return reward, game_over, self.points

    def background(self):
        """
        Scroll the background image.
        """
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def score(self):
        """
        Display the current score.
        """
        self.points += 1

        if self.points % 100 == 0:
            self.game_speed += 1

        text = self.font.render("Points: " + str(self.points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        self.screen.blit(text, textRect)


if __name__ == "__main__":
    dino_ai = DinoAI()
    agent = Agent(dino_ai)
    agent.train("model_v1.0.pth", training=True)
