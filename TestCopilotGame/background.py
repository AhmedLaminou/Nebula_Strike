"""
TestCopilotGame - Background System
Manages scrolling starfield and parallax backgrounds.
"""

import pygame
import math
import random
from typing import List, Tuple
from settings import *
from utils import clamp


class Star:
    """Single star in the starfield."""
    
    def __init__(self, x: float, y: float, speed: float, size: int = 1, brightness: int = 255):
        """Initialize a star."""
        self.x = float(x)
        self.y = float(y)
        self.speed = speed
        self.size = size
        self.brightness = brightness
        self.color = (brightness, brightness, brightness)
        self.twinkle_timer = random.uniform(0, math.pi * 2)
        self.twinkle_speed = random.uniform(0.5, 2.0)
    
    def update(self, dt: float):
        """Update star position and twinkle effect."""
        # Move down
        self.y += self.speed * dt
        
        # Wrap around when off screen
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)
        
        # Update twinkle
        self.twinkle_timer += dt * self.twinkle_speed
        twinkle = (math.sin(self.twinkle_timer) + 1.0) / 2.0
        brightness = int(self.brightness * (0.7 + 0.3 * twinkle))
        self.color = (brightness, brightness, brightness)
    
    def render(self, screen: pygame.Surface):
        """Render the star."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


class Nebula:
    """Nebula cloud for background atmosphere."""
    
    def __init__(self, x: float, y: float, width: int, height: int, color: tuple, alpha: int = 30):
        """Initialize a nebula."""
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.color = color
        self.alpha = alpha
        self.speed = random.uniform(20, 50)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Create gradient nebula
        self.create_gradient()
    
    def create_gradient(self):
        """Create gradient effect for nebula."""
        for y in range(self.height):
            for x in range(self.width):
                # Distance from center
                center_x = self.width // 2
                center_y = self.height // 2
                dist = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                max_dist = math.sqrt(center_x ** 2 + center_y ** 2)
                
                # Calculate alpha based on distance
                alpha_factor = 1.0 - (dist / max_dist)
                alpha = int(self.alpha * alpha_factor * alpha_factor)
                
                # Set pixel
                self.surface.set_at((x, y), (*self.color, alpha))
    
    def update(self, dt: float):
        """Update nebula position."""
        self.y += self.speed * dt
        
        # Wrap around
        if self.y > SCREEN_HEIGHT + self.height:
            self.y = -self.height
            self.x = random.randint(0, SCREEN_WIDTH)
    
    def render(self, screen: pygame.Surface):
        """Render the nebula."""
        screen.blit(self.surface, (int(self.x), int(self.y)))


class BackgroundLayer:
    """A single parallax layer of the background."""
    
    def __init__(self, depth: int, star_count: int, speed_factor: float):
        """Initialize a background layer."""
        self.depth = depth
        self.star_count = star_count
        self.speed_factor = speed_factor
        self.stars: List[Star] = []
        
        # Create stars for this layer
        self.create_stars()
    
    def create_stars(self):
        """Create stars for this layer."""
        for _ in range(self.star_count):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            speed = random.uniform(STAR_SPEED_MIN, STAR_SPEED_MAX) * self.speed_factor
            
            # Deeper layers have smaller, dimmer stars
            size = max(1, 3 - self.depth)
            brightness = int(255 * (1.0 - self.depth * 0.2))
            brightness = max(50, brightness)
            
            star = Star(x, y, speed, size, brightness)
            self.stars.append(star)
    
    def update(self, dt: float):
        """Update all stars in this layer."""
        for star in self.stars:
            star.update(dt)
    
    def render(self, screen: pygame.Surface):
        """Render all stars in this layer."""
        for star in self.stars:
            star.render(screen)


class BackgroundManager:
    """Manages all background elements including starfield and parallax layers."""
    
    def __init__(self):
        """Initialize background manager."""
        self.layers: List[BackgroundLayer] = []
        self.nebulas: List[Nebula] = []
        
        # Create parallax layers
        self.create_layers()
        
        # Create nebulas
        self.create_nebulas()
        
        # Scrolling offset
        self.scroll_y = 0.0
        self.scroll_speed = 100.0
        
        # Background color
        self.bg_color = BG_COLOR
    
    def create_layers(self):
        """Create parallax background layers."""
        for i in range(PARALLAX_LAYERS):
            depth = i
            star_count = STAR_COUNT // PARALLAX_LAYERS
            speed_factor = 0.5 + (i * 0.3)  # Faster layers in front
            
            layer = BackgroundLayer(depth, star_count, speed_factor)
            self.layers.append(layer)
    
    def create_nebulas(self, count: int = 3):
        """Create nebula clouds for atmosphere."""
        for _ in range(count):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT)
            width = random.randint(200, 400)
            height = random.randint(150, 300)
            
            # Random nebula color
            colors = [
                (100, 50, 150),  # Purple
                (150, 50, 100),  # Magenta
                (50, 100, 150),  # Blue
                (100, 150, 50),  # Green
            ]
            color = random.choice(colors)
            alpha = random.randint(20, 50)
            
            nebula = Nebula(x, y, width, height, color, alpha)
            self.nebulas.append(nebula)
    
    def update(self, dt: float):
        """Update all background elements."""
        # Update layers (back to front)
        for layer in reversed(self.layers):
            layer.update(dt)
        
        # Update nebulas
        for nebula in self.nebulas:
            nebula.update(dt)
        
        # Update scroll
        self.scroll_y += self.scroll_speed * dt
        if self.scroll_y >= SCREEN_HEIGHT:
            self.scroll_y = 0.0
    
    def render(self, screen: pygame.Surface):
        """Render all background elements."""
        # Fill background
        screen.fill(self.bg_color)
        
        # Render nebulas (back layer)
        for nebula in self.nebulas:
            nebula.render(screen)
        
        # Render star layers (back to front)
        for layer in self.layers:
            layer.render(screen)
    
    def set_scroll_speed(self, speed: float):
        """Set scroll speed."""
        self.scroll_speed = speed
    
    def reset(self):
        """Reset background state."""
        self.scroll_y = 0.0
        self.layers.clear()
        self.create_layers()
        self.nebulas.clear()
        self.create_nebulas()

