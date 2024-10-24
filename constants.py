import importlib
import os
import pkgutil
from inspect import isclass, getfile, getmodule
from pathlib import Path

from games.connect4.simulator import Connect4Simulator
from games.hlpoker.simulator import HLPokerSimulator
from games.minesweeper.simulator import MinesweeperSimulator

AVAILABLE_GAME_TYPES = {
    "hlpoker":      HLPokerSimulator,
    "connect4":     Connect4Simulator,
    "minesweeper":  MinesweeperSimulator
}


def __get_player_types(base_class):
    subclasses = []

    # Find the directory of the module where the base_class is defined
    base_class_module = getmodule(base_class)
    if not base_class_module:
        raise ValueError("Base class module could not be found")

    base_class_dir = Path(getfile(base_class_module)).parent
    base_module_name = base_class_module.__name__.rsplit('.', 1)[0]
    players_dir = base_class_dir / 'players'

    # Check if the players subfolder exists
    if not players_dir.is_dir():
        raise ValueError(f"No 'players' subfolder found in {base_class_dir}")

    # Recursively walk through the players directory and import modules
    for importer, modname, ispkg in pkgutil.walk_packages(path=[str(players_dir)], prefix=base_module_name + '.players.'):
        try:
            module = importlib.import_module(modname)
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isclass(attribute) and issubclass(attribute, base_class) and attribute is not base_class:
                    subclasses.append(attribute)
        except ImportError:
            continue  # Skip modules that can't be imported

    return subclasses

def __build_available_player_types():
    ret = {}
    for game_type in AVAILABLE_GAME_TYPES:
        simulator_type = AVAILABLE_GAME_TYPES[game_type]
        ret[game_type] = __get_player_types(simulator_type.get_player_type())
    return ret


"""
The available player classes
"""
AVAILABLE_PLAYER_TYPES = __build_available_player_types()