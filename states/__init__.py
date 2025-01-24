from enum import Enum, auto

class GameStates(Enum):
    MAIN_MENU = auto()
    PLAY = auto()
    PAUSE = auto()
    OPTIONS = auto()
    GAME_OVER = auto()

from .StateManager import StateManager

__all__ = ['GameStates', 'StateManager']
