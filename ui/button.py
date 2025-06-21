from typing import Any
from const.colors import Colors
import pygame


class Button:
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        color: Colors = Colors.GRAY,
    ):
        self.rect = pygame.Rect(rect)
        self.text: str = text
        self.color = color
        self.font: pygame.font.Font = pygame.font.SysFont("arial", 30)

    def draw(
        self,
        surface: pygame.Surface,
    ):
        pygame.draw.rect(surface, self.color.rgb, self.rect)
        label = self.font.render(self.text, True, Colors.WHITE.rgb)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def is_clicked(self, event: pygame.event.Event) -> Any:
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
