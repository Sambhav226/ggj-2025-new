# File: /states/PlayState.py

import pygame
from gameObjects import Bubbles, Blower, GameUI, EconomyBubble
from settings import themes
from . import GameStates

class PlayState:
    def __init__(self, stateManager):
        self.stateManager = stateManager
        self.screen_rect = stateManager.game.surface.get_rect()
        self.reset()  # Initialize game objects

    def reset(self):
        """Reset the game state."""
        self.gameObjects = {
            "bubble": Bubbles.Bubble(self),
            "blower": Blower.Blower(self.screen_rect),
            "economy": EconomyBubble.EconomyBubble(self.screen_rect, self.stateManager)
        }
        self.gameUI = {
            'newsStrip': GameUI.News(self.stateManager)
        }

    def enter(self):
        """Reset the game state when entering the PlayState."""
        self.reset()
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
        # Render game objects
        for obj in self.gameObjects.values():
            obj.render(surface)

        # Render UI elements
        for UIobj in self.gameUI.values():
            UIobj.render(surface)

        # Render stability bar
        self._render_stability_bar(surface)

        # Render score below the stability bar
        self._render_score(surface)

    def _render_stability_bar(self, surface):
        """Render the stability bar on the right side of the screen."""
        bar_width = 20
        bar_height = self.screen_rect.height * 0.8
        bar_x = self.screen_rect.width - bar_width - 10
        bar_y = self.screen_rect.height * 0.1

        # Draw the background of the stability bar
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        # Draw the current stability level
        stability_height = bar_height * (self.gameObjects["economy"].instability / self.gameObjects["economy"].max_instability)
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y + bar_height - stability_height, bar_width, stability_height))

    def _render_score(self, surface):
        """Render the score below the stability bar."""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.gameObjects['economy'].score}", True, (255, 255, 255))
        score_x = self.screen_rect.width - 100
        score_y = self.screen_rect.height * 0.9
        surface.blit(score_text, (score_x, score_y))

    def exit(self):
        for ui in self.gameUI.values():
            ui.hideUI()