from enum import Enum


class Colors(Enum):
    WHITE = ((255, 255, 255), "white")
    BLACK = ((0, 0, 0), "black")
    RED = ((255, 0, 0), "red")
    GREEN = ((0, 255, 0), "green")
    BLUE = ((0, 0, 255), "blue")
    GRAY = ((100, 100, 100), "gray")
    PINK = ((255, 192, 203), "pink")
    OAK = ((216, 181, 47), "oak")
    WOOD = ((161, 102, 47), "wood")
    GRAY_200 = ((230, 230, 230), "gray200")
    GRAY_400 = ((160, 160, 160), "gray400")
    GRAY_600 = ((90, 90, 90), "gray600")
    GRAY_800 = ((30, 30, 30), "gray800")

    @property
    def rgb(self):
        return self.value[0]

    @property
    def label(self):
        return self.value[1]
