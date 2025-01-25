import pygame
from pygame.math import Vector2

class EconomyBubble:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.position = Vector2(screen_rect.centerx, screen_rect.centery)  # Center of the screen
        self.radius = 100  # Initial radius
        self.max_radius = 150  # Maximum size before bursting
        self.growth_rate = 5  # How much the bubble grows when a keyword bubble merges
        self.color = (255, 0, 0)  # Red color for the economy bubble

        self.effects = {
            'pop': pygame.mixer.Sound('assets/audio/bubblepop.wav'),
            'death': pygame.mixer.Sound('assets/audio/death.wav')
        }

    def update(self, bubbles):
        """Check for collisions with keyword bubbles and grow/shrink accordingly."""
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
        self.effects['death'].play()
        print("Game Over! The economy bubble burst.")
        # You can trigger a game over state here

    def render(self, surface):
        """Draw the economy bubble on the screen."""
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.position.x), int(self.position.y)),
            int(self.radius)
        )
        
    def handle_event(self, event):
        pass  # No event handling needed for bubbles
            