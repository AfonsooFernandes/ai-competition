from abc import ABC

from games.connect4.result import Connect4Result
from games.player import Player


class Connect4Player(Player, ABC):

    def __init__(self, name):
        super().__init__(name)

        """
        stats is a dictionary that will store the number of times each result occurred
        """
        self.__stats = {}
        for c4res in Connect4Result:
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
