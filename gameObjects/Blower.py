import pygame
from pygame.math import Vector2
import math

class Blower:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.position = Vector2(screen_rect.centerx, screen_rect.centery)  # Start at the center
        self.target_position = Vector2(screen_rect.centerx, screen_rect.centery)  # Target position (mouse position)
        self.size = Vector2(100, 100)  # Size of the blower (width, height)
        self.angle = 0  # Current rotation angle
        self.rotation_speed = 5  # Degrees per frame
        self.scale_factor = 1.0  # Initial scale factor
        self.min_scale = 0.5  # Minimum scale factor
        self.max_scale = 2.0  # Maximum scale factor
        self.follow_speed = 0.1  # Speed at which the blower follows the mouse (lower = more delay)

        # Load the blower image (fan image)
        self.image = pygame.image.load("fan.png")  # Replace with your PNG file path
        self.image = pygame.transform.scale(self.image, self.size)  # Resize to initial size
        self.rect = self.image.get_rect(center=self.position)  # Initial position

    def update(self, dt):
        """Update the blower's position to follow the mouse with a delay and rotate."""
        # Smoothly interpolate the blower's position toward the target position (mouse position)
        self.position += (self.target_position - self.position) * self.follow_speed

        # Keep the blower within the screen bounds
        self.position.x = max(self.size.x // 2, min(self.position.x, self.screen_rect.width - self.size.x // 2))
        self.position.y = max(self.size.y // 2, min(self.position.y, self.screen_rect.height - self.size.y // 2))

        # Update blower angle for rotation
        self.angle += self.rotation_speed
        if self.angle >= 360:  # Keep angle within 0-359 degrees
            self.angle -= 360

    def render(self, surface):
        """Draw the blower on the screen."""
        # Scale the blower image
        scaled_image = pygame.transform.smoothscale(
            self.image,
            (int(self.size.x * self.scale_factor), int(self.size.y * self.scale_factor))
        )
        # Rotate the scaled blower image
        rotated_image = pygame.transform.rotate(scaled_image, -self.angle)  # Negative angle for clockwise rotation
        # Get the new rect with the same center as the original image
        rotated_rect = rotated_image.get_rect(center=self.position)
        # Draw the rotated and scaled blower
        surface.blit(rotated_image, rotated_rect.topleft)

    def handle_event(self, event):
        """Handle mouse events to update the target position and scaling."""
        if event.type == pygame.MOUSEMOTION:
            # Update the target position to the mouse position
            self.target_position = Vector2(event.pos)
        elif event.type == pygame.MOUSEWHEEL:  # Handle mouse wheel for scaling
            if event.y > 0:  # Scroll up
                self.scale_factor = min(self.scale_factor + 0.1, self.max_scale)  # Increase scale
            elif event.y < 0:  # Scroll down
                self.scale_factor = max(self.scale_factor - 0.1, self.min_scale)  # Decrease scale

    def apply_blow_force(self, bubbles):
        """Apply a blowing force to nearby bubbles."""
        for bubble in bubbles:
            # Calculate the distance between the blower and the bubble
            distance = self.position.distance_to(bubble["position"])
            if distance < 100:  # Only affect bubbles within a certain range
                # Calculate the direction of the force
                direction = (bubble["position"] - self.position).normalize()
                # Apply the force to the bubble's velocity
                bubble["speed"] += direction * 50 * (1 - distance / 100)  # Adjust blow strength as needed