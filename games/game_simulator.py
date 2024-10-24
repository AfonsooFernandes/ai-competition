from abc import ABC, abstractmethod

from games.player import Player
from games.state import State


class GameSimulator(ABC):

    def __init__(self, players: list):
        # only allow list of players
        assert len(list(filter(lambda p: not isinstance(p, Player), players))) <= 0

        # Ensure all player names are unique
        names = [player.get_name() for player in players]
        assert len(names) == len(set(names)), "Player names must be unique"

        # stores the possible permutations between players
        self.__permutations = []

        self.heap_permutation(players, len(players))

        # the selected permutation for the current game
        self.__current_permutation = 0

        # the results of all games between all players
        self.__results = []

    """
    Adapted from https://www.geeksforgeeks.org/heaps-algorithm-for-generating-permutations/
    It allows for generating all possible permutations of seats in a game
    """

    def heap_permutation(self, a: list, size: int):
        if size == 1:
            self.__permutations.append(a.copy())

        for i in range(0, size):
            self.heap_permutation(a, size - 1)

            if size % 2 == 1:
                temp = a[0]
                a[0] = a[size - 1]
                a[size - 1] = temp
            else:
                temp = a[i]
                a[i] = a[size - 1]
                a[size - 1] = temp

    """
    Swaps the order of the players. The order is changed in a way that guarantees that all combinations are considered
    Example for 2 players [a,b]
        - iteration 1: a,b
        - iteration 2, b,a
        - iteration 3, a,b (back to the initial configuration)
    
    Example for 3 players [x,y,z]
        - iteration 1: x,y,z
        - iteration 2: y,x,z
        - iteration 3: z,x,y
        - iteration 4: x,z,y
        - iteration 5: y,z,x
        - iteration 6: z,y,x
        - iteration 6: x,y,z (back to the initial configuration)
    """

    def change_player_positions(self):
        self.__current_permutation += 1
        if self.__current_permutation >= len(self.__permutations):
            self.__current_permutation = 0

    """
    starts a new game
    """

    @abstractmethod
    def on_init_game(self) -> State:
        pass

    """
    event before a game ends
    """

    @abstractmethod
    def on_before_end_game(self, state):
        pass

    """
    event when a game ends
    """

    @abstractmethod
    def on_end_game(self, state):
        pass


    """
    event that occur when a game state is updated
    """

    @abstractmethod
    def on_state_update(self, state):
        pass


    def get_player_positions(self):
        return self.__permutations[self.__current_permutation]

    """
    runs the simulation
    """
    def run_simulation(self):
        state = self.on_init_game()
        players = self.get_player_positions()

        # notify players a new game is starting
        for pos in range(0, len(players)):
            players[pos].set_current_pos(pos)
            players[pos].event_new_game()

        # play a turn
        while not state.is_finished():
            selected_action = None
            pos = state.get_acting_player()

            # obtain a valid action
            while True:
                selected_action = players[pos].get_action(state.clone())
                if state.validate_action(selected_action):
                    break

            state.play(selected_action)

            # notify players of the action
            for player in players:
                player.event_action(pos, selected_action, state.clone())

            # the simulator will run an optional hanlder for each updated state
            self.on_state_update(state)

        # handler to run before the game ends
        self.on_before_end_game(state)

        result = {}
        for player in players:
            # notify the player of the result in each position
            for pos in range(len(players)):
                player.event_result(pos, state.get_result(pos))

            # store the result for that player
            result[player.get_name()] = state.get_result(player.get_current_pos())
            player.event_end_game(state.clone())

        self.__results.append(result)

        # handler to run after a game ends
        self.on_end_game(state)

    # prints the stats for all players
    def print_stats(self):
        scores = self.get_global_score()
        for player in self.__permutations[0]:
            name = player.get_name()
            print(f"Player {name} | Total score: {scores[name]}$ | Avg. score per game: {scores[name] / len(self.__results)}$")

    # returns the list of players
    def get_players(self):
        return self.__permutations[0]

    # returns the ordered list of players for the current permutation
    def get_player_positions(self):
        return self.__permutations[self.__current_permutation]

    # gets the number os players
    def num_players(self):
        return len(self.__permutations[0])

    # gets the results of all games
    def get_results(self):
        return self.__results

    # gets the scores of all players
    def get_global_score(self):
        scores = {}
        for player in self.__permutations[0]:
            name = player.get_name()
            scores[name] = 0
            for result in self.__results:
                scores[name] += result[name]
        return scores


    @staticmethod
    @abstractmethod
    def get_player_type():
        pass

    @staticmethod
    @abstractmethod
    def get_state_type():
        pass

    @staticmethod
    @abstractmethod
    def get_action_type():
        pass