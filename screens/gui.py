from typing import Sequence

import pygame

from const import Colors, Settings
from objects import Player


class GameGUI:
    def __init__(
        self,
        surface: pygame.Surface,
        players: Sequence[Player],
        heart_texture: pygame.Surface,
    ) -> None:
        self.surface = surface
        self.players = players
        self.heart_texture = heart_texture
        self.font = pygame.font.SysFont("Arial", 22)
        self.active_player: Player | None = None

    def _box_color(self, player: Player) -> Colors:
        if player is self.active_player:
            return Colors.GRAY_400
        if player.lives == 0:
            return Colors.GRAY_800

        return Colors.GRAY_600

    def draw(self, _player: Player | None = None):
        self.surface.fill(Colors.BLACK.rgb)
        self.active_player = _player

        padding = 10
        spacing = 86
        start_y = 30

        box_height = 72
        box_radius = 12
        box_width = self.surface.get_width() - 2 * padding

        for idx, player in enumerate(self.players):
            y = start_y + idx * spacing

            box_rect = pygame.Rect(padding, y, box_width, box_height)
            pygame.draw.rect(
                self.surface,
                self._box_color(player).rgb,
                box_rect,
                border_radius=box_radius,
            )

            line = f"{player.name:<15} {player.score:>3}"
            name_text = self.font.render(line, True, player.colour)
            text_rect = name_text.get_rect()
            text_rect.topleft = (padding + 20, y + (box_height - text_rect.height) // 2)
            self.surface.blit(name_text, text_rect)

            if player.lives is not None:
                heart_y = y + (box_height - self.heart_texture.get_height()) // 2
                for i in range(player.lives):
                    heart_x = padding + box_width - 20 - (player.lives - i) * 30
                    self.surface.blit(self.heart_texture, (heart_x, heart_y))

        pygame.draw.rect(self.surface, Colors.BLACK.rgb, Settings.GUI_BOARD, width=2)
