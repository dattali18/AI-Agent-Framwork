import pygame
import sys

from snake_game import SnakeGameAI
from flappy_bird import FlappyBirdGame
from ai_agent import Agent
from dino_game import DinoAI

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

GREEN = (31, 171, 41)
RED = (233, 34, 34)

BLUE = (80, 173, 248)
YELLOW = (255, 170, 41)

GREY = (85, 85, 85)
LIGHT_GREY = (246, 246, 246)

clock = pygame.time.Clock()
fps = 60


class UI:
    def __init__(self, width, height, title):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.font = pygame.font.Font(None, 32)  # Font for buttons
        self.caption_font = pygame.font.Font(None, 48)  # Font for the caption

        self.snake_icon = pygame.image.load("icons/snake-icon.png")
        self.flappy_icon = pygame.image.load("icons/flappy-icon.png")
        self.dino_icon = pygame.image.load("icons/dino-icon.png")

        self.corner_radius = 10

        self.buttons = []
        self.button_width = 100
        self.button_height = 35

    def draw_button(self, text, x, y, color, text_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_rect = pygame.Rect(x, y, self.button_width, self.button_height)
        pygame.draw.rect(self.screen, color, button_rect)

        if x <= mouse[0] <= x + self.button_width and y <= mouse[1] <= y + self.button_height:
            if click[0] and action is not None:

                action = action.split()
                game = None

                if action[1] == 'snake':
                    game = SnakeGameAI(main_window=main_window)
                elif action[1] == 'flappy':
                    game = FlappyBirdGame(main_window=main_window)
                elif action[1] == 'dino':
                    game = DinoAI(main_window=main_window)

                agent = Agent(game)
                if action[0] == 'train':
                    agent.train(model_path=f"{action[1]}/model_v2.pth")
                elif action[0] == 'play':
                    agent.play(model_path=f"{action[1]}/model_v1.pth")

        text_surface = self.font.render(text, True, text_color)
        text_width, text_height = text_surface.get_size()
        self.screen.blit(text_surface,
                         (x + (self.button_width - text_width) // 2, y + (self.button_height - text_height) // 2))

    def draw_group(self, icon, x, y, color1, color2, color3, color4, game: str):
        icon_rect = icon.get_rect(center=(x, y))
        self.screen.blit(icon, icon_rect)

        # Draw buttons with icons

        play_button_x = 100 + x
        play_button_y = y + 5

        self.draw_button("Play", play_button_x, play_button_y, color1, color2,
                         f"play {game}")

        train_button_x = play_button_x
        train_button_y = y - 35 - 5
        self.draw_button("Train", train_button_x, train_button_y, color3, color4,
                         f"train {game}")

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the screen with white
            self.screen.fill(WHITE)

            # Draw the caption
            caption_text = "Al Agent Game"
            caption_surface = self.caption_font.render(caption_text, True, BLACK)
            caption_rect = caption_surface.get_rect(center=(self.screen.get_width() // 2, 50))
            self.screen.blit(caption_surface, caption_rect)

            self.draw_group(self.snake_icon, 300, 200, GREEN, WHITE, RED, WHITE, "snake")
            self.draw_group(self.flappy_icon, 300, 350, BLUE, WHITE, YELLOW, WHITE, "flappy")
            self.draw_group(self.dino_icon, 300, 500, GREY, WHITE, LIGHT_GREY, BLACK, "dino")

            # Update the display
            pygame.display.flip()

            clock.tick(fps)

        # Quit Pygame
        pygame.quit()
        sys.exit()


def main_window():
    # Create and run the UI
    ui = UI(800, 600, "AI Agent Game")
    ui.main_loop()


if __name__ == "__main__":
    main_window()
