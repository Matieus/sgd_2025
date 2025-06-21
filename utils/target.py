from const.settings import Settings


class TargetLayoutCalculator:
    @staticmethod
    def position(row_index: int, col_index: int, pins_in_row: int) -> tuple[int, int]:
        x = TargetLayoutCalculator._calculate_x(col_index, pins_in_row)
        y = TargetLayoutCalculator._calculate_y(row_index)
        return x, y

    @staticmethod
    def _calculate_x(col_index: int, pins_in_row: int) -> int:
        row_width = TargetLayoutCalculator._get_row_width(pins_in_row)
        start_x = Settings.BOARD_X + (Settings.BOARD_SIZE - row_width) // 2
        return start_x + col_index * TargetLayoutCalculator._pin_spacing()

    @staticmethod
    def _calculate_y(row_index: int) -> int:
        return (
            Settings.TARGET_START_Y + row_index * TargetLayoutCalculator._pin_spacing()
        )

    @staticmethod
    def _pin_spacing() -> int:
        return Settings.TARGET_SIZE + Settings.TARGET_SPACING

    @staticmethod
    def _get_row_width(pins_in_row: int) -> int:
        return (
            pins_in_row * Settings.TARGET_SIZE
            + (pins_in_row - 1) * Settings.TARGET_SPACING
        )
