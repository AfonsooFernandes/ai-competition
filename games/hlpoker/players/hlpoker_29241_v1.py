from games.hlpoker.action import HLPokerAction
from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.state import State
from collections import Counter

def check_hand_strength(cards):
    ranks = sorted(card.rank.value for card in cards)
    suits = [card.suit for card in cards]
    rank_counts = Counter(ranks)

    flush = len(set(suits)) == 1
    straight = max(ranks) - min(ranks) == 4 and len(rank_counts) == 5

    if flush and ranks == [10, 11, 12, 13, 14]:
        return 9  # Royal Flush
    if flush and straight:
        return 8  # Straight Flush
    if 4 in rank_counts.values():
        return 7  # Four of a Kind
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        return 6  # Full House
    if flush:
        return 5  # Flush
    if straight:
        return 4  # Straight
    if 3 in rank_counts.values():
        return 3  # Three of a Kind
    if len(rank_counts) == 3:
        return 2  # Two Pair
    if 2 in rank_counts.values():
        return 1  # One Pair

    return 0  # High Card


def missing_cards_for_straight(hand):
    ranks = sorted(set(card.rank.value for card in hand))
    gaps = max(0, 4 - (max(ranks) - min(ranks)))
    return gaps + 1 - len(ranks)


def missing_cards_for_flush(hand):
    suit_counts = Counter(card.suit for card in hand)
    return max(0, 5 - max(suit_counts.values()))


def is_folding_hand(hand):
    ranks = sorted(card.rank.value for card in hand)
    suits = {card.suit for card in hand}
    if len(set(ranks)) == 1:
        return False
    if abs(ranks[0] - ranks[1]) > 2 and len(suits) == 2:
        return True
    if ranks[0] <= 5 and ranks[1] <= 8 and len(suits) == 2:
        return True
    if ranks[1] <= 7:
        return True
    return False


def is_calling_hand(hand):
    ranks = sorted(card.rank.value for card in hand)
    suits = {card.suit for card in hand}
    if len(set(ranks)) == 1 and 2 <= ranks[0] <= 9:
        return True
    if len(set(ranks)) == 2 and abs(ranks[0] - ranks[1]) == 1 and len(suits) == 1:
        return True
    if len(set(ranks)) == 2 and ranks[1] >= 10:
        return True
    return False


def is_raising_hand(hand):
    ranks = sorted(card.rank.value for card in hand)
    suits = {card.suit for card in hand}
    if len(set(ranks)) == 1 and ranks[0] >= 11:
        return True
    if len(set(ranks)) == 2 and ranks[1] >= 10 and len(suits) == 1:
        return True
    if len(set(ranks)) == 2 and abs(ranks[0] - ranks[1]) == 1 and len(suits) == 1 and ranks[1] >= 10:
        return True
    return False


class hlpoker_29241_v1(HLPokerPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action_with_cards(self, state: HLPokerState, private_cards, board_cards):
        combined_cards = private_cards + board_cards
        strength = check_hand_strength(combined_cards)
        n_missing_flush_cards = missing_cards_for_flush(combined_cards)
        n_missing_straight_cards = missing_cards_for_straight(combined_cards)

        current_round = state.get_current_round()
        return self.decide_action(current_round, private_cards, combined_cards, strength, n_missing_flush_cards, n_missing_straight_cards)

    def decide_action(self, current_round, private_cards, combined_cards, strength, n_missing_flush_cards, n_missing_straight_cards):
        if current_round == Round.Preflop:
            if is_folding_hand(private_cards):
                return HLPokerAction.FOLD
            if is_calling_hand(private_cards):
                return HLPokerAction.CALL
            if is_raising_hand(private_cards):
                return HLPokerAction.RAISE

        if current_round == Round.Flop:
            if strength >= 2 or n_missing_flush_cards <= 1 or n_missing_straight_cards <= 1:
                return HLPokerAction.RAISE
            if strength == 1 or n_missing_flush_cards == 2 or n_missing_straight_cards == 2:
                return HLPokerAction.CALL
            return HLPokerAction.FOLD

        if current_round == Round.Turn:
            if strength >= 2 or n_missing_flush_cards == 0 or n_missing_straight_cards == 0:
                return HLPokerAction.RAISE
            if strength == 1 or n_missing_flush_cards == 1 or n_missing_straight_cards == 1:
                return HLPokerAction.CALL
            return HLPokerAction.FOLD

        if current_round == Round.River:
            if strength >= 2 or n_missing_flush_cards == 0 or n_missing_straight_cards == 0:
                return HLPokerAction.RAISE
            if strength == 1:
                return HLPokerAction.CALL
            return HLPokerAction.FOLD

        if current_round == Round.Showdown:
            return HLPokerAction.CALL

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
