import pygame
import random
import math
from settings import themes, gameSettings

class Bubble:
    def __init__(self, currentState):
        self.stateManager = currentState.stateManager
        self.screen_rect = self.stateManager.game.surface.get_rect()
        self.bubbles = []
        self.spawn_timer = 0
        self.spawn_interval = 1000  # Spawn a bubble every 1 second
        self.keywords = {
            "positive": ["growth", "profit", "success", "innovation", "stability"],
            "negative": ["scam", "fake", "fraud", "collapse", "bankruptcy"],
            "risky": ["investment", "speculation", "boom", "volatility", "leverage"],
            "stable": ["regulation", "safety", "security", "balance"]
        }

        # Set bubble size relative to screen dimensions
        self.base_radius = int(self.screen_rect.width * 0.02)  # 2% of screen width
        self.min_radius = int(self.screen_rect.width * 0.015)  # Minimum size
        self.max_radius = int(self.screen_rect.width * 0.03)   # Maximum size

        # Border properties
        self.border_width = 10  # Width of the border

        self.effects = {'collide': pygame.mixer.Sound('assets/audio/bubblecollide.wav')}

    def spawn_bubble(self):
        category = random.choice(list(self.keywords.keys()))
        keyword = random.choice(self.keywords[category])
        radius = random.randint(self.min_radius, self.max_radius)  # Random size within range
        speed = random.uniform(50, 150)  # Vertical speed
        horizontal_speed = random.uniform(-50, 50)  # Horizontal speed (random drift)

        # Ensure bubbles don't spawn too close to the edges
        position = pygame.Vector2(
            random.randint(radius, self.screen_rect.width - radius),  # X position
            self.screen_rect.height + radius  # Y position (start below the screen)
        )

        self.bubbles.append({
            "keyword": keyword,
            "category": category,
            "position": position,
            "speed": pygame.Vector2(horizontal_speed, -speed),  # Use Vector2 for velocity
            "radius": radius,
            "color": self._get_color_based_on_category(category)
        })

    def _get_color_based_on_category(self, category):
        # Use the theme's button colors for bubbles
        if category == "positive":
            return pygame.Color(self.stateManager.game.theme["buttons"]["success"])  # Green for positive
        elif category == "negative":
            return pygame.Color(self.stateManager.game.theme["buttons"]["danger"])  # Red for negative
        elif category == "risky":
            return pygame.Color(self.stateManager.game.theme["buttons"]["warning"])  # Yellow for risky
        else:
            return pygame.Color(self.stateManager.game.theme["buttons"]["primary"])  # Blue for default

    def update(self, dt):
        self.spawn_timer += dt * 1000
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_bubble()
            self.spawn_timer = 0

        # Update bubble positions
        for bubble in self.bubbles:
            bubble["position"] += bubble["speed"] * dt

        # Check for collisions with borders and other bubbles
        self.handle_collisions()

        # Remove bubbles that go out of bounds (above the top of the screen)
        for bubble in self.bubbles[:]:
            if bubble["position"].y + bubble["radius"] < 0:
                self.bubbles.remove(bubble)

    def handle_collisions(self):
        # Check for collisions with left and right borders
        for bubble in self.bubbles:
            if bubble["position"].x - bubble["radius"] < self.border_width:  # Left border collision
                bubble["position"].x = self.border_width + bubble["radius"]
                bubble["speed"].x *= -1  # Reverse horizontal speed
            elif bubble["position"].x + bubble["radius"] > self.screen_rect.width - self.border_width:  # Right border collision
                bubble["position"].x = self.screen_rect.width - self.border_width - bubble["radius"]
                bubble["speed"].x *= -1  # Reverse horizontal speed

        # Check all pairs of bubbles for collisions
        for i in range(len(self.bubbles)):
            for j in range(i + 1, len(self.bubbles)):
                bubble1 = self.bubbles[i]
                bubble2 = self.bubbles[j]

                # Calculate the distance between the centers of the two bubbles
                distance = bubble1["position"].distance_to(bubble2["position"])
                min_distance = bubble1["radius"] + bubble2["radius"]

                if distance < min_distance:
                    self.effects['collide'].play()
                    # Bubbles are colliding, so deflect them
                    self.deflect_bubbles(bubble1, bubble2)

    def deflect_bubbles(self, bubble1, bubble2):
        # Calculate the collision normal (direction vector between centers)
        normal = (bubble2["position"] - bubble1["position"]).normalize()

        # Calculate the relative velocity
        relative_velocity = bubble2["speed"] - bubble1["speed"]

        # Calculate the velocity along the normal
        velocity_along_normal = relative_velocity.dot(normal)

        # If bubbles are moving towards each other, deflect them
        if velocity_along_normal < 0:
            # Calculate the impulse (change in velocity)
            impulse = -(1 + 0.8) * velocity_along_normal  # 0.8 is the coefficient of restitution (bounciness)

            # Apply the impulse to the bubbles' velocities
            bubble1["speed"] -= impulse * normal
            bubble2["speed"] += impulse * normal

    def render(self, surface):
        for bubble in self.bubbles:
            # Main bubble surface
            radius = bubble["radius"]
            bubble_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            
            # Draw translucent bubble body
            pygame.draw.circle(bubble_surface, bubble["color"], (radius, radius), radius)

            # Primary highlight (larger, subtle)
            highlight_main = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            highlight_color = (255, 255, 255, 160)  # More transparent
            pygame.draw.ellipse(highlight_main, highlight_color, (
                radius * 0.7,  # X offset (right side)
                radius * 0.15,  # Y offset
                radius * 0.6,   # Width
                radius * 0.3    # Height
            ))
            # Rotate and blend primary highlight
            rotated_main = pygame.transform.rotate(highlight_main, 45)
            bubble_surface.blit(rotated_main, rotated_main.get_rect(center=(radius, radius)))

            # Secondary highlight (smaller, brighter)
            highlight_secondary = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.ellipse(highlight_secondary, (255, 255, 255, 220), (
                radius * 0.8,  # Closer to edge
                radius * 0.25,
                radius * 0.4,
                radius * 0.15
            ))
            # Rotate and position secondary highlight
            rotated_secondary = pygame.transform.rotate(highlight_secondary, 35)
            bubble_surface.blit(rotated_secondary, rotated_secondary.get_rect(center=(radius, radius)))

            # Thin glossy border (top half)
            border_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.arc(border_surface, (255, 255, 255, 100), 
                        (0, 0, radius*2, radius*2), 
                        -3.14/2, 3.14/2, 2)  # Top half arc
            bubble_surface.blit(border_surface, (0, 0))

            # Dynamic border shine (bottom subtle)
            pygame.draw.circle(bubble_surface, (255, 255, 255, 30), 
                            (radius, radius), radius, 2)

            # Text rendering with shadow
            font_size = int(radius * 0.7)
            font = pygame.font.Font(None, font_size)
            
            # Text shadow
            text_shadow = font.render(bubble["keyword"], True, (0, 0, 0, 100))
            shadow_rect = text_shadow.get_rect(center=(radius+1, radius+1))
            bubble_surface.blit(text_shadow, shadow_rect)
            
            # Main text
            text = font.render(bubble["keyword"], True, (10, 10, 10, 240))
            text_rect = text.get_rect(center=(radius, radius))
            bubble_surface.blit(text, text_rect)

            # Final blit to main surface
            surface.blit(bubble_surface, 
                        bubble["position"] - pygame.Vector2(radius, radius))

    def handle_event(self, event):
        pass  # No event handling needed for bubbles