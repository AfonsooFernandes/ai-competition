from termcolor import colored

from games.minesweeper.action import MinesweeperAction
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.result import MinesweeperResult
from games.minesweeper.state import MinesweeperState


class HumanMinesweeperPlayer(MinesweeperPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_color(self):
        pos = self.get_current_pos()
        prompt_color = 'red' if pos == 0 else 'blue'
        char = '●' if pos == 0 else '○'
        return [prompt_color, char]

    def get_action(self, state: MinesweeperState):
        state.display()
        while True:
            try:
                [prompt_color, char] = self.get_color()
                input_str = input(
                    colored(f"{self.get_name()} ({char}) > please choose row and column (separated by a space): ",
                            prompt_color))
                row, col = map(int, input_str.split())
                return MinesweeperAction(row, col)
            except Exception:
                print("Invalid input. Please enter row and column numbers separated by a space.")
                continue

    def event_action(self, pos: int, action, new_state: MinesweeperState):
        # ignore
        pass

    def event_end_game(self, final_state: MinesweeperState):
        final_state.display()
        [color, char] = self.get_color()
        if self.__last_result == MinesweeperResult.LOOSE.value:
            print(colored(f">{self.get_name()} ({char}) > I lost!", color))
        else:
            print(colored(f">{self.get_name()} ({char}) > I won!", color))

    def event_result(self, pos: int, result: int):
        if self.get_current_pos() == pos:
            self.__last_result = result