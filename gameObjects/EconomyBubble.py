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
        self.growth_rate = 5
        self.base_color = pygame.Color(98, 114, 164)
        self.color = pygame.Color(self.base_color)
        self.pulse_speed = 0.5
        self.pulse_phase = 0
        
        # Sound effects
        self.effects = {
            'pop': pygame.mixer.Sound('assets/audio/bubblepop.wav'),
            'death': pygame.mixer.Sound('assets/audio/death.wav'),
            # 'warning': pygame.mixer.Sound('assets/audio/warning.wav')
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

        # Dynamic color based on size
        progress = self.target_radius / self.max_radius
        self.color = self.base_color.lerp(pygame.Color(255, 0, 0), progress**2)

        # Check collisions
        for bubble in bubbles[:]:
            if self.position.distance_to(bubble["position"]) < self.radius + bubble["radius"]:
                self.target_radius = min(self.target_radius + self.growth_rate, self.max_radius)
                bubbles.remove(bubble)
                self.effects['pop'].play()
                
                if self.target_radius >= self.max_radius:
                    self.burst()

        # Warning system
        if not self.warning_activated and self.target_radius > self.max_radius * 0.8:
            # self.effects['warning'].play()
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