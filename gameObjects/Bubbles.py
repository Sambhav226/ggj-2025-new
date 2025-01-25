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
            "positive": ["growth", "profit", "success"],
            "negative": ["scam", "fake", "fraud"],
            "risky": ["investment", "speculation", "boom"]
        }

        # Set bubble size relative to screen dimensions
        self.base_radius = int(self.screen_rect.width * 0.02)  # 2% of screen width
        self.min_radius = int(self.screen_rect.width * 0.015)  # Minimum size
        self.max_radius = int(self.screen_rect.width * 0.03)   # Maximum size

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

        # Check for collisions and deflect bubbles
        self.handle_collisions()

        # Remove bubbles that go out of bounds (above the top of the screen)
        for bubble in self.bubbles[:]:
            if bubble["position"].y + bubble["radius"] < 0:
                self.bubbles.remove(bubble)

    def handle_collisions(self):
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
            # Draw bubble with a border for better aesthetics
            pygame.draw.circle(surface, bubble["color"], (int(bubble["position"].x), int(bubble["position"].y)), bubble["radius"])
            pygame.draw.circle(surface, (255, 255, 255), (int(bubble["position"].x), int(bubble["position"].y)), bubble["radius"], 2)  # White border

            # Render text inside the bubble
            font_size = int(bubble["radius"] * 1.2)  # Adjust font size based on bubble size
            font = pygame.font.Font(None, font_size)
            text = font.render(bubble["keyword"], True, (0, 0, 0))  # Black text for contrast
            text_rect = text.get_rect(center=(int(bubble["position"].x), int(bubble["position"].y)))

            surface.blit(text, text_rect)

    def handle_event(self, event):
        pass  # No event handling needed for bubbles
            