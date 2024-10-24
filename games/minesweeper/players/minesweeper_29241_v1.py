from random import choice
from queue import PriorityQueue
from games.minesweeper.action import MinesweeperAction
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from games.state import State
from games.minesweeper.result import MinesweeperResult

class minesweeper_29241_v1(MinesweeperPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.counter = 0  # Contador para desempate

    def heuristic(self, state, action):
        row, col = action.get_row(), action.get_col()
        grid = state.get_grid()
        if grid[row][col] != MinesweeperState.EMPTY_CELL:
            return float('inf')  # Célula já revelada, custo infinito

        mine_indicators = 0
        unopened_cells = 0
        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                if 0 <= row + drow < state.get_num_rows() and 0 <= col + dcol < state.get_num_cols():
                    if grid[row + drow][col + dcol] == MinesweeperState.EMPTY_CELL:
                        unopened_cells += 1
                    elif grid[row + drow][col + dcol] > 0:
                        mine_indicators += grid[row + drow][col + dcol]

        if unopened_cells == 0:
            return float('inf')  # Evita divisão por zero e escolha de células sem informação útil

        # Probabilidade estimada de mina na célula, com base no número de indicadores e células não abertas
        estimated_mine_probability = mine_indicators / unopened_cells
        return estimated_mine_probability

    def get_action(self, state: MinesweeperState):
        possible_actions = list(state.get_possible_actions())
        open_list = PriorityQueue()
        for action in possible_actions:
            h_cost = self.heuristic(state, action)
            open_list.put((h_cost, self.counter, action))
            self.counter += 1  # Incrementa o contador a cada ação adicionada

        if not open_list.empty():
            return open_list.get()[2]  # [2] para acessar o objeto action no tuplo
        else:
            return choice(possible_actions) if possible_actions else None

    def event_action(self, pos: int, action, new_state: State):
        pass  # Ignora por agora

    def event_end_game(self, final_state: State):
        pass  # Ignora por agora
