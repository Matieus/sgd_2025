import pygame
from ui.button import Button
from const import Colors, Settings


class PauseMenu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.overlay = pygame.Surface((Settings.WIDTH, Settings.HEIGHT))
        self.overlay.set_alpha(200)
        self.overlay.fill((0, 0, 0))

        self.font_title = pygame.font.SysFont("Arial", 48)
        self.title = self.font_title.render("PAUSE", True, Colors.WHITE.rgb)
        self.title_rect = self.title.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 150)
        )

        button_width = 200
        button_height = 60
        button_y_start = Settings.HEIGHT // 2 - 50

        self.buttons = {
            "continue": Button(
                pygame.Rect(
                    (Settings.WIDTH - button_width) // 2,
                    button_y_start,
                    button_width,
                    button_height,
                ),
                "Continue",
                Colors.GREEN,
            ),
            "main_menu": Button(
                pygame.Rect(
                    (Settings.WIDTH - button_width) // 2,
                    button_y_start + 80,
                    button_width,
                    button_height,
                ),
                "Main Menu",
                Colors.GRAY,
            ),
            "quit": Button(
                pygame.Rect(
                    (Settings.WIDTH - button_width) // 2,
                    button_y_start + 160,
                    button_width,
                    button_height,
                ),
                "Quit Game",
                Colors.RED,
            ),
        }

    def draw(self):
        self.screen.blit(self.overlay, (0, 0))
        self.screen.blit(self.title, self.title_rect)
        for button in self.buttons.values():
            button.draw(self.screen)
