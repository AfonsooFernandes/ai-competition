from abc import ABC, abstractmethod

from termcolor import colored

from games.hlpoker.card import Card, Suit
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.player import Player


class HLPokerPlayer(Player, ABC):

    def __init__(self, name):
        super().__init__(name)

        """
        score will store the money earned (or lost)
        """
        self.__score = 0

        """
        here we are storing the number of games
        """
        self.__num_games = 0

        """
        we also need to store the current card we are holding
        """
        self.__private_cards = [None, None]

        """
        we also need to store the current card we saw
        """
        self.__board_cards = []

        """
        we are storing the cards our opponent holds
        """
        self.__opponent_cards = [None, None]

    """
    gets the score
    """

    def get_score(self):
        return self.__score

    def start_new_game(self, private_cards):
        self.__private_cards = private_cards.copy()
        self.__opponent_cards = [None, None]
        self.__board_cards = []
        self.__current_round = Round.Preflop
        self.event_new_round(self.__current_round)

    def event_result(self, pos: int, result: int):
        if pos == self.get_current_pos():
            self.__score += result

    """
    this method gets called at the start of a new game to
    indicate to the player which private cards they will start with
    """

    def event_show_private_cards(self, c1: Card, c2: Card):
        self.__private_cards[0] = c1
        self.__private_cards[1] = c2

    """
    this method gets called at the end of a game if it reaches the showdown
    where we will get to know the cards of our opponent
    """

    def event_show_opponent_cards(self, c1: Card, c2: Card):
        self.__opponent_cards[0] = c1
        self.__opponent_cards[1] = c2
        pass

    """
    this method gets called at the start of a new game to
    indicate to the player which private cards they will start with
    :param cards the cards that will be added to the board
    :param round new rounds that is being played
    """

    def event_show_board_cards(self, cards: [Card], round):
        self.__board_cards.extend(cards)
        self.__current_round = round
        self.event_new_round(self.__current_round)

    def print_stats(self):
        print(
            f"Player {self.get_name()} | Total profit: ${self.__score} | Profit per game: ${self.get_expected_value()}")

    """
    Overrides the original get_action method but includes the cards
    The cards are not part of the game state, but rather hidden information
    :param state: the current game state
    """
    def get_action(self, state):
        return self.get_action_with_cards(state, self.__private_cards, self.__board_cards)

    @staticmethod
    def print_colored_cards(card_list):
        for card in card_list:
            color = "black" if card.suit in [Suit.Clubs, Suit.Spades] else "red"
            colored_card = colored(card.to_symbol_str(), color)
            print(colored_card, end=" ")
        print()

    def print_cards(self):
        print("Private cards: ", end="")
        HLPokerPlayer.print_colored_cards(self.__private_cards)

        print("  Board cards: ", end="")
        HLPokerPlayer.print_colored_cards(self.__board_cards)

    def print_state(self, state: HLPokerState):
        self.print_cards()
        for action in state.get_sequence():
            print(f"{action}", end=" > ")
        print(
            f"| round = {state.get_current_round()} | pot = ${state.get_pot()} | spent = ${state.get_spent(self.get_current_pos())}")

    def get_private_cards(self):
        return self.__private_cards

    def get_board_cards(self):
        return self.__board_cards

    def get_opponent_cards(self):
        return self.__opponent_cards

    def event_action(self, pos: int, action, new_state):
        if self.get_current_pos() == pos:
            self.event_my_action(action, new_state)
        else:
            self.event_opponent_action(action, new_state)

    """
    this method should be implemented in the child class.
    gets called at the start of a new game to indicate to the player 
    which private cards they will start with
    """
    @abstractmethod
    def event_new_game(self):
        pass

    """
    this method should be implemented in the child class.
    gets called whenever a player needs to select the action to perform
    """
    @abstractmethod
    def get_action_with_cards(self, state, private_cards, board_cards):
        pass

    """
    this method should be implemented in the child class.
    gets called whenever I perform a successful action
    """
    @abstractmethod
    def event_my_action(self, action, new_state):
        pass

    """
    this method should be implemented in the child class.
    gets called whenever I perform a successful action
    """
    @abstractmethod
    def event_opponent_action(self, action, new_state):
        pass

    """
    this method should be implemented in the child class.
    gets called whenever a new round starts
    :param round: the new round that started
    """
    @abstractmethod
    def event_new_round(self, round):
        pass
