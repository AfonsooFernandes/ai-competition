from abc import ABC

from games.minesweeper.result import MinesweeperResult
from games.player import Player


class MinesweeperPlayer(Player, ABC):

    def __init__(self, name):
        super().__init__(name)

        """
        stats is a dictionary that will store the number of times each result occurred
        """
        self.__stats = {}
        for c4res in MinesweeperResult:
            self.__stats[c4res] = 0

        """
        here we are storing the number of games
        """
        self.__num_games = 0

    def print_stats(self):
        pass

    def event_new_game(self):
        pass

    def event_result(self, pos: int, result):
        pass
