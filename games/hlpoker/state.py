from games.hlpoker.action import HLPokerAction
from games.hlpoker.round import Round
from games.state import State
from phevaluator.evaluator import evaluate_cards


class HLPokerState(State):
    BET_SIZE = 1.0
    MAX_RAISES = 4

    def __init__(self, num_players: int):
        super().__init__()

        if num_players != 2:
            raise ValueError("At the moment, HLPokerState only supports games with 2 players")

        """
        the sequence of actions
        """
        self.__sequence = []
        """
        the acting player index
        """
        self.__acting_player = 0
        """
        indicates if the game is finished
        """
        self.__is_finished = False
        """
        how much amount was betted by each player
        big blind will bet $2
        small blind will bet $1
        """
        self.__bets = [HLPokerState.BET_SIZE / 2, HLPokerState.BET_SIZE]
        """
        indicates the current game rounds
        """
        self.__round = Round.Preflop
        """
        indicates the current number of raises
        """
        self.__raise_count = 1
        """
        number of players in the game
        """
        self.__num_players = num_players
        """
        number of actions in the current round.
        """
        self.__actions_this_round = 0
        """
        number of actions in the current round.
        """
        self.__winner = None

    def get_num_players(self):
        return self.__num_players

    def validate_action(self, action) -> bool:
        if action not in [HLPokerAction.FOLD, HLPokerAction.CALL, HLPokerAction.RAISE]:
            return False

        if action == HLPokerAction.RAISE and self.__raise_count >= HLPokerState.MAX_RAISES:
            #print(f"[error] can't raise more than {HLPokerState.MAX_RAISES} times")
            return False

        if action == HLPokerAction.FOLD and self.__raise_count == 0:
            #print(f"[error] can't fold before there are any raises")
            return False

        return True

    def update(self, action):
        # update sequence of actions
        self.__sequence.append(action)

        # update the number of actions in the current round
        self.__actions_this_round += 1

        if action == HLPokerAction.FOLD:
            self.__is_finished = True
            self.__winner = 1 if self.__acting_player == 0 else 0
            return

        elif action == HLPokerAction.CALL:
            self.__bets[0] = self.__bets[1] = max(self.__bets[0], self.__bets[1])

            # Check if both players have acted and the bets are equal
            if self.__bets[0] == self.__bets[1] and self.__actions_this_round >= 2:
                # Move to the next round or showdown
                self.__round = Round(self.__round.value + 1)

                # Reset the acting player, actions count for the new round and num of raises
                self.__acting_player = 0
                self.__actions_this_round = 0
                self.__raise_count = 0
            else:
                # Swap the acting player
                self.__acting_player = 1 if self.__acting_player == 0 else 0
                self.__actions_this_round += 1

        elif action == HLPokerAction.RAISE:
            self.__raise_count += 1

            # equalize bets
            self.__bets[0] = self.__bets[1] = max(self.__bets[0], self.__bets[1])

            # increase the bet of the raising player
            self.__bets[self.__acting_player] += HLPokerState.BET_SIZE

            # swap the acting player
            self.__acting_player = 1 if self.__acting_player == 0 else 0

        # Finish the game if we reached showdown
        if self.__round == Round.Showdown:
            self.__is_finished = True

    def display(self):
        for action in self.__sequence:
            print(f"{action}", end=" > ")
        print(f"| round = {self.__round} | pot = {self.get_pot()}")

    """
    get the total amount that was put into bets so far
    """
    def get_pot(self):
        return sum(self.__bets)

    def is_finished(self) -> bool:
        return self.__is_finished

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned = HLPokerState(self.__num_players)
        cloned.__sequence = self.__sequence.copy()
        cloned.__acting_player = self.__acting_player
        cloned.__is_finished = self.__is_finished
        cloned.__bets = self.__bets.copy()
        cloned.__round = self.__round
        cloned.__raise_count = self.__raise_count
        cloned.__num_players = self.__num_players
        cloned.__actions_this_round = self.__actions_this_round
        cloned.__winner = self.__winner
        return cloned

    def get_result(self, pos):
        if self.__winner is None:
            # tie, nobody wins anything
            return 0

        if self.__winner == pos:
            # I will get the amount the other player betted
            return self.__bets[1 if pos == 0 else 0]
        else:
            return -self.__bets[pos]

    def before_results(self):
        pass

    def is_showdown(self):
        return self.__round == Round.Showdown

    def get_sequence(self):
        return self.__sequence

    def get_current_round(self):
        return self.__round

    def get_spent(self, pos):
        return self.__bets[pos]

    '''
    get the evaluation of a group of cards
    '''
    @staticmethod
    def evaluate_hand(cards):
        return evaluate_cards(*[card.__str__() for card in cards])

    def compute_results(self, p0cards, p1cards, board_cards):
        if self.is_showdown():

            # Helper function to convert cards to strings and evaluate
            p0_score = HLPokerState.evaluate_hand(p0cards + board_cards)
            p1_score = HLPokerState.evaluate_hand(p1cards + board_cards)

            if p0_score > p1_score:
                self.__winner = 1
            elif p1_score > p0_score:
                self.__winner = 0
            else:
                self.__winner = None  # Tie

        else:
            if self.__winner is None:
                raise ValueError("There should be a winner if we didn't reach showdown")

    def get_possible_actions(self):
        return list(filter(lambda a : self.validate_action(a), [action for action in HLPokerAction]))
