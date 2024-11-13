from random import shuffle

from termcolor import cprint

from games.game_simulator import GameSimulator
from games.hlpoker.action import HLPokerAction
from games.hlpoker.card import Card, Suit, Rank
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.hlpoker.player import HLPokerPlayer


class HLPokerSimulator(GameSimulator):

    def __init__(self, players: list[HLPokerPlayer]):
        super().__init__(players)
        """
        deck of cards
        """
        self.__deck = [Card(rank, suit) for suit in Suit for rank in Rank]
        """
        stores the current round of the current game being simulated
        """
        self.__current_round = None
        """
        number of cards that were played in the current game
        """
        self.__used_card_count = None

    def on_init_game(self):
        # shuffle the deck
        shuffle(self.__deck)

        self.__used_card_count = 0
        self.__current_round = Round.Preflop

        # assign a pair of cards to each player
        for player in self.get_player_positions():
            private_cards = self.__deck[self.__used_card_count:self.__used_card_count+2]
            player.start_new_game(private_cards)
            self.__used_card_count += 2

        return HLPokerState(len(self.get_players()))

    def on_state_update(self, state):
        # check if we changed the round
        new_round = state.get_current_round()
        if new_round != self.__current_round:
            self.__current_round = new_round
            if self.__current_round != Round.Showdown:

                # Calculate the next card(s) to be shown
                next_card_index = self.__used_card_count
                positions = self.get_player_positions()

                if self.__current_round == Round.Flop:
                    # Show three cards for Flop
                    cards_to_show = self.__deck[next_card_index:next_card_index + 3]
                    self.__used_card_count += 3
                elif self.__current_round in (Round.Turn, Round.River):
                    # Show one card for Turn and River
                    cards_to_show = [self.__deck[next_card_index]]
                    self.__used_card_count += 1

                # Notify all positions about the new board cards
                for pos in positions:
                    pos.event_show_board_cards(cards_to_show, new_round)

            else:
                # Notify all positions about the opponent's cards
                players = self.get_player_positions()
                players[0].event_show_opponent_cards(*self.__deck[2:4])
                players[1].event_show_opponent_cards(*self.__deck[0:2])

    def on_before_end_game(self, state: HLPokerState):
        # if we reached the showdown, we are going to reveal the cards to all players
        state.compute_results(self.__deck[0:2], self.__deck[2:4], self.__deck[4:9])


    def on_end_game(self, state: HLPokerState):
        # ignored for this simulator
        pass

    @staticmethod
    def get_player_type():
        return HLPokerPlayer

    @staticmethod
    def get_state_type():
        return HLPokerState

    @staticmethod
    def get_action_type():
        return HLPokerAction