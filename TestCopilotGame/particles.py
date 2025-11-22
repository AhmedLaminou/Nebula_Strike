"""
TestCopilotGame - Particle System
Manages particle effects for explosions, trails, and other visual effects.
"""

import pygame
import math
import random
from typing import List, Tuple
from settings import *
from utils import clamp, random_color_vibrant


class Particle:
    """Single particle for particle effects."""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, color: tuple, lifetime: float, size: int = 3):
        """Initialize a particle."""
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.age = 0.0
        self.size = size
        self.active = True
        
        # Physics
        self.gravity = 0.0
        self.friction = 0.98
        self.rotation = random.uniform(0, math.pi * 2)
        self.rotation_speed = random.uniform(-5, 5)
        
        # Visual
        self.alpha = 255
        self.fade_out = True
        
        # Trail
        self.trail = []
        self.max_trail_length = 2
    
    def update(self, dt: float):
        """Update particle state."""
        if not self.active:
            return
        
        # Update age
        self.age += dt
        if self.age >= self.lifetime:
            self.active = False
            return
        
        # Apply physics
        self.vy += self.gravity * dt
        self.vx *= self.friction
        self.vy *= self.friction
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Update rotation
        self.rotation += self.rotation_speed * dt
        
        # Update alpha (fade out)
        if self.fade_out:
            progress = self.age / self.max_lifetime
            self.alpha = int(255 * (1.0 - progress))
        
        # Update trail
        if len(self.trail) >= self.max_trail_length:
            self.trail.pop(0)
        self.trail.append((self.x, self.y))
    
    def render(self, screen: pygame.Surface):
        """Render the particle."""
        if not self.active:
            return
        
        # Create surface with alpha
        surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # Draw particle
        color_with_alpha = (*self.color, self.alpha)
        pygame.draw.circle(surface, color_with_alpha, (self.size, self.size), self.size)
        
        # Draw glow
        glow_radius = int(self.size * 1.5)
        glow_alpha = int(self.alpha * 0.5)
        pygame.draw.circle(surface, (*self.color, glow_alpha), (self.size, self.size), glow_radius)
        
        # Blit to screen
        screen.blit(surface, (int(self.x - self.size), int(self.y - self.size)))


class ParticleManager:
    """Manages all particle effects in the game."""
    
    def __init__(self):
        """Initialize particle manager."""
        self.particles: List[Particle] = []
        self.max_particles = MAX_PARTICLES
    
    def reset(self):
        """Reset all particles."""
        self.particles.clear()
    
    def create_particle(self, x: float, y: float, vx: float, vy: float, color: tuple, lifetime: float, size: int = 3) -> Particle:
        """Create a single particle."""
        if len(self.particles) >= self.max_particles:
            # Remove oldest particle
            if self.particles:
                self.particles.pop(0)
        
        particle = Particle(x, y, vx, vy, color, lifetime, size)
        self.particles.append(particle)
        return particle
    
    def create_explosion(self, x: float, y: float, count: int, color: tuple = EXPLOSION_COLOR):
        """Create an explosion effect."""
        for _ in range(min(count, self.max_particles // 4)):
            # Random velocity in all directions
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(PARTICLE_SPEED_MIN, PARTICLE_SPEED_MAX)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # Vary color slightly
            color_variation = random.randint(-30, 30)
            r = clamp(color[0] + color_variation, 0, 255)
            g = clamp(color[1] + color_variation, 0, 255)
            b = clamp(color[2] + color_variation, 0, 255)
            particle_color = (r, g, b)
            
            # Random size
            size = random.randint(2, 6)
            lifetime = random.uniform(PARTICLE_LIFETIME * 0.5, PARTICLE_LIFETIME)
            
            self.create_particle(x, y, vx, vy, particle_color, lifetime, size)
    
    def create_hit_sparks(self, x: float, y: float, count: int):
        """Create hit sparks effect."""
        for _ in range(min(count, 10)):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(50, 150)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # White/yellow sparks
            color = random.choice([WHITE, YELLOW, ORANGE])
            size = random.randint(1, 3)
            lifetime = random.uniform(0.2, 0.5)
            
            self.create_particle(x, y, vx, vy, color, lifetime, size)
    
    def create_collect_effect(self, x: float, y: float):
        """Create collect/pickup effect."""
        for _ in range(15):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(50, 200)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            color = random_color_vibrant()
            size = random.randint(2, 5)
            lifetime = random.uniform(0.5, 1.0)
            
            particle = self.create_particle(x, y, vx, vy, color, lifetime, size)
            particle.gravity = -50  # Float upward
    
    def create_trail(self, x: float, y: float, color: tuple, count: int = 3):
        """Create a trail effect."""
        for _ in range(count):
            # Small random offset
            offset_x = random.uniform(-5, 5)
            offset_y = random.uniform(-5, 5)
            vx = random.uniform(-20, 20)
            vy = random.uniform(-20, 20)
            
            size = random.randint(1, 3)
            lifetime = random.uniform(0.3, 0.6)
            
            self.create_particle(x + offset_x, y + offset_y, vx, vy, color, lifetime, size)
    
    def create_smoke(self, x: float, y: float, count: int = 10):
        """Create smoke effect."""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(20, 80)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 50  # Float up
            
            # Gray smoke color
            gray = random.randint(100, 200)
            color = (gray, gray, gray)
            size = random.randint(5, 15)
            lifetime = random.uniform(1.0, 2.0)
            
            particle = self.create_particle(x, y, vx, vy, color, lifetime, size)
            particle.gravity = -30
            particle.friction = 0.95
    
    def create_star_field(self, count: int):
        """Create background star field particles."""
        for _ in range(count):
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.uniform(0, SCREEN_HEIGHT)
            vy = random.uniform(STAR_SPEED_MIN, STAR_SPEED_MAX)
            
            # White stars
            brightness = random.randint(150, 255)
            color = (brightness, brightness, brightness)
            size = random.randint(1, 2)
            lifetime = 100.0  # Very long lifetime
            
            particle = self.create_particle(x, y, 0, vy, color, lifetime, size)
            particle.fade_out = False
    
    def create_energy_ball(self, x: float, y: float, color: tuple, size: int = 20):
        """Create energy ball effect."""
        for _ in range(20):
            angle = random.uniform(0, math.pi * 2)
            distance = random.uniform(0, size)
            px = x + math.cos(angle) * distance
            py = y + math.sin(angle) * distance
            
            # Particles spiral outward
            vx = math.cos(angle) * random.uniform(50, 150)
            vy = math.sin(angle) * random.uniform(50, 150)
            
            particle_size = random.randint(2, 4)
            lifetime = random.uniform(0.5, 1.0)
            
            self.create_particle(px, py, vx, vy, color, lifetime, particle_size)
    
    def create_beam(self, x1: float, y1: float, x2: float, y2: float, color: tuple, width: int = 5):
        """Create beam/laser effect."""
        # Calculate direction
        dx = x2 - x1
        dy = y2 - y1
        dist = math.sqrt(dx * dx + dy * dy)
        steps = int(dist / 10)
        
        if dist == 0:
            return
        
        for i in range(steps):
            t = i / steps if steps > 0 else 0
            px = x1 + dx * t
            py = y1 + dy * t
            
            # Perpendicular offset for width
            perp_x = -dy / dist
            perp_y = dx / dist
            
            for j in range(width):
                offset = (j - width / 2) * 3
                particle_x = px + perp_x * offset
                particle_y = py + perp_y * offset
                
                vx = random.uniform(-10, 10)
                vy = random.uniform(-10, 10)
                particle_size = random.randint(1, 3)
                lifetime = random.uniform(0.2, 0.4)
                
                self.create_particle(particle_x, particle_y, vx, vy, color, lifetime, particle_size)
    
    def update(self, dt: float):
        """Update all particles."""
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.active:
                self.particles.remove(particle)
        
        # Cull particles that are far off screen
        margin = PARTICLE_CULLING_DISTANCE
        for particle in self.particles[:]:
            if (particle.x < -margin or particle.x > SCREEN_WIDTH + margin or
                particle.y < -margin or particle.y > SCREEN_HEIGHT + margin):
                if particle.active:
                    particle.active = False
                    self.particles.remove(particle)
    
    def render(self, screen: pygame.Surface):
        """Render all particles."""
        for particle in self.particles:
            if particle.active:
                particle.render(screen)
    
    def get_active_particles(self) -> List[Particle]:
        """Get all active particles."""
        return [p for p in self.particles if p.active]
    
    def count_active_particles(self) -> int:
        """Count active particles."""
        return len(self.get_active_particles())

