import pygame
from const import Colors, Settings
from object import Object


class Target:
    def __init__(self, x: int, y: int, points: int) -> None:
        self.overturned = False
        self.points = points

        self.texture = self.generate_texture()
        self.object = Object(
            x, y, self.texture, Settings.TARGET_MASS, Settings.TARGET_FRICTION
        )

    def generate_texture(self):
        texture = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(texture, Colors.WOOD.rgb, (10, 10), 10)

        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(str(self.points), True, Colors.WHITE.rgb)
        text_rect = text_surface.get_rect(center=(10, 10))
        texture.blit(text_surface, text_rect)

        return texture
