import pygame
from const import Colors, Settings
from object import Object


class ThrowingPin:
    def __init__(self) -> None:
        self.thrown = False

        self.texture = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.rect(self.texture, Colors.WOOD.rgb, (20, 0, 20, 60))

        self.object = self._create_object()

    def throw(self):
        mouse_vec = pygame.Vector2(pygame.mouse.get_pos())
        direction: pygame.Vector2 = mouse_vec - self.object.position

        if direction.length() != 0:
            direction = direction.normalize()

        strength = 22  # TO DO: zmiana/ustawienia/pobieranie siły
        self.object.velocity = direction * strength

        self.thrown = True

    def _create_object(self) -> Object:
        pin_width, pin_height = self.texture.get_size()
        start_x = Settings.BOARD_X + (Settings.BOARD_SIZE - pin_width) // 2
        start_y = Settings.BOARD_Y + Settings.BOARD_SIZE - pin_height - 10
        return Object(
            start_x, start_y, self.texture, Settings.PIN_MASS, Settings.PIN_FRICTION
        )

    def reset_position(self):
        self.object = self._create_object()
        self.thrown = False

    def rotate(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and not self.thrown:
            if event.key == pygame.K_LEFT:
                self.object.angle += 5
            elif event.key == pygame.K_RIGHT:
                self.object.angle -= 5
