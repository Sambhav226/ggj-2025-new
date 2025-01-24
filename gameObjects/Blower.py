import pygame
from pygame.math import Vector2

class Blower:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.position = Vector2(screen_rect.centerx, screen_rect.centery)  # Start at the center
        self.target_position = Vector2(screen_rect.centerx, screen_rect.centery)  # Target position (mouse position)
        self.size = 50  # Size of the blower
        self.blow_strength = 50  # Strength of the blowing force
        self.color = (0, 255, 0)  # Green color for the blower
        self.speed = 2  # Speed at which the blower follows the mouse (lower = more delay)
        self.delay_factor = 0.1  # Delay factor for smoother movement

    def update(self, dt):
        """Update the blower's position to follow the mouse with a delay."""
        # Smoothly interpolate the blower's position toward the target position (mouse position)
        self.position += (self.target_position - self.position) * self.delay_factor

        # Keep the blower within the screen bounds
        self.position.x = max(self.size // 2, min(self.position.x, self.screen_rect.width - self.size // 2))
        self.position.y = max(self.size // 2, min(self.position.y, self.screen_rect.height - self.size // 2))

    def apply_blow_force(self, bubbles):
        """Apply a blowing force to nearby bubbles."""
        for bubble in bubbles:
            # Calculate the distance between the blower and the bubble
            distance = self.position.distance_to(bubble["position"])
            if distance < 100:  # Only affect bubbles within a certain range
                # Calculate the direction of the force
                direction = (bubble["position"] - self.position).normalize()
                # Apply the force to the bubble's velocity
                bubble["speed"] += direction * self.blow_strength * (1 - distance / 100)

    def render(self, surface):
        """Draw the blower on the screen."""
        pygame.draw.rect(
            surface,
            self.color,
            (int(self.position.x - self.size // 2), int(self.position.y - self.size // 2), self.size, self.size)
        )

    def handle_event(self, event):
        """Handle mouse events to update the target position."""
        if event.type == pygame.MOUSEMOTION:
            # Update the target position to the mouse position
            self.target_position = Vector2(event.pos)