import random

from termcolor import colored

from games.minesweeper.action import MinesweeperAction
from games.minesweeper.result import MinesweeperResult
from games.state import State


class MinesweeperState(State):
    EMPTY_CELL = -1
    MINE_CELL = -2

    def __init__(self, num_rows: int = 7, num_cols: int = 7, num_mines: int = 11):
        super().__init__()

        if num_rows < 4:
            raise Exception("the number of rows must be 4 or over")
        if num_cols < 4:
            raise Exception("the number of cols must be 4 or over")
        if num_mines % 2 == 0:
            raise Exception("Number of mines must be odd")

        """
        the dimensions of the board
        """
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__num_mines = num_mines

        """
        the grid
        """
        self.__grid = [[MinesweeperState.EMPTY_CELL for _i in range(self.__num_cols)] for _j in range(self.__num_rows)]
        self.__grid_players = [[MinesweeperState.EMPTY_CELL for _i in range(self.__num_cols)] for _j in range(self.__num_rows)]
        self.__mines = self.__place_mines()
        self.__acting_player = 0
        self.__mines_hit = [0, 0]
        self.__has_winner = False

    def __place_mines(self):
        mines = set()
        while len(mines) < self.__num_mines:
            mine = (random.randint(0, self.__num_rows - 1), random.randint(0, self.__num_cols - 1))
            mines.add(mine)
        return mines

    def get_grid(self):
        return self.__grid

    def __count_neighbor_mines(self, row, col):
        count = 0
        for r in range(max(0, row - 1), min(self.__num_rows, row + 2)):
            for c in range(max(0, col - 1), min(self.__num_cols, col + 2)):
                if (r, c) != (row, col) and (r, c) in self.__mines:
                    count += 1
        return count

    def get_result(self, player):
        if not self.__has_winner:
            return None
        return MinesweeperResult.WIN if self.__mines_hit[player] < self.__mines_hit[1 - player] else MinesweeperResult.LOSE

    def get_num_players(self):
        return 2

    def update(self, action: MinesweeperAction):
        row, col = action.get_row(), action.get_col()
        self.__grid_players[row][col] = self.__acting_player

        if (row, col) in self.__mines:
            self.__grid[row][col] = MinesweeperState.MINE_CELL
            self.__mines_hit[self.__acting_player] += 1
        else:
            self.__grid[row][col] = self.__count_neighbor_mines(row, col)

        self.__acting_player = 1 - self.__acting_player
        self.__has_winner = len(self.__mines) == sum(self.__mines_hit)

    def validate_action(self, action: MinesweeperAction) -> bool:
        row, col = action.get_row(), action.get_col()

        if row >= self.__num_rows:
            return False

        if col >= self.__num_cols:
            return False

        if self.__grid[row][col] != MinesweeperState.EMPTY_CELL:
            return False

        return True


    def __display_cell(self, row, col):
        cell_value = self.__grid[row][col]

        if cell_value != MinesweeperState.EMPTY_CELL:
            color = 'red' if self.__grid_players[row][col] == 0 else 'blue'
            char = ('●' if color == 'red' else '◍') if self.__grid[row][col] == MinesweeperState.MINE_CELL else self.__grid[row][col]
            print(colored(char, color), end="")
        else:
            print(' ', end="")

    def __display_numbers(self):
        for col in range(0, self.__num_cols):
            if col < 10:
                print(' ', end="")
            print(col, end="")
        print("")

    def __display_separator(self):
        for col in range(0, self.__num_cols):
            print("--", end="")
        print("-")

    def display(self):
        self.__display_numbers()
        self.__display_separator()

        for row in range(0, self.__num_rows):
            print('|', end="")
            for col in range(0, self.__num_cols):
                self.__display_cell(row, col)
                print('|', end="")
            print("")
            self.__display_separator()

        self.__display_numbers()
        print("")

    def is_finished(self) -> bool:
        return self.__has_winner

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned_state = MinesweeperState(self.__num_rows, self.__num_cols)
        cloned_state.__num_rows = self.__num_rows
        cloned_state.__num_cols = self.__num_cols
        cloned_state.__num_mines = self.__num_mines
        cloned_state.__mines = self.__mines.copy()
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__mines_hit = self.__mines_hit.copy()
        cloned_state.__has_winner = self.__has_winner
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                cloned_state.__grid[row][col] = self.__grid[row][col]
                cloned_state.__grid_players[row][col] = self.__grid_players[row][col]
        return cloned_state

    def get_result(self, pos):
        return MinesweeperResult.WIN.value if self.__mines_hit[pos] < self.__mines_hit[1 - pos] else MinesweeperResult.LOOSE.value

    def get_num_rows(self):
        return self.__num_rows

    def get_num_cols(self):
        return self.__num_cols

    def before_results(self):
        pass

    def get_possible_actions(self):
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                if self.validate_action(MinesweeperAction(row, col)):
                    yield MinesweeperAction(row, col)
