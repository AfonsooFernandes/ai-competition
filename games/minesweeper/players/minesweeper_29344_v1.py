import random
from games.minesweeper.action import MinesweeperAction
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from games.state import State

class minesweeper_29344_v1(MinesweeperPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.simulations = 50

    def set_simulations(self, simulations):
        self.simulations = simulations

    def get_action(self, state: MinesweeperState):
        best_action = None
        best_score = -float('inf') #garantir que qualquer pontuação calculada durante as simulações será maior que a pontuação inicial

        possible_actions = self.get_possible_actions(state)
        if not possible_actions:
            return None

        for _ in range(self.simulations): #loop pelo número de simulações especificado
            action, score = self.simulate(state, possible_actions)
            if score > best_score:
                best_action = action
                best_score = score

        if best_action is None:
            best_action = random.choice(possible_actions)

        return best_action
    
    #executa uma simulação para determinar a melhor ação a ser tomada a partir de um estado específico do jogo 
    def simulate(self, state: MinesweeperState, possible_actions):
        #calcula uma pontuação heurística para cada ação possível
        action_scores = [(action, self.heuristic(state, action)) for action in possible_actions]

        #encontra a menor pontuação entre as ações
        min_score = min(score for _, score in action_scores)

        #ajusta todas as pontuações para que a menor pontuação seja 1, garantindo que todas as ações tenham uma chance de serem escolhidas. 
        action_scores = [(action, score - min_score + 1) for action, score in action_scores]

        #seleciona uma ação de forma probabilística, com as ações de pontuação mais alta tendo maior probabilidade de serem escolhidas
        action = random.choices(action_scores, weights=[score for _, score in action_scores], k=1)[0][0]
        temp_state = state.clone()
        temp_state.play(action)

        score = self.rollout(temp_state)
        return action, score

    #realiza uma simulação a partir de um estado específico do jogo para avaliar seu resultado
    def rollout(self, state: MinesweeperState):
        max_rollout_depth = 5
        depth = 0
        while depth < max_rollout_depth:
            actions = list(self.get_possible_actions(state)) #obtém a lista de ações possíveis a partir do estado atual
            if not actions:
                break
            action = random.choice(actions) #Escolhe uma ação aleatória da lista de ações possíveis
            if not state.validate_action(action): #valida a ação
                break
            state.play(action) #aplica a ação ao estado
            depth += 1
        return self.evaluate(state)

    def get_possible_actions(self, state: MinesweeperState):
        return list(state.get_possible_actions())


    #determinar a segurança e o progresso no estado atual do jogo, penalizando fortemente a presença de minas enquanto recompensa células reveladas.
    def evaluate(self, state: MinesweeperState):
        score = 0
        grid = state.get_grid()
        for row in grid:
            for cell in row:
                #verifica se em cada linha para cada celula nao esta vazia e incrementa 1
                if cell != MinesweeperState.EMPTY_CELL:
                    score += 1
                if cell == MinesweeperState.MINE_CELL:
                    score -= 10
        return score

    def heuristic(self, state: MinesweeperState, action: MinesweeperAction):
        #extrai a linha e a coluna da ação, bem como o número de linhas e colunas do estado atual do jogo
        row, col = action.get_row(), action.get_col()
        num_rows = state.get_num_rows()
        num_cols = state.get_num_cols()
        score = 0

        grid = state.get_grid()
        unrevealed_cell_value = self.find_unrevealed_cell_value(grid)

        #percorre as células ao redor da célula de destino da ação garantindo que os índices permaneçam dentro dos limites da grade
        for r in range(max(0, row - 1), min(num_rows, row + 2)):
            for c in range(max(0, col - 1), min(num_cols, col + 2)):
                #obtém o valor da célula
                cell_value = grid[r][c]
                if cell_value != unrevealed_cell_value:
                    if cell_value == MinesweeperState.MINE_CELL:
                        score -= 10
                    elif cell_value == MinesweeperState.EMPTY_CELL:
                        score += 5
        return score

    def find_unrevealed_cell_value(self, grid):
        for row in grid:
            for cell in row:
                if cell in [None, -1, 0]: #célula contiver um valor que indique que ela não foi revelada 
                    return cell
        return -1

    def event_action(self, pos: int, action, new_state: State):
        pass

    def event_end_game(self, final_state: State):
        pass