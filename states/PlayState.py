import pygame
from gameObjects import Bubbles, Blower
from settings import themes
from . import GameStates

class PlayState:
    def __init__(self, stateManager):
        self.stateManager = stateManager
        self.screen_rect = stateManager.game.surface.get_rect()
        self.gameObjects = {
            "bubble": Bubbles.Bubble(self),
            "blower": Blower.Blower(self.screen_rect)
        }

    def enter(self):
        # self.stateManager.game.theme = themes['gruvbox-dark']
        ...

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.stateManager.changeState(GameStates.MAIN_MENU)
        for obj in self.gameObjects.values():
            obj.handle_event(event)

    def update(self, dt):
        for obj in self.gameObjects.values():
            obj.update(dt)

    def render(self, surface):
        surface.fill(self.stateManager.game.theme["background"])
        for obj in self.gameObjects.values():
            obj.render(surface)

    def exit(self):
        pass