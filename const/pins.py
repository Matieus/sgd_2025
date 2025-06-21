from enum import Enum


class PinsMap(Enum):
    STANDARD = (
        [7, 9, 8],
        [5, 11, 12, 6],
        [3, 10, 4],
        [1, 2],
    )

    BUSY = (
        [11, 9, 10, 12],
        [7, 5, 6, 8],
        [3, 1, 2, 4],
    )

    LINE = ([i for i in range(1, 13)],)
