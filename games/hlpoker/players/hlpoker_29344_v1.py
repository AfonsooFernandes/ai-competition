import random
import math
from collections import defaultdict
from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.state import HLPokerState
from games.state import State
from games.hlpoker.round import Round 

class MonteCarloTreeSearchNode:
    def __init__(self, state, parent=None, action=None, player_pos=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.player_pos = player_pos if player_pos is not None else 0
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._untried_actions = state.get_possible_actions() if hasattr(state, 'get_possible_actions') else []

    def is_fully_expanded(self): #verifica se todas as ações possíveis a partir do estado atual já foram exploradas
        return len(self._untried_actions) == 0

    def expand(self): #criar novos nós filhos para o nó atual em uma árvore de busca 
        if self._untried_actions:
            action = self._untried_actions.pop() #Remove e retorna uma ação da lista de ações não tentadas.
            next_state = self.state.clone()
            self.apply_action(next_state, action)
            #cria um novo nó filho com o novo estado, definindo o nó atual como pai, e adiciona o novo nó à lista de filhos. 
            child_node = MonteCarloTreeSearchNode(next_state, parent=self, action=action, player_pos=(self.player_pos + 1) % next_state.get_num_players())
            self.children.append(child_node)
            return child_node
        return None

    def apply_action(self, state, action):
        if not state.validate_action(action):
            raise ValueError("Invalid action attempted")
        state._HLPokerState__sequence.append(action)
        state._HLPokerState__actions_this_round += 1

        if action == "raise":
            state._HLPokerState__bets[state._HLPokerState__acting_player] += HLPokerState.BET_SIZE
            state._HLPokerState__raise_count += 1
        elif action == "call":
            state._HLPokerState__bets[state._HLPokerState__acting_player] = max(state._HLPokerState__bets)
        elif action == "fold":
            state._HLPokerState__is_finished = True
            state._HLPokerState__winner = 1 if state._HLPokerState__acting_player == 0 else 0
            return

        if state._HLPokerState__round != Round.Showdown and state._HLPokerState__actions_this_round >= len(state._HLPokerState__bets):
            state._HLPokerState__round = Round(state._HLPokerState__round.value + 1)
            state._HLPokerState__actions_this_round = 0
            state._HLPokerState__raise_count = 0

        state._HLPokerState__acting_player = (state._HLPokerState__acting_player + 1) % state._HLPokerState__num_players

        if state._HLPokerState__round == Round.Showdown:
            state._HLPokerState__is_finished = True

    #seleciona o melhor filho do nó
    def best_child(self, c_param=1.4):
        if not self.children:
            return None
        choices_weights = [
            (c._results[1] / c._number_of_visits) + c_param * math.sqrt((2 * math.log(self._number_of_visits) / c._number_of_visits))
            for c in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    #escolhe uma acao a partir de uma lista de movimentos possiveis
    def heuristic_rollout_policy(self, possible_moves):
        for action in possible_moves:
            if action == "raise" or action == "call": #se a ação for "raise" ou "call", a função retorna essa ação imediatamente
                return action
        return random.choice(possible_moves)

    def rollout(self):
        current_rollout_state = self.state #Começa com o estado atual e, enquanto o jogo não terminar
        while not self.is_terminal_state(current_rollout_state):
            possible_moves = current_rollout_state.get_possible_actions()
            action = self.heuristic_rollout_policy(possible_moves) #escolhe uma usando a política heurística de rollout
            self.apply_action(current_rollout_state, action)
        return self.get_result(current_rollout_state, self.player_pos)

    def backpropagate(self, result): #atualiza o nó atual e seus ancestrais com o resultado da simulação
        self._number_of_visits += 1
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result) #chama recursivamente backpropagate no nó pai com o mesmo resultado

    def is_terminal_node(self):
        return self.is_terminal_state(self.state)

    def best_action(self):
        simulation_no = 1000
        for _ in range(simulation_no):
            v = self.tree_policy() #_tree_policy para selecionar um nó a ser expandido e simulado
            if v is not None:
                reward = v.rollout()
                v.backpropagate(reward)
        return self.best_child(c_param=0.).action #Após todas as simulações, a função retorna a ação do melhor filho do nó atual

    def tree_policy(self): #responsável por selecionar o próximo nó a ser expandido durante o processo de seleção 
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                next_node = current_node.best_child()
                if next_node is not None:
                    current_node = next_node
                else:
                    break
        return current_node

    def is_terminal_state(self, state):
        if hasattr(state, 'is_game_over'):
            return state.is_game_over()
        elif hasattr(state, 'is_finished'):
            return state.is_finished()
        elif hasattr(state, 'is_end'):
            return state.is_end()
        elif hasattr(state, 'game_over'):
            return state.game_over()
        return False

    def get_result(self, state, pos):
        if hasattr(state, 'get_winner'):
            return state.get_winner()
        elif hasattr(state, 'result'):
            return state.result()
        elif hasattr(state, 'get_result'):
            return state.get_result(pos)
        return None

class hlpoker_29344_v1(HLPokerPlayer):
    def __init__(self, name="MCTSPlayer"):
        super().__init__(name)
        self.position = None 

    def select_action(self, state):
        if isinstance(state, HLPokerState):
            #cria um nó raiz de busca de Monte Carlo com o estado atual e a posição do jogador
            root = MonteCarloTreeSearchNode(state, player_pos=self.position if self.position is not None else 0)
            selected_action = root.best_action()
            return selected_action
        else:
            raise ValueError("O estado fornecido não é uma instância de HLPokerState")

    def event_new_game(self, round_count=None, players=None):
        pass

    def event_new_round(self, round=None):
        pass

    def event_end_game(self, final_state=None):
        pass

    def event_my_action(self, action=None, new_state=None):
        pass

    def event_opponent_action(self, player=None, action=None, new_state=None):
        pass

    def set_position(self, position):
        self.position = position  # Setter method for position

    def get_action_with_cards(self, state, private_cards, board_cards):
        if isinstance(state, HLPokerState):
            return self.select_action(state)
        else:
            raise ValueError("O estado do jogo fornecido não é uma instância de HLPokerState")