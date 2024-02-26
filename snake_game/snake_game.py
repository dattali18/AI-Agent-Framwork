import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
from typing import List, Tuple

from ai_agent import AIAgentGame



pygame.init()


# font = pygame.font.Font('arial.ttf', 25)


font = pygame.font.SysFont('arial', 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
WHITE2 = (217, 217, 217)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GREEN1 = (9, 58, 6)
GREEN2 = (31, 133, 28)

BLOCK_SIZE = 20
SPEED = 60


class SnakeGameAI(AIAgentGame):

    def __init__(self, w=640, h=480, main_window=None):
        super().__init__(input_size=11, output_size=3, main_window=main_window)

        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init values
        self.direction = None
        self.frame_iteration = None
        self.food = None
        self.score = None
        self.snake = None
        self.head = None

        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        # Draw white grid lines
        for x in range(0, self.w, BLOCK_SIZE):
            pygame.draw.line(self.display, WHITE2, (x, 0), (x, self.h))
        for y in range(0, self.h, BLOCK_SIZE):
            pygame.draw.line(self.display, WHITE2, (0, y), (self.w, y))

        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pt = self.snake[0]
        pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    # implementing the interface

    def get_state(self):
        head = self.snake[0]

        # Move direction
        dir_l = self.direction == Direction.LEFT
        dir_r = self.direction == Direction.RIGHT
        dir_u = self.direction == Direction.UP
        dir_d = self.direction == Direction.DOWN

        dir_x = (dir_r - dir_l)
        dir_y = (dir_u - dir_d)

        # Calculate Manhattan distance to food
        distance_to_food = abs(self.food.x - head.x) + abs(self.food.y - head.y)

        # Direction to food
        food_left = self.food.x < head.x
        food_right = self.food.x > head.x
        food_up = self.food.y < head.y
        food_down = self.food.y > head.y

        food_x = (food_left - food_right)
        food_y = (food_up - food_down)

        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        # Obstacle proximity indicators
        obstacle_left = self.is_collision(Point(head.x - BLOCK_SIZE, head.y))
        obstacle_right = self.is_collision(Point(head.x + BLOCK_SIZE, head.y))
        obstacle_up = self.is_collision(Point(head.x, head.y - BLOCK_SIZE))
        obstacle_down = self.is_collision(Point(head.x, head.y + BLOCK_SIZE))

        # Body proximity indicators
        body_left = any(Point(head.x - BLOCK_SIZE, head.y) == segment for segment in self.snake[1:])
        body_right = any(Point(head.x + BLOCK_SIZE, head.y) == segment for segment in self.snake[1:])
        body_up = any(Point(head.x, head.y - BLOCK_SIZE) == segment for segment in self.snake[1:])
        body_down = any(Point(head.x, head.y + BLOCK_SIZE) == segment for segment in self.snake[1:])

        danger_straight = ((dir_r and self.is_collision(point_r)) or
                           (dir_l and self.is_collision(point_l)) or
                           (dir_u and self.is_collision(point_u)) or
                           (dir_d and self.is_collision(point_d)))
        danger_right = ((dir_u and self.is_collision(point_r)) or
                        (dir_d and self.is_collision(point_l)) or
                        (dir_l and self.is_collision(point_u)) or
                        (dir_r and self.is_collision(point_d)))
        danger_left = ((dir_d and self.is_collision(point_r)) or
                       (dir_u and self.is_collision(point_l)) or
                       (dir_r and self.is_collision(point_u)) or
                       (dir_l and self.is_collision(point_d)))

        # Snake length
        snake_length = len(self.snake)

        state = [
            # Danger
            danger_straight, danger_right, danger_left,
            # Move direction
            dir_l, dir_r, dir_u, dir_d,
            # dir_x, dir_y,
            # Direction to food
            # food_x, food_y,
            food_left, food_right, food_up, food_down,
            # Calculate Manhattan distance to food
            # distance_to_food,
            # Snake length
            # snake_length,
            # Body proximity indicators
            # body_left, body_right, body_up, body_down,
            # Obstacle proximity indicators
            # obstacle_left, obstacle_right, obstacle_up, obstacle_down,
        ]

        return state

    def play_step(self, action: List[int]) -> Tuple[int, bool, int]:
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.main_window is not None:
                    self.main_window()
            #     else:
            #         pygame.quit()
            #         quit()
                pygame.quit()
                quit()

        # 2. move
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score
