from const import Colors


class Player:
    def __init__(self, lives: int | None, colour: Colors) -> None:
        self.score: int = 0
        self.colour = colour.rgb
        self.name: str = colour.label.upper()
        self.score: int = 0
        self.lives: int | None = lives

    def check(self, win_score: int):
        if self.score == win_score:
            return True
        elif self.score > win_score:
            self.score = self.score // 2
            return False
