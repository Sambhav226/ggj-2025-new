from . import GameStates

from .MainMenu import MainMenu
from .PlayState import PlayState
from .OptionsMenu import OptionsMenu
from .GameOver import GameOver

class StateManager:
    # oh well, this looks susk wusky
    def __init__(self, gameSingleton):
        self.game = gameSingleton
        self.states = {GameStates.MAIN_MENU: MainMenu(self),
                       GameStates.PLAY: PlayState(self),
                       GameStates.OPTIONS: OptionsMenu(self),
                       GameStates.GAME_OVER: GameOver(self)}

        self.currentState = self.states[GameStates.MAIN_MENU]

    def changeState(self, newState: GameStates):
        self.currentState.exit()
        self.currentState = self.states[newState]
        self.currentState.enter()
