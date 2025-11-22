"""
TestCopilotGame - Power-up System
Manages all power-up types and effects.
"""

import pygame
import math
import random
from typing import List
from settings import *
from utils import clamp
from player import Player
from bullets import BulletManager


class PowerUp:
    """Base power-up class."""
    
    def __init__(self, x: float, y: float, powerup_type: str):
        """Initialize a power-up."""
        self.x = float(x)
        self.y = float(y)
        self.powerup_type = powerup_type
        self.active = True
        
        # Visual
        self.width, self.height = POWERUP_SIZE
        self.color = self.get_color()
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.rect.center = (int(self.x), int(self.y))
        
        # Movement
        self.velocity_y = POWERUP_SPEED
        self.rotation = 0.0
        self.rotation_speed = 180.0  # degrees per second
        
        # Pulsing effect
        self.pulse_timer = 0.0
        self.pulse_speed = 2.0
        
        # Lifetime
        self.lifetime = 15.0
        self.age = 0.0
    
    def get_color(self) -> tuple:
        """Get color based on power-up type."""
        color_map = {
            'health': HEALTH_POWERUP_COLOR,
            'speed': SPEED_POWERUP_COLOR,
            'damage': DAMAGE_POWERUP_COLOR,
            'shield': SHIELD_POWERUP_COLOR,
            'rapid_fire': RAPID_FIRE_COLOR,
            'multi_shot': MULTI_SHOT_COLOR,
        }
        return color_map.get(self.powerup_type, WHITE)
    
    def get_symbol(self) -> str:
        """Get symbol/icon for power-up."""
        symbol_map = {
            'health': '+',
            'speed': 'S',
            'damage': 'D',
            'shield': '[]',
            'rapid_fire': 'R',
            'multi_shot': 'M',
        }
        return symbol_map.get(self.powerup_type, '?')
    
    def update(self, dt: float):
        """Update power-up state."""
        if not self.active:
            return
        
        # Update position
        self.y += self.velocity_y * dt
        
        # Update rotation
        self.rotation += self.rotation_speed * dt
        if self.rotation >= 360.0:
            self.rotation -= 360.0
        
        # Update pulse
        self.pulse_timer += dt * self.pulse_speed
        
        # Update lifetime
        self.age += dt
        if self.age >= self.lifetime:
            self.active = False
        
        # Update rect
        self.rect.center = (int(self.x), int(self.y))
        
        # Remove if off screen
        if self.y > SCREEN_HEIGHT + 50:
            self.active = False
    
    def apply_effect(self, player: Player, bullet_manager: BulletManager):
        """Apply power-up effect to player."""
        if not self.active or not player:
            return
        
        duration = POWERUP_DURATION
        
        if self.powerup_type == 'health':
            player.apply_health_powerup()
        
        elif self.powerup_type == 'speed':
            player.apply_speed_powerup(duration)
        
        elif self.powerup_type == 'damage':
            player.apply_damage_powerup(duration)
        
        elif self.powerup_type == 'shield':
            player.apply_shield_powerup(duration)
        
        elif self.powerup_type == 'rapid_fire':
            player.apply_rapid_fire_powerup(duration)
        
        elif self.powerup_type == 'multi_shot':
            player.apply_multi_shot_powerup(duration)
        
        # Deactivate after applying
        self.active = False
    
    def render(self, screen: pygame.Surface):
        """Render the power-up."""
        if not self.active:
            return
        
        # Calculate pulse size
        pulse_scale = 1.0 + 0.2 * math.sin(self.pulse_timer)
        size = int(self.width * pulse_scale)
        
        # Create rotated surface
        surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        
        # Draw power-up shape
        center = (size, size)
        
        # Draw glow
        glow_radius = int(size * 1.5)
        for i in range(3):
            alpha = int(128 / (i + 1))
            pygame.draw.circle(surface, (*self.color, alpha), center, glow_radius - i * 5)
        
        # Draw main shape
        pygame.draw.circle(surface, self.color, center, size // 2)
        pygame.draw.circle(surface, WHITE, center, size // 2, 2)
        
        # Draw symbol
        font = pygame.font.Font(None, size // 2)
        symbol = self.get_symbol()
        text_surface = font.render(symbol, True, WHITE)
        text_rect = text_surface.get_rect(center=center)
        surface.blit(text_surface, text_rect)
        
        # Rotate surface
        rotated_surface = pygame.transform.rotate(surface, self.rotation)
        rotated_rect = rotated_surface.get_rect(center=self.rect.center)
        
        screen.blit(rotated_surface, rotated_rect)


class PowerUpManager:
    """Manages all power-ups in the game."""
    
    def __init__(self):
        """Initialize power-up manager."""
        self.powerups: List[PowerUp] = []
        self.max_powerups = 10
    
    def reset(self):
        """Reset all power-ups."""
        self.powerups.clear()
    
    def create_powerup(self, x: float, y: float, powerup_type: str = None) -> PowerUp:
        """Create a power-up at position."""
        if len(self.powerups) >= self.max_powerups:
            return None
        
        # Choose random type if not specified
        if not powerup_type:
            powerup_type = self.choose_powerup_type()
        
        powerup = PowerUp(x, y, powerup_type)
        self.powerups.append(powerup)
        return powerup
    
    def choose_powerup_type(self) -> str:
        """Choose power-up type based on rarity."""
        r = random.random()
        
        # Common power-ups (50%)
        if r < POWERUP_RARITY_COMMON:
            return random.choice(['health', 'speed', 'damage'])
        
        # Rare power-ups (30%)
        elif r < POWERUP_RARITY_COMMON + POWERUP_RARITY_RARE:
            return random.choice(['shield', 'rapid_fire'])
        
        # Epic power-ups (15%)
        elif r < POWERUP_RARITY_COMMON + POWERUP_RARITY_RARE + POWERUP_RARITY_EPIC:
            return 'multi_shot'
        
        # Legendary power-ups (5%)
        else:
            return random.choice(['health', 'shield'])  # Fallback
    
    def spawn_powerup_chance(self, x: float, y: float, chance: float = POWERUP_SPAWN_CHANCE):
        """Spawn a power-up with given chance."""
        if random.random() < chance:
            self.create_powerup(x, y)
    
    def update(self, dt: float):
        """Update all power-ups."""
        for powerup in self.powerups[:]:
            powerup.update(dt)
            if not powerup.active:
                self.powerups.remove(powerup)
    
    def render(self, screen: pygame.Surface):
        """Render all power-ups."""
        for powerup in self.powerups:
            if powerup.active:
                powerup.render(screen)
    
    def get_active_powerups(self) -> List[PowerUp]:
        """Get all active power-ups."""
        return [p for p in self.powerups if p.active]
    
    def count_active_powerups(self) -> int:
        """Count active power-ups."""
        return len(self.get_active_powerups())

