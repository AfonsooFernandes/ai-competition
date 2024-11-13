from enum import Enum

class Round(Enum):
    Preflop = 0
    Flop = 1
    Turn = 2
    River = 3
    Showdown = 4

    def __str__(self):
        return {
            0: "Preflop",
            1: "Flop",
            2: "Turn",
            3: "River",
            4: "Showdown"
        }[self.value]
