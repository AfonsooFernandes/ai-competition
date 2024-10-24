from games.minesweeper.action import MinesweeperAction
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from games.game_simulator import GameSimulator


class MinesweeperSimulator(GameSimulator):

    def __init__(self, players, num_rows: int = 7, num_cols: int = 7):
        super(MinesweeperSimulator, self).__init__(players)
        """
        the number of rows and cols from the Minesweeper grid
        """
        self.__num_rows = num_rows
        self.__num_cols = num_cols

    def on_init_game(self):
        return MinesweeperState(self.__num_rows, self.__num_cols)

    def on_before_end_game(self, state: MinesweeperState):
        # ignored for this simulator
        pass

    def on_end_game(self, state: MinesweeperState):
        # ignored for this simulator
        pass

    def on_state_update(self, state):
        # ignored for this simulator
        pass

    @staticmethod
    def get_player_type():
        return MinesweeperPlayer

    @staticmethod
    def get_state_type():
        return MinesweeperState

    @staticmethod
    def get_action_type():
        return MinesweeperAction