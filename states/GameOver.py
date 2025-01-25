import pygame
import pygame_gui as pg
from . import GameStates

class GameOver:
    def __init__(self, stateManager):
        self.stateManager = stateManager
        self.uiElements = {}

        screen_width = stateManager.game.surface.get_width()
        screen_height = stateManager.game.surface.get_height()

        # Create a "Retry" button
        self.uiElements['retry'] = pg.elements.UIButton(
            relative_rect=pygame.Rect((screen_width // 2 - 100, screen_height // 2 - 50), (200, 50)),  # Center the button
            text="Retry",
            manager=stateManager.game.uiManager,
            anchors={'centerx': 'centerx'},
            visible=False
        )

        # Create a "Main Menu" button
        self.uiElements['main_menu'] = pg.elements.UIButton(
            relative_rect=pygame.Rect((screen_width // 2 - 100, screen_height // 2 + 50), (200, 50)),  # Position below the Retry button
            text="Main Menu",
            manager=stateManager.game.uiManager,
            anchors={'centerx': 'centerx'},
            visible=False
        )

    def handle_event(self, event):
        """Handle button clicks."""
        if event.type == pg.UI_BUTTON_PRESSED:
            if event.ui_element == self.uiElements['retry']:
                # Restart the game by transitioning to the PLAY state
                self.stateManager.changeState(GameStates.PLAY)
            elif event.ui_element == self.uiElements['main_menu']:
                # Return to the main menu by transitioning to the MAIN_MENU state
                self.stateManager.changeState(GameStates.MAIN_MENU)

    def enter(self):
        """Show the buttons when entering the GameOver state."""
        print("Entering GameOver state")  # Debug print
        for element in self.uiElements.values():
            element.show()
            print(f"Button shown: {element.text}")  # Debug print to confirm buttons are shown

    def exit(self):
        """Hide the buttons when exiting the GameOver state."""
        for element in self.uiElements.values():
            element.hide()

    def update(self, dt):
        """Update the UI manager."""
        self.stateManager.game.uiManager.update(dt)  # Update the UI manager

    def render(self, surface):
        """Render the GameOver screen."""
        surface.fill(self.stateManager.game.theme["background"])
        
        # Display "Game Over!" text
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over!", True, (255, 0, 0))  # Red text
        text_rect = text.get_rect(center=surface.get_rect().center)
        surface.blit(text, text_rect)

        # Draw the UI elements
        self.stateManager.game.uiManager.draw_ui(surface)