import pygame_gui as pg
import pygame
from . import GameStates
#from .BaseState import BaseState

class MainMenu():
    def __init__(self, stateManager):
        self.stateManager = stateManager
        self.uiElements = {}
        self.uiElements['startButton'] = pg.elements.UIButton(relative_rect=pygame.Rect(0, 30, 100, 20),
                                                              text="Start Game",
                                                              manager=stateManager.game.uiManager,
                                                              anchors={'centerx': 'centerx'},
                                                              )
        self.uiElements['option'] = pg.elements.UIButton(relative_rect=pygame.Rect(0, 60, 100, 20),
                                                         text="Options",
                                                         manager=stateManager.game.uiManager,
                                                         anchors={'centerx': 'centerx'},
                                                         )


    def enter(self):
        for element in self.uiElements.values():
            element.show()

    def handle_event(self, event):
        if event.type == pg.UI_BUTTON_PRESSED:
            if event.ui_element == self.uiElements['startButton']:
                print('Changing State to play')
                self.stateManager.changeState(GameStates.PLAY)
            if event.ui_element == self.uiElements['option']:
                print('Changing State to options')
                self.stateManager.changeState(GameStates.OPTIONS)


    def update(self, dt):
        ...

    def render(self, surface):
        ...

    def exit(self):
        for element in self.uiElements.values():
            element.hide()
