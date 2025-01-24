import pygame
from settings import themes, gameSettings

class Blower:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.position = pygame.Vector2(self.screen_rect.centerx, self.screen_rect.centery)
        self.size = int(self.screen_rect.width * 0.05)  # Size relative to screen width (5%)
        self.theme = gameSettings["theme"]
        self.color = pygame.Color(self.theme["buttons"]["primary"])  # Use primary color from the theme

    def update(self, dt):
        # Update the blower's position to follow the mouse
        self.position.x, self.position.y = pygame.mouse.get_pos()

        # Ensure the blower stays within the screen bounds
        self.position.x = max(self.size // 2, min(self.position.x, self.screen_rect.width - self.size // 2))
        self.position.y = max(self.size // 2, min(self.position.y, self.screen_rect.height - self.size // 2))

    def render(self, surface):
        # Draw the square blower
        pygame.draw.rect(
            surface,
            self.color,
            (int(self.position.x - self.size // 2), int(self.position.y - self.size // 2), self.size, self.size)
        )

    def handle_event(self, event):
        pass  # No event handling needed for now