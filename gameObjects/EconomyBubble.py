import pygame
import math
from pygame.math import Vector2
from random import randint
from settings import themes, gameSettings
from states import GameStates


class EconomyBubble:
    def __init__(self, screen_rect, stateManager):
        self.screen_rect = screen_rect
        self.stateManager = stateManager
        self.position = Vector2(screen_rect.centerx, screen_rect.centery)
        
        # Bubble properties
        self.target_radius = 100
        self.radius = self.target_radius
        self.max_radius = 150
        self.min_radius = 50  # Minimum size for the bubble
        self.growth_rate = 5
        self.base_color = pygame.Color(98, 114, 164)
        self.color = pygame.Color(self.base_color)
        self.pulse_speed = 0.5
        self.pulse_phase = 0
        
        # Instability properties
        self.instability = 0  # Instability meter (0 to 100)
        self.max_instability = 100  # Max instability before bursting
        self.instability_growth_rate = 5  # Instability increase per risky bubble
        self.instability_decay_rate = 10  # Instability decrease per stable bubble

        # Score
        self.score = 0  # Player's score

        # Sound effects
        self.effects = {
            'pop': pygame.mixer.Sound('assets/audio/bubblepop.wav'),
            'death': pygame.mixer.Sound('assets/audio/death.wav'),
        }
        for sound in self.effects.values():
            sound.set_volume(0.5)
            
        # Animation states
        self.bursting = False
        self.burst_radius = 0
        self.burst_particles = []
        self.warning_activated = False

    @staticmethod
    def _ease_out_sine(t):
        """Custom implementation of easeOutSine easing function"""
        return math.sin(t * (math.pi / 2))

    def update(self, bubbles):
        if self.bursting:
            self._update_burst_animation()
            return

        # Smooth size transition
        self.radius += (self.target_radius - self.radius) * 0.1
        self.pulse_phase = (self.pulse_phase + self.pulse_speed) % 360

        # Dynamic color based on size and instability
        progress = self.target_radius / self.max_radius
        instability_factor = self.instability / self.max_instability

        # Clamp the interpolation factor to [0, 1]
        interpolation_factor = min(progress**2 + instability_factor, 1.0)
        self.color = self.base_color.lerp(pygame.Color(255, 0, 0), interpolation_factor)

        # Check collisions
        for bubble in bubbles[:]:
            if self.position.distance_to(bubble["position"]) < self.radius + bubble["radius"]:
                self._handle_bubble_collision(bubble)
                bubbles.remove(bubble)
                self.effects['pop'].play()

        # Warning system
        if not self.warning_activated and self.instability > self.max_instability * 0.8:
            self.warning_activated = True

    def burst(self):
        self.bursting = True
        self.burst_radius = self.radius
        self.effects['death'].play()
        
        # Create burst particles
        self.burst_particles = [{
            'pos': Vector2(self.position),
            'vel': Vector2(randint(-5,5), randint(-5,5)).normalize() * randint(3,7),
            'radius': randint(3,6),
            'life': 1.0
        } for _ in range(20)]

    def _update_burst_animation(self):
        self.burst_radius += 15
        for p in self.burst_particles:
            p['pos'] += p['vel']
            p['life'] -= 0.02
            p['vel'] *= 0.98
            
        self.burst_particles = [p for p in self.burst_particles if p['life'] > 0]
        
        if self.burst_radius > max(self.screen_rect.size)*1.5 and not self.burst_particles:
            self.stateManager.changeState(GameStates.GAME_OVER)

    def _handle_bubble_collision(self, bubble):
        if bubble["category"] == "positive":
            self.target_radius = min(self.target_radius + self.growth_rate, self.max_radius)
            self.score += 10  # Increase score for positive bubbles
        elif bubble["category"] == "risky":
            self.target_radius = min(self.target_radius + self.growth_rate * 2, self.max_radius)
            self.instability = min(self.instability + self.instability_growth_rate, self.max_instability)
            self.score += 20  # Increase score for risky bubbles
        elif bubble["category"] == "negative":
            self.target_radius = max(self.target_radius - self.growth_rate * 5, self.min_radius)  # Ensure it doesn't go below min size
            self.score -= 30  # Decrease score for negative bubbles
        elif bubble["category"] == "stable":
            self.instability = max(self.instability - self.instability_decay_rate, 0)
            self.score += 15  # Increase score for stable bubbles

        if self.instability >= self.max_instability:
            self.burst()

    def render(self, surface):
        if self.bursting:
            self._render_burst(surface)
            return

        # Main bubble surface
        bubble_surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        
        # Pulsating base using custom easing
        t = self.pulse_phase / 360
        pulse_offset = 2 * abs(self._ease_out_sine(t))
        pygame.draw.circle(bubble_surf, self.color, 
                         (self.radius, self.radius), 
                         self.radius + pulse_offset)
        
         # Draw instability meter
        instability_angle = 360 * (self.instability / self.max_instability)
        pygame.draw.arc(bubble_surf, (255, 0, 0, 200), 
                        (0, 0, self.radius*2, self.radius*2), 
                        -90, -90 + instability_angle, 10)
        
        # Draw score inside the bubble
        font = pygame.font.Font(None, int(self.radius * 0.5))
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.radius, self.radius))
        bubble_surf.blit(score_text, score_rect)

        # Highlights
        highlight = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.ellipse(highlight, (255, 255, 255, 120), 
                           (self.radius*0.6, self.radius*0.2,
                            self.radius*0.5, self.radius*0.25))
        rotated = pygame.transform.rotate(highlight, 45)
        bubble_surf.blit(rotated, rotated.get_rect(center=(self.radius, self.radius)))

        # Border effects
        pygame.draw.circle(bubble_surf, (255, 255, 255, 30), 
                         (self.radius, self.radius), 
                         self.radius, 3)

        # Warning glow
        if self.warning_activated:
            t_warning = self.pulse_phase / 180  # Faster oscillation
            alpha = int(100 + 155 * abs(self._ease_out_sine(t_warning)))
            pygame.draw.circle(bubble_surf, (255, 50, 50, alpha), 
                             (self.radius, self.radius), 
                             self.radius, 4)

        surface.blit(bubble_surf, self.position - Vector2(self.radius))

    def _render_burst(self, surface):
        # Shockwave
        pygame.draw.circle(surface, (255, 255, 255, 150),
                         (int(self.position.x), int(self.position.y)),
                         self.burst_radius, 3)
        
        # Particles
        for p in self.burst_particles:
            alpha = int(255 * p['life'])
            pygame.draw.circle(surface, (255, 255, 255, alpha),
                             (int(p['pos'].x), int(p['pos'].y)),
                             int(p['radius']))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.bursting:
            mouse_pos = Vector2(event.pos)
            if self.position.distance_to(mouse_pos) < self.radius:
                self.burst()