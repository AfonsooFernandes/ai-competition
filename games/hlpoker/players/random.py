from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.state import State
from random import choice


class RandomHLPokerPlayer(HLPokerPlayer):
    def __init__(self, name):
        super().__init__(name)

    def get_action_with_cards(self, state: HLPokerState, private_cards, board_cards):
        return choice(state.get_possible_actions())

    def event_my_action(self, action, new_state):
        pass

    def event_opponent_action(self, action, new_state):
        pass

    def event_new_game(self):
        pass

    def event_end_game(self, final_state: State):
        pass

    def event_result(self, pos: int, result: int):
        pass

    def event_new_round(self, round: Round):
        pass
