import pygame
import random
from settings import themes, gameSettings

class Bubble:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.bubbles = []
        self.spawn_timer = 0
        self.spawn_interval = 1000  # Spawn a bubble every 1 second
        self.keywords = {
            "positive": ["growth", "profit", "success"],
            "negative": ["scam", "fake", "fraud"],
            "risky": ["investment", "speculation", "boom"]
        }
        self.theme = gameSettings["theme"]

        # Set bubble size relative to screen dimensions
        self.base_radius = int(self.screen_rect.width * 0.02)  # 2% of screen width
        self.min_radius = int(self.screen_rect.width * 0.015)  # Minimum size
        self.max_radius = int(self.screen_rect.width * 0.03)   # Maximum size

    def spawn_bubble(self):
        category = random.choice(list(self.keywords.keys()))
        keyword = random.choice(self.keywords[category])
        position = (random.randint(0, self.screen_rect.width), self.screen_rect.height)
        speed = random.uniform(50, 150)
        radius = random.randint(self.min_radius, self.max_radius)  # Random size within range
        self.bubbles.append({
            "keyword": keyword,
            "category": category,
            "position": pygame.Vector2(position),
            "speed": speed,
            "radius": radius,
            "color": self._get_color_based_on_category(category)
        })

    def _get_color_based_on_category(self, category):
        # Use the theme's button colors for bubbles
        if category == "positive":
            return pygame.Color(self.theme["buttons"]["success"])  # Green for positive
        elif category == "negative":
            return pygame.Color(self.theme["buttons"]["danger"])  # Red for negative
        elif category == "risky":
            return pygame.Color(self.theme["buttons"]["warning"])  # Yellow for risky
        else:
            return pygame.Color(self.theme["buttons"]["primary"])  # Blue for default

    def update(self, dt):
        self.spawn_timer += dt * 1000
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_bubble()
            self.spawn_timer = 0

        # Update bubble positions and remove out-of-bounds bubbles
        for bubble in self.bubbles[:]:  # Iterate over a copy of the list to safely remove items
            bubble["position"].y -= bubble["speed"] * dt  # Move upwards

            # Remove bubbles that go out of bounds (above the top of the screen)
            if bubble["position"].y + bubble["radius"] < 0:
                self.bubbles.remove(bubble)

    def render(self, surface):
        for bubble in self.bubbles:
            pygame.draw.circle(surface, bubble["color"], (int(bubble["position"].x), int(bubble["position"].y)), bubble["radius"])
            font = pygame.font.Font(None, int(bubble["radius"] * 1.5))  # Font size relative to bubble size
            text = font.render(bubble["keyword"], True, (0, 0, 0))  # Black text for contrast
            text_rect = text.get_rect(center=(int(bubble["position"].x), int(bubble["position"].y)))
            surface.blit(text, text_rect)

    def handle_event(self, event):
        pass  # No event handling needed for bubbles