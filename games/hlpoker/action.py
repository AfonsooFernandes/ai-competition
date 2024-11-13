from enum import Enum


class HLPokerAction(Enum):
    """
    there are 3 possible actions in limit texas hold'em poker:
        - CALL: match the current bet
        - FOLD: forfeit the current bet
        - RAISE: increase the current bet
    """
    FOLD = 0
    CALL = 1
    RAISE = 2

    def __str__(self):
        return {
            0: "Fold",
            1: "Call",
            2: "Raise"
        }[self.value]