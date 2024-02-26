import pygame
import sys

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


class Button:
    def __init__(self, text, x, y, width, height, normal_color, hover_color, click_color, text_color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.text_color = text_color
        self.action = action

        self.font = pygame.font.Font(None, 36)
        self.clicked = False

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]

        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            pygame.draw.rect(surface, self.hover_color, (self.x, self.y, self.width, self.height))
            if clicked and not self.clicked and self.action is not None:
                self.clicked = True
                self.action()
        else:
            pygame.draw.rect(surface, self.normal_color, (self.x, self.y, self.width, self.height))

        text_surface = self.font.render(self.text, True, self.text_color)
        text_width, text_height = text_surface.get_size()
        surface.blit(text_surface, (self.x + (self.width - text_width) // 2, self.y + (self.height - text_height) // 2))

    def reset(self):
        self.clicked = False


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

    def draw_button(self, text, x, y, width, height, color, text_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        pygame.draw.rect(self.screen, color, (x, y, width, height))

        if x <= mouse[0] <= x + width and y <= mouse[1] <= y + height:
            if click[0] and action is not None:
                action()

        text_surface = self.font.render(text, True, text_color)
        text_width, text_height = text_surface.get_size()
        self.screen.blit(text_surface, (x + (width - text_width) // 2, y + (height - text_height) // 2))

    def draw_group(self, icon, x, y, color1, color2, color3, color4):
        icon_rect = icon.get_rect(center=(x, y))
        self.screen.blit(icon, icon_rect)

        # Draw buttons with icons

        play_button_x = 100 + x
        play_button_y = y + 5

        self.draw_button("Play", play_button_x, play_button_y, 100, 35, color1, color2,
                         play_button_action)

        train_button_x = play_button_x
        train_button_y = y - 35 - 5
        self.draw_button("Train", train_button_x, train_button_y, 100, 35, color3, color4,
                         train_button_action)

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

            self.draw_group(self.snake_icon, 300, 200, GREEN, WHITE, RED, WHITE)
            self.draw_group(self.flappy_icon, 300, 350, BLUE, WHITE, YELLOW, WHITE)
            self.draw_group(self.dino_icon, 300, 500, GREY, WHITE, LIGHT_GREY, BLACK)

            # Update the display
            pygame.display.flip()

            clock.tick(fps)

        # Quit Pygame
        pygame.quit()
        sys.exit()


# Define the button actions (replace with your actual functionality)
def play_button_action():
    print("Play button clicked")


def train_button_action():
    print("Train button clicked")


if __name__ == "__main__":
    # Create and run the UI
    ui = UI(800, 600, "AI Agent Game")
    ui.main_loop()
