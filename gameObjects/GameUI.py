import pygame_gui
from pygame import Rect # oh dear dear pygame_gui
from pygame_gui.elements import UITextBox

class News:
    def __init__(self, stateManager):
        self.surfaceRect = stateManager.game.surface.get_rect()
        newsStripRect = Rect(0, -self.surfaceRect.height * 0.24,
                            self.surfaceRect.width * 0.995,
                            self.surfaceRect.height * 0.20)
        self.newsStrip = UITextBox(relative_rect=newsStripRect,
                              html_text='Economy is <effect id=hu><font color=#ff0000>stable</font><effect>',
                              visible=False,
                              manager=stateManager.game.uiManager,
                              anchors={'centerx': 'centerx',
                                       'bottom': 'bottom'})
        self.newsStrip.set_active_effect(pygame_gui.TEXT_EFFECT_BOUNCE, effect_tag='hu')
    
    def update_news(self, news_text):
        self.newsStrip.set_text(news_text)
    
    def showUI(self):
        self.newsStrip.show()

    def update(self, dt):
        pass

    def render(self, surface):
        pass

    def handle_event(self, event):
        pass

    def hideUI(self):
        # self.newsStrip.set_active_effect(None)
        self.newsStrip.hide()

    