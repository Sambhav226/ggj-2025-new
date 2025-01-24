import pygame_gui as pg
import pygame

from . import GameStates
from settings import themes

class OptionsMenu:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.ui_manager = state_manager.game.uiManager
        self.ui_elements = {}

        # Create a dropdown to select themes
        self.ui_elements['theme_dropdown'] = pg.elements.UIDropDownMenu(
            options_list=list(themes.keys()),  # List of theme names
            starting_option="gruvbox-dark",  # Default selection
            relative_rect=pygame.Rect(50, 50, 200, 30),
            visible=False,
            manager=self.ui_manager
        )

    def handle_event(self, event):
        if event.type == pg.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.ui_elements['theme_dropdown']:
                self.state_manager.game.theme = themes[event.text]
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state_manager.changeState(GameStates.MAIN_MENU)

    def enter(self):
        for element in self.ui_elements.values():
            element.show()

    def exit(self):
        for element in self.ui_elements.values():
            element.hide()

    def update(self, dt):
        pass

    def render(self, surface):
        pass
