import sys

import pygame

from const import Colors, PinsMap, Settings
from ui.button import Button


class Menu:
    def __init__(self):
        self.heart_image = pygame.image.load("assets/heart32.png").convert_alpha()
        self.heart_size = 32

        self.current_map_index = 0
        self.current_lives_index = 0
        self.current_map = list(PinsMap)[self.current_map_index]
        self.lives_options: list[int | None] = [3, 5, None]
        self.current_lives = self.lives_options[self.current_lives_index]

        self.map_button = Button(
            pygame.Rect(Settings.WIDTH // 2 - 100, 340, 200, 50),
            f"{self.current_map.name}",
        )
        self.lives_button = Button(
            pygame.Rect(Settings.WIDTH // 2 - 100, 270, 200, 50), "", color=Colors.PINK
        )

        self.play = Button(
            pygame.Rect(Settings.WIDTH // 2 - 100, 200, 200, 50),
            "Play",
        )
        self.exit = Button(
            pygame.Rect(Settings.WIDTH // 2 - 100, 410, 200, 50),
            "Exit",
        )

        self.current_player_count_index = 0
        self.max_players = 3
        self.player_icon_radius = 12
        self.player_icon_spacing = 15

        self.players_button = Button(
            pygame.Rect(Settings.WIDTH // 2 - 100, 480, 200, 50),
            "",
        )

    def draw(self, surface: pygame.Surface):
        surface.fill(Colors.BLACK.rgb)
        self.play.draw(surface)
        self.exit.draw(surface)
        self.draw_lives(surface)
        self.map_button.draw(surface)
        self.draw_players_icons(surface)

    def draw_lives(self, surface: pygame.Surface):
        self.current_lives = self.lives_options[self.current_lives_index]
        self.lives_button.draw(surface)

        rect = self.lives_button.rect
        top_offset = (rect.height - self.heart_size) // 2

        if self.current_lives is None:
            font = pygame.font.SysFont("Arial", 84)
            infinity = font.render("∞", True, Colors.BLACK.rgb)
            surface.blit(
                infinity,
                (
                    rect.centerx - infinity.get_width() // 2,
                    rect.top + (rect.height - infinity.get_height()) // 2,
                ),
            )
        else:
            total_width = self.current_lives * self.heart_size
            start_x = rect.centerx - total_width // 2

            for i in range(self.current_lives):
                pos_x = start_x + i * self.heart_size
                pos_y = rect.top + top_offset
                surface.blit(self.heart_image, (pos_x, pos_y))

    def draw_players_icons(self, surface: pygame.Surface):
        x, y = self.players_button.rect.topleft
        num_players = self.current_player_count_index + 1

        center_x = x + self.players_button.rect.width // 2
        start_x = (
            center_x
            - (
                (num_players - 1)
                * (self.player_icon_radius * 2 + self.player_icon_spacing)
            )
            // 2
        )
        icon_y = y + self.players_button.rect.height // 2

        for i in range(num_players):
            _player = Settings.players[i]
            circle_x = start_x + i * (
                self.player_icon_radius * 2 + self.player_icon_spacing
            )
            pygame.draw.circle(
                surface,
                _player.rgb,
                (circle_x, icon_y),
                self.player_icon_radius,
            )

    def toggle_map(self):
        self.current_map_index = (self.current_map_index + 1) % len(PinsMap)
        self.current_map = list(PinsMap)[self.current_map_index]
        self.map_button.text = f"{self.current_map.name}"

    def toggle_lives(self):
        self.current_lives_index = (self.current_lives_index + 1) % len(
            self.lives_options
        )

    def toggle_player_count(self):
        self.current_player_count_index = (
            self.current_player_count_index + 1
        ) % self.max_players

    def get_active_players(self):
        return Settings.players[: self.current_player_count_index + 1]

    def quit_game(self):
        pygame.quit()
        sys.exit()
