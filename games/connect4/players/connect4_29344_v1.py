from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
from games.connect4.action import Connect4Action
from games.state import State
import time

class connect4_29344_v1(Connect4Player):
    def __init__(self, name, depth=4):
        super().__init__(name)
        self.depth = depth
        self.memo = {}

    def heuristic(self, state: Connect4State):
        score = 0
        grid = self.get_grid(state)
        if grid is None:
            raise AttributeError("O estado do jogo não possui o atributo 'grid'.")

        player = self.get_current_player(state)
        opponent = 1 if player == 0 else 0

        def count_pattern(pattern, row_str):
            return row_str.count(pattern)

        for row in grid:
            row_str = ''.join(str(cell) for cell in row)
            score += 5 * count_pattern(str(player) * 2, row_str)
            score += 10 * count_pattern(str(player) * 3, row_str)
            score += 100 * count_pattern(str(player) * 4, row_str)
            score -= 5 * count_pattern(str(opponent) * 2, row_str)
            score -= 10 * count_pattern(str(opponent) * 3, row_str)
            score -= 100 * count_pattern(str(opponent) * 4, row_str)

        center_col = len(grid[0]) // 2
        for row in grid:
            if row[center_col] == player:
                score += 3
        return score

    def get_grid(self, state):
        if hasattr(state, 'grid'):
            return state.grid
        elif hasattr(state, '_Connect4State__grid'):
            return state._Connect4State__grid
        else:
            print("Atributos do estado:", state.__dict__)
            return None

    def get_current_player(self, state):
        if hasattr(state, 'current_player'):
            return state.current_player
        elif hasattr(state, '_Connect4State__acting_player'):
            return state._Connect4State__acting_player
        else:
            raise AttributeError("O estado do jogo não possui o atributo 'current_player'.")

    def simulate_result(self, state: Connect4State, action):
        grid = self.get_grid(state)
        if grid is None:
            raise AttributeError("O estado do jogo não possui o atributo 'grid'.")

        action_column = action._Connect4Action__col #obtém a coluna da ação 
        new_grid = [row.copy() for row in grid]

        for row in reversed(new_grid): #Percorre as linhas da nova grade de baixo para cima
            if row[action_column] == -1:
                row[action_column] = self.get_current_player(state) #Quando encontra essa célula vazia, coloca a peça do jogador atual nessa posição e interrompe 
                break

        new_state = Connect4State(state._Connect4State__num_rows, state._Connect4State__num_cols)
        new_state._Connect4State__grid = new_grid
        new_state._Connect4State__turns_count = state._Connect4State__turns_count + 1
        new_state._Connect4State__acting_player = 1 - self.get_current_player(state)
        new_state._Connect4State__has_winner = self.check_winner(new_grid, self.get_current_player(state))

        return new_state

    def check_winner(self, grid, player):
        def check_line(line):
            return any(line[i:i+4] == [player] * 4 for i in range(len(line) - 3))

        for row in grid:
            if check_line(row):
                return True

        for col in range(len(grid[0])):
            column = [row[col] for row in grid]
            if check_line(column):
                return True

        for row in range(len(grid) - 3):
            for col in range(len(grid[0]) - 3):
                if all(grid[row + i][col + i] == player for i in range(4)):
                    return True
                if all(grid[row + 3 - i][col + i] == player for i in range(4)):
                    return True

        return False

    def minimax(self, state: Connect4State, depth, alpha, beta, maximizing_player):
        state_tuple = self.state_to_tuple(state) #converte o estado do jogo em uma tupla para que possa ser usada como chave no dicionário
        if state_tuple in self.memo:
            return self.memo[state_tuple]

        if depth == 0 or self.is_game_over(state):
            eval = self.heuristic(state) # calcula a avaliação heurística do estado atual.
            self.memo[state_tuple] = eval #armazena o valor calculado no memo
            return eval

        if maximizing_player:
            max_eval = float('-inf')
            #ordena as ações possíveis com base na avaliação heurística e simula o resultado
            for action in sorted(state.get_possible_actions(), key=lambda a: self.heuristic(self.simulate_result(state, a)), reverse=True):
                #chama recursivamente o método minimax com a profundidade reduzida
                eval = self.minimax(self.simulate_result(state, action), depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.memo[state_tuple] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for action in sorted(state.get_possible_actions(), key=lambda a: self.heuristic(self.simulate_result(state, a))):
                eval = self.minimax(self.simulate_result(state, action), depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.memo[state_tuple] = min_eval
            return min_eval

    def is_game_over(self, state: Connect4State):
        grid = self.get_grid(state)
        if grid is None:
            raise AttributeError("O estado do jogo não possui o atributo 'grid'.")

        if self.check_winner(grid, self.get_current_player(state)):
            return True

        return all(cell != Connect4State.EMPTY_CELL for row in grid for cell in row)

    def get_action(self, state: Connect4State):
        start_time = time.time()
        best_score = float('-inf') #inicializa a melhor pontuação com um valor muito baixo
        best_action = None
        possible_actions = state.get_possible_actions()

        #Para cada ação possível, calcula a heurística do estado resultante simulado
        actions_with_heuristic = [(action, self.heuristic(self.simulate_result(state, action))) for action in possible_actions]
        sorted_actions = sorted(actions_with_heuristic, key=lambda x: x[1], reverse=True)

        for action, _ in sorted_actions:
            #simula o resultado e chama recursivamente o método minimax com a profundidade reduzida
            eval = self.minimax(self.simulate_result(state, action), self.depth - 1, float('-inf'), float('inf'), False)
            if eval > best_score:
                best_score = eval
                best_action = action
            if time.time() - start_time > 1:
                break
        return best_action

    def state_to_tuple(self, state):
        grid = self.get_grid(state)
        return tuple(tuple(row) for row in grid), self.get_current_player(state)

    def event_action(self, pos, action, state):
        pass

    def event_end_game(self, state):
        pass

    def event_new_game(self):
        pass

    def event_result(self, pos: int, result):
        pass