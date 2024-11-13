from enum import Enum

from enum import Enum

class Rank(Enum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14

    def __str__(self):
        return {
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "T",
            11: "J",
            12: "Q",
            13: "K",
            14: "A"
        }[self.value]


SUIT_SYMBOLS = ['♥', '♦', '♣', '♠']

class Suit(Enum):

    Hearts = 0
    Diamonds = 1
    Clubs = 2
    Spades = 3

    def __str__(self):
        return {
            0: "h",
            1: "d",
            2: "c",
            3: "s"
        }[self.value]

    def symbol(self):
        return SUIT_SYMBOLS[self.value]


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __lt__(self, other):
        return self.rank.value < other.rank.value

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def to_symbol_str(self):
        return f"{self.rank}{self.suit.symbol()}"
