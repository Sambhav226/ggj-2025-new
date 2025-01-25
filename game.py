import pygame
import pygame_gui

from settings import gameSettings
from states import StateManager

class Game:
    def __init__(self):
        self.title = "GGJ 2025"
        self.running = True
        pygame.display.set_caption(self.title)
        pygame.init()
        gameSettings["resolution"] = pygame.display.get_desktop_sizes()[0]
        self.surface = pygame.display.set_mode(size=gameSettings["resolution"])
        self.clock  = pygame.time.Clock()
        self.refreshRate = pygame.display.get_current_refresh_rate()
        self.dt = 0.0
        self.theme = gameSettings["theme"]
        
        self.uiManager = pygame_gui.UIManager(gameSettings["resolution"])

        self.stateManager = StateManager(self)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.stateManager.currentState.handle_event(event)
            self.uiManager.process_events(event)

    def update(self):
        self.stateManager.currentState.update(self.dt)
        self.uiManager.update(self.dt)

    def render(self):
        self.surface.fill(self.theme["background"])
        self.uiManager.draw_ui(self.surface)
        self.stateManager.currentState.render(self.surface)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_event()
            self.update()
            self.render()

            self.dt = self.clock.tick(self.refreshRate) / 1000.0
        pygame.quit()