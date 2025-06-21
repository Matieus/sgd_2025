import pygame
from const import Settings


class Object:
    def __init__(
        self,
        x: int,
        y: int,
        texture: pygame.Surface,
        mass: float,
        friction: float = 0.97,
    ) -> None:
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.friction: float = friction
        self.angle: float = 0
        self.texture = texture
        self.mass = mass
        self.velocity: pygame.Vector2

    def draw(
        self,
        surface: pygame.Surface,
        texture: pygame.Surface,
        offset: tuple[int, int] = (0, 0),
    ):
        draw_pos: pygame.Vector2 = self.position - pygame.Vector2(offset)

        rotated_image = pygame.transform.rotate(texture, self.angle)
        rotated_rect = rotated_image.get_rect(center=draw_pos)

        surface.blit(rotated_image, rotated_rect)

    def update(self):
        self.velocity *= self.friction
        if self.velocity.length_squared() < 0.01:
            self.velocity = pygame.Vector2(0, 0)
        self.position += self.velocity
        self._check_bounds_and_bounce()

    def _check_bounds_and_bounce(self):
        w, h = self.texture.get_size()
        min_x = Settings.BOARD_X + w / 2
        max_x = Settings.BOARD_X + Settings.BOARD_SIZE - w / 2
        min_y = Settings.BOARD_Y + h / 2
        max_y = Settings.BOARD_Y + Settings.BOARD_SIZE - h / 2

        bounced = False
        if self.position.x < min_x:
            self.position.x = min_x
            self.velocity.x *= -0.8
            bounced = True
        elif self.position.x > max_x:
            self.position.x = max_x
            self.velocity.x *= -0.8
            bounced = True

        if self.position.y < min_y:
            self.position.y = min_y
            self.velocity.y *= -0.8
            bounced = True
        elif self.position.y > max_y:
            self.position.y = max_y
            self.velocity.y *= -0.8
            bounced = True

        if bounced:
            self.angle += 15

    def resolve_collision_with(self, other: "Object", self_push: float = 0.5):
        delta = other.position - self.position
        dist_sq = delta.length_squared()
        if dist_sq == 0:
            delta = pygame.Vector2(1, 0)
            dist_sq = 1
        dist = dist_sq**0.5
        r_self = self.texture.get_width() / 2
        r_other = other.texture.get_width() / 2
        overlap = r_self + r_other - dist

        if overlap > 0:
            direction = delta / dist
            self.position -= direction * overlap * self_push
            other.position += direction * overlap * (1 - self_push)

            v_self = self.velocity.dot(direction)
            v_other = other.velocity.dot(direction)

            m1 = self.mass
            m2 = other.mass

            new_v_self = (v_self * (m1 - m2) + 2 * m2 * v_other) / (m1 + m2)
            new_v_other = (v_other * (m2 - m1) + 2 * m1 * v_self) / (m1 + m2)

            self.velocity += (new_v_self - v_self) * direction
            other.velocity += (new_v_other - v_other) * direction
