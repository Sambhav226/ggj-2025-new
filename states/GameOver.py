import pygame
import pygame_gui as pg
from . import GameStates

class GameOver:
    def __init__(self, stateManager):
        self.stateManager = stateManager
        self.uiElements = {}
        self.uiElements['retry'] = pg.elements.UIButton(
            relative_rect=pygame.Rect(0, 100, 200, 50),
            text="Retry",
            manager=stateManager.game.uiManager,
            anchors={'centerx': 'centerx'}
        )

    def handle_event(self, event):
        if event.type == pg.UI_BUTTON_PRESSED:
            if event.ui_element == self.uiElements['retry']:
                self.stateManager.changeState(GameStates.PLAY)

    def enter(self):
        self.uiElements['retry'].show()

    def exit(self):
        self.uiElements['retry'].hide()

    def update(self, dt):
        pass

    def render(self, surface):
        surface.fill(self.stateManager.game.theme["background"])
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over!", True, (255, 0, 0))
        text_rect = text.get_rect(center=surface.get_rect().center)
        surface.blit(text, text_rect)