import pygame_gui as pg
import pygame
from . import GameStates
#from .BaseState import BaseState

class MainMenu():
    def __init__(self, stateManager):
        self.stateManager = stateManager
        self.game_rect = stateManager.game.surface.get_rect()
        self.uiElements = {}
        startButtonRect = pygame.Rect(0, 30, 
                                      self.game_rect.width * 0.2, 
                                      self.game_rect.height * 0.1)
        self.uiElements['startButton'] = pg.elements.UIButton(relative_rect=startButtonRect,
                                                              text="Start Game",
                                                              manager=stateManager.game.uiManager,
                                                              anchors={'centerx': 'centerx',
                                                                       'centery': 'centery'},
                                                              )
        optionButtonRect = pygame.Rect(0, 150, self.game_rect.width * 0.2, self.game_rect.height * 0.1)
        self.uiElements['option'] = pg.elements.UIButton(relative_rect=optionButtonRect,
                                                         text="Options",
                                                         manager=stateManager.game.uiManager,
                                                         anchors={'centerx': 'centerx',
                                                                  'centery': 'centery'}
                                                         )
        pygame.mixer.music.load("assets/audio/mainmenu.ogg")


    def enter(self):
        pygame.mixer.music.play(loops=-1, fade_ms=1000)
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
        pygame.mixer.music.fadeout(500)
        for element in self.uiElements.values():
            element.hide()
