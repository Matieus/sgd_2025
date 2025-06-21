import sys

import pygame

from const import Colors, PinsMap, Settings
from objects import Player, Target, ThrowingPin
from screens import GameGUI, Menu, PauseMenu
from utils.target import TargetLayoutCalculator

pygame.init()
screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
pygame.display.set_caption("Molkky")
FONT = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

gui_surface = pygame.Surface((Settings.GUI_WIDTH, Settings.HEIGHT))
board_surface = pygame.Surface((Settings.BOARD_SIZE, Settings.BOARD_SIZE))
heart_texture = pygame.image.load("assets/heart32.png").convert_alpha()


def pause():
    pause_menu = PauseMenu(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "continue"

            for action, button in pause_menu.buttons.items():
                if button.is_clicked(event):
                    return action

        pause_menu.draw()

        pygame.display.flip()
        clock.tick(30)


class GameCreator:
    def __init__(self) -> None:
        pass


class Game:
    def __init__(self, players: list[Player], pins_map: PinsMap) -> None:
        self.players = players
        self.throwing_pin = ThrowingPin()
        self.targets = self.generate_targets(pins_map)
        self.current_player_index = 0

        self.gui = GameGUI(gui_surface, self.players, heart_texture)
        self.winner: Player | None = None
        self.game_lost = False

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def overturned_targets(self) -> list[int]:
        return [target.points for target in self.targets if target.overturned]

    def counter(self):
        _targets: list[int] = self.overturned_targets()
        if not _targets:
            return 0
        elif len(_targets) > 1:
            return len(_targets)

        return _targets.pop()

    def _update(self):
        self.throwing_pin.object.update()
        for target in self.targets:
            target.object.update()

    def generate_targets(self, pins_map: PinsMap):
        targets: list[Target] = []
        layout = pins_map.value

        for row_idx, row in enumerate(layout):
            for col_idx, points in enumerate(row):
                x, y = TargetLayoutCalculator.position(row_idx, col_idx, len(row))
                targets.append(Target(x, y, points))

        return targets

    def draw(self):
        self.throwing_pin.object.draw(
            board_surface,
            self.throwing_pin.texture,
            offset=Settings.OFFSET,
        )

        for target in self.targets:
            target.object.draw(
                board_surface,
                target.texture,
                offset=Settings.OFFSET,
            )

    def draw_win(self):
        overlay = pygame.Surface((Settings.WIDTH, Settings.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont("Arial", 48, bold=True)
        text = font.render(f"{self.winner.name} wins!", True, self.winner.colour)
        text_rect = text.get_rect(center=(Settings.WIDTH // 2, Settings.HEIGHT // 2))
        screen.blit(text, text_rect)

    def draw_loss(self):
        overlay = pygame.Surface((Settings.WIDTH, Settings.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont("Arial", 48, bold=True)
        text = font.render("Game Over!", True, Colors.RED.rgb)
        text_rect = text.get_rect(center=(Settings.WIDTH // 2, Settings.HEIGHT // 2))
        screen.blit(text, text_rect)

    def check_loss(self):
        if all(player.lives == 0 for player in self.players):
            self.game_lost = True

    def _collisions(self):
        for i in range(len(self.targets)):
            for j in range(i + 1, len(self.targets)):
                self.targets[i].object.resolve_collision_with(
                    self.targets[j].object, self_push=0.2
                )

        for target in self.targets:
            self.throwing_pin.object.resolve_collision_with(
                target.object, self_push=0.95
            )

            if not target.overturned and target.object.velocity.length_squared() > 0:
                target.overturned = True

    def _throw(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.throwing_pin.thrown:
                self.throwing_pin.throw()

    def _next_turn(self):
        if self.throwing_pin.thrown:
            if self.throwing_pin.object.velocity.length_squared() == 0:
                points = self.counter()
                if points:
                    self.current_player.score += points

                    if self.current_player.score == 50:
                        self.winner = self.current_player
                    elif self.current_player.score > 50:
                        self.current_player.score //= 2

                else:
                    if isinstance(self.current_player.lives, int):
                        self.current_player.lives -= 1

                for target in self.targets:
                    target.overturned = False

                self.throwing_pin.reset_position()
                self.next_player()

                if self.current_player.lives == 0:
                    self.next_player()

                self.check_loss()

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.throwing_pin.rotate(event)
            self._throw(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                choice = pause()
                if choice == "continue":
                    continue
                elif choice == "main_menu":
                    return "menu"
                elif choice == "quit":
                    pygame.quit()
                    sys.exit()

        self._update()
        self._collisions()
        self._next_turn()


def main(lives: int | None, pins_map: PinsMap, players_colors: list[Colors]):
    _players = [Player(lives, player) for player in players_colors]

    game = Game(_players, pins_map)
    gui = GameGUI(gui_surface, _players, heart_texture)

    while True:

        result = game.run()
        if result is not None:
            return

        screen.fill(Colors.BLACK.rgb)
        board_surface.fill(Colors.BLACK.rgb)

        if game.winner:
            gui.draw(game.current_player)
            game.draw()

            screen.blit(gui_surface, (0, 0))
            screen.blit(board_surface, Settings.OFFSET)

            game.draw_win()
            pygame.display.flip()

            pygame.time.delay(5000)
            return

        if game.game_lost:
            gui.draw(game.current_player)
            game.draw()

            screen.blit(gui_surface, (0, 0))
            screen.blit(board_surface, Settings.OFFSET)

            game.draw_loss()
            pygame.display.flip()

            pygame.time.delay(5000)
            return

        gui.draw(game.current_player)
        game.draw()

        screen.blit(gui_surface, (0, 0))
        screen.blit(board_surface, Settings.OFFSET)

        pygame.display.flip()
        clock.tick(60)


def splash_screen():
    splash_time = 10_000
    start_time = pygame.time.get_ticks()

    title_font = pygame.font.SysFont("Arial", 24)
    title = title_font.render("Welcome in Molkky!", True, Colors.WHITE.rgb)

    subtitle_font = pygame.font.SysFont("Arial", 18)
    subtitle = subtitle_font.render("press enter to skip ...", True, Colors.GRAY.rgb)

    title_rect = title.get_rect(center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 30))
    subtitle_rect = subtitle.get_rect(
        center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 + 10)
    )

    while True:
        now = pygame.time.get_ticks()
        elapsed = now - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

        screen.fill(Colors.BLACK.rgb)
        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)
        pygame.display.flip()
        clock.tick(60)

        if elapsed >= splash_time:
            return


def run_menu():
    running = True
    menu = Menu()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu.quit_game()

            if menu.play.is_clicked(event):

                main(menu.current_lives, menu.current_map, menu.get_active_players())

            if menu.exit.is_clicked(event):
                menu.quit_game()

            if menu.lives_button.is_clicked(event):
                menu.toggle_lives()

            if menu.map_button.is_clicked(event):
                menu.toggle_map()

            if menu.players_button.is_clicked(event):
                menu.toggle_player_count()

        menu.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    splash_screen()
    run_menu()
