import pygame
from game import Bubbles
from game import Blower

from settings import themes
from . import GameStates

class PlayState:
    def __init__(self, stateManager):
        self.stateManager = stateManager

    def enter(self):
        self.stateManager.game.theme = themes['gruvbox-dark']

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.stateManager.changeState(GameStates.MAIN_MENU)

    def update(self, dt):
        ...

    def render(self, surface):
        ...

    def exit(self):
        ...
