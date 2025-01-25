import pygame
from gameObjects import Bubbles, Blower, GameUI, EconomyBubble
from settings import themes
from . import GameStates

class PlayState:
    def __init__(self, stateManager):
        self.stateManager = stateManager
        self.screen_rect = stateManager.game.surface.get_rect()
        self.gameObjects = {
            "bubble": Bubbles.Bubble(self),
            "blower": Blower.Blower(self.screen_rect),
            "economy": EconomyBubble.EconomyBubble(self.screen_rect)
        }
        self.gameUI = {
            'newsStrip': GameUI.News(stateManager)
        }

    def enter(self):
        # self.stateManager.game.theme = themes['gruvbox-dark']
        for ui in self.gameUI.values():
            ui.showUI()

    def update(self, dt):
        """Update all game objects."""
        # Update the blower to follow the mouse with a delay
        self.gameObjects["blower"].update(dt)  # Only pass `dt` (no `keys` argument)

        # Apply blowing force to nearby bubbles
        self.gameObjects["blower"].apply_blow_force(self.gameObjects["bubble"].bubbles)

        # Update the economy bubble (check for collisions with keyword bubbles)
        self.gameObjects["economy"].update(self.gameObjects["bubble"].bubbles)

        # Update the keyword bubbles
        self.gameObjects["bubble"].update(dt)

    def handle_event(self, event):
        """Handle events like mouse input."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.stateManager.changeState(GameStates.MAIN_MENU)
        # Pass mouse events to the blower
        self.gameObjects["blower"].handle_event(event)

    def render(self, surface):
        # surface.fill(self.stateManager.game.theme["background"])
        for obj in self.gameObjects.values():
            obj.render(surface)
        for UIobj in self.gameUI.values():
            UIobj.render(surface)

    def exit(self):
        for ui in self.gameUI.values():
            ui.hideUI()