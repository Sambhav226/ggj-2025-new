import pygame
from pygame.math import Vector2
from states import GameStates, StateManager

class EconomyBubble:
    def __init__(self, screen_rect, stateManager):  # stateManager is passed as a parameter
        self.screen_rect = screen_rect
        self.stateManager = stateManager  # Ensure this line exists
        self.position = Vector2(screen_rect.centerx, screen_rect.centery)
        self.radius = 100
        self.max_radius = 150
        self.growth_rate = 5
        self.color = (255, 0, 0)
        self.effects = {
            'pop': pygame.mixer.Sound('assets/audio/bubblepop.wav'),
            'death': pygame.mixer.Sound('assets/audio/death.wav')
        }
        self.bursting = False

    def update(self, bubbles):
        """Check for collisions with keyword bubbles and grow/shrink accordingly."""
        if self.bursting:
            return  # Do nothing if the bubble is bursting

        for bubble in bubbles[:]:  # Iterate over a copy of the list
            # Calculate the distance between the economy bubble and the keyword bubble
            distance = self.position.distance_to(bubble["position"])
            if distance < self.radius + bubble["radius"]:  # Collision detected
                # Merge the keyword bubble into the economy bubble
                self.radius += self.growth_rate
                bubbles.remove(bubble)  # Remove the keyword bubble
                self.effects['pop'].play()

                # Check if the economy bubble has burst
                if self.radius > self.max_radius:
                    self.burst()

    def burst(self):
        """Handle the bursting of the economy bubble (game over)."""
        self.bursting = True
        self.effects['death'].play()
        self.stateManager.changeState(GameStates.GAME_OVER)  # Transition to game over state

    def render(self, surface):
        """Draw the economy bubble on the screen."""
        if not self.bursting:
            pygame.draw.circle(
                surface,
                self.color,
                (int(self.position.x), int(self.position.y)),
                int(self.radius)
            )
        else:
            # Optionally, you can add an animation or effect here for the bursting
            pass

    def handle_event(self, event):
        pass  # No event handling needed for bubbles