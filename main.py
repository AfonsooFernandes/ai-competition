import argparse
import itertools
from collections import namedtuple, defaultdict
from tqdm import tqdm

from constants import AVAILABLE_GAME_TYPES, AVAILABLE_PLAYER_TYPES

def run_simulation(game_settings):
    removed_players = []

    while len(game_settings['players']) > 1:
        scores = defaultdict(int)
        match_results = defaultdict(dict)

        for player1, player2 in itertools.combinations(game_settings['players'], 2):
            simulator = game_settings['game']([player1, player2])
            print(f"Simulation: {player1.get_name()} VS {player2.get_name()}")

            names = {player1.get_name(): player1, player2.get_name(): player2}

            # Run initial iterations with progress bar
            for _ in tqdm(range(game_settings['num_iterations']), desc="Running iterations"):
                run_game_iteration(simulator, game_settings['seat_permutation'])

            # Run additional iterations if there's a draw
            while check_draw(simulator):
                run_game_iteration(simulator, game_settings['seat_permutation'])

            update_scores(scores, simulator, names)

            # Update match results for cross table
            update_match_results(match_results, simulator, player1, player2)

            simulator.print_stats()

        # Print cross table and leaderboard before removing a player
        print_cross_table(match_results)
        print_leaderboard(scores)

        removed_player = remove_worst_player(game_settings['players'], scores)
        removed_players.insert(0, removed_player)

    last_remaining_player = game_settings['players'][0]
    removed_players.insert(0, last_remaining_player)
    print_leaderboard(removed_players, final=True)

def run_game_iteration(simulator, seat_permutation):
    simulator.run_simulation()
    if seat_permutation:
        simulator.change_player_positions()
        simulator.run_simulation()

def check_draw(simulator):
    global_scores = simulator.get_global_score()
    # Assuming there are only two players in each game
    player_scores = list(global_scores.values())
    if len(player_scores) == 2 and player_scores[0] == player_scores[1]:
        return True  # It's a draw
    return False  # Not a draw

def update_scores(scores, simulator, names):
    # Update global scores for each player
    global_scores = simulator.get_global_score()
    for player_name, score in global_scores.items():
        scores[names[player_name]] += score

def remove_worst_player(players, scores):
    # Find the player with the lowest score
    lowest_score_player = min(players, key=lambda player: scores[player])
    players.remove(lowest_score_player)
    return lowest_score_player

def update_match_results(match_results, simulator, player1, player2):
    result = simulator.get_global_score()  # Assuming this method exists and returns the match result
    match_results[player1.get_name()][player2.get_name()] = result[player1.get_name()]
    match_results[player2.get_name()][player1.get_name()] = result[player2.get_name()]

def print_cross_table(match_results):
    print("\nCross Table:")
    player_names = sorted(match_results.keys())
    print(" " * 15 + " ".join(f"{name:<15}" for name in player_names))
    for name in player_names:
        results = [match_results[name].get(opponent, 'N/A') for opponent in player_names]
        print(f"{name:<15}" + " ".join(f"{result:<15}" for result in results))
    print()

def print_leaderboard(players, final=False):
    print("\n" + "=" * 60)
    title = "Final Leaderboard" if final else "Leaderboard"
    print("{:^40}".format(title))
    print("=" * 60)

    if final:
        for position, player in enumerate(players, start=1):
            print("{:2}. {:<40}".format(position, f"{player.get_name()} ({player.__class__.__name__})"))
    else:
        sorted_scores = sorted(players.items(), key=lambda x: x[1], reverse=True)
        for position, (player, score) in enumerate(sorted_scores, start=1):
            print("{:2}. {:<40} {:>5}".format(position, f"{player.get_name()} ({player.__class__.__name__})", score))

    print("=" * 60 + "\n")

def main():
    # Define a namedtuple for a Player
    Player = namedtuple('Player', ['name', 'type'])

    parser = argparse.ArgumentParser(description='Simulate a game with various settings.')

    # Mandatory game type argument
    parser.add_argument('--game', required=True, choices=AVAILABLE_GAME_TYPES.keys(),
                        help='Type of game to simulate. Choices are game1, game2, game3.')

    # Seat permutation (default: True)
    parser.add_argument('--seat-permutation', action='store_true', default=True,
                        help='Permute seats during the simulation. Defaults to True.')

    # Number of iterations (default: 1)
    parser.add_argument('--num-iterations', type=int, default=10000,
                        help='Number of iterations in the simulation. Defaults to 10000.')

    # Player argument. This should be specified at least twice.
    parser.add_argument('--player', action='append', nargs=2, metavar=('NAME', 'TYPE'),
                        help='Add a player with a name and type. Requires two values. This option should be specified at least twice.')

    args = parser.parse_args()

    # Check if at least two players are provided
    if args.player is None or len(args.player) < 2:
        parser.error('At least two --player arguments are required.')

    try:
        # Retrieve available player types for the selected game
        available_player_types = AVAILABLE_PLAYER_TYPES[args.game]
    except KeyError:
        parser.error(f"No player types available for the game '{args.game}'.")

    used_names = set()

    players = []
    for name, type_name in args.player:
        if name in used_names:
            parser.error(f"Duplicate player name '{name}' is not allowed.")

        used_names.add(name)

        # Find the player class that matches the provided type name
        player_class = None
        for cls in available_player_types:
            if cls.__name__ == type_name:
                player_class = cls
                break

        if player_class is None:
            parser.error(f"Player type '{type_name}' is not available for game '{args.game}'.")

        # Create a new player instance
        players.append(player_class(name))

    # Your logic to build the object with these arguments
    game_settings = {
        'game': AVAILABLE_GAME_TYPES[args.game],
        'seat_permutation': args.seat_permutation,
        'num_iterations': args.num_iterations,
        'players': players
    }

    run_simulation(game_settings)

if __name__ == '__main__':
    main()
