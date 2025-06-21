from const.colors import Colors


class Settings:
    WIDTH = 1200
    HEIGHT = 800

    GUI_WIDTH = WIDTH // 3
    BOARD_MAX_WIDTH = WIDTH - GUI_WIDTH
    BOARD_SIZE = min(BOARD_MAX_WIDTH, HEIGHT)

    BOARD_X = GUI_WIDTH + (BOARD_MAX_WIDTH - BOARD_SIZE) // 2
    BOARD_Y = (HEIGHT - BOARD_SIZE) // 2

    OFFSET = (BOARD_X, BOARD_Y)
    BOARD = (BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE)
    GUI_BOARD = (0, 0, GUI_WIDTH, HEIGHT)

    TARGET_SPACING = 10
    TARGET_SIZE = 20
    TARGET_START_Y = 75
    TARGET_FRICTION = 0.9
    TARGET_MASS = 1.5

    PIN_FRICTION = 0.98
    PIN_MASS = 3

    players = [
        Colors.RED,
        Colors.GREEN,
        Colors.BLUE,
    ]
