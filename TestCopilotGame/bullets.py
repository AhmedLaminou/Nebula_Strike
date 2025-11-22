"""
TestCopilotGame - Bullet System
Manages all bullet types for player, enemies, and bosses.
"""

import pygame
import math
from typing import List
from settings import *
from utils import clamp


class Bullet:
    """Base bullet class for all projectile types."""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, damage: float, color: tuple, size: tuple, owner: str = 'player'):
        """Initialize a bullet."""
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.damage = float(damage)
        self.color = color
        self.width, self.height = size
        self.owner = owner  # 'player', 'enemy', 'boss'
        self.active = True
        self.lifetime = 10.0
        self.age = 0.0
        
        # Visual
        self.angle = math.atan2(self.vy, self.vx) if (self.vx != 0 or self.vy != 0) else 0
        self.trail = []
        self.max_trail_length = 3
        
        # Special properties
        self.homing = False
        self.homing_target = None
        self.homing_strength = 0.0
        self.piercing = False
        self.pierce_count = 0
        self.explosive = False
        self.explosion_radius = 0.0
        
        # Create rect for collision
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.rect.center = (int(self.x), int(self.y))
    
    def update(self, dt: float):
        """Update bullet position and state."""
        if not self.active:
            return
        
        # Update lifetime
        self.age += dt
        if self.age >= self.lifetime:
            self.active = False
            return
        
        # Homing behavior
        if self.homing and self.homing_target:
            self.update_homing(dt)
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Update trail
        self.update_trail()
        
        # Update rect
        self.rect.center = (int(self.x), int(self.y))
        
        # Check bounds
        margin = 100
        if (self.x < -margin or self.x > SCREEN_WIDTH + margin or
            self.y < -margin or self.y > SCREEN_HEIGHT + margin):
            self.active = False
    
    def update_homing(self, dt: float):
        """Update homing behavior toward target."""
        if not self.homing_target:
            return
        
        # Calculate direction to target
        dx = self.homing_target[0] - self.x
        dy = self.homing_target[1] - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            # Normalize direction
            dx /= distance
            dy /= distance
            
            # Current velocity direction
            speed = math.sqrt(self.vx * self.vx + self.vy * self.vy)
            if speed > 0:
                current_angle = math.atan2(self.vy, self.vx)
                target_angle = math.atan2(dy, dx)
                
                # Interpolate angle
                angle_diff = target_angle - current_angle
                # Normalize angle difference
                while angle_diff > math.pi:
                    angle_diff -= 2 * math.pi
                while angle_diff < -math.pi:
                    angle_diff += 2 * math.pi
                
                # Apply homing strength
                new_angle = current_angle + angle_diff * self.homing_strength * dt * 5.0
                
                # Update velocity
                self.vx = math.cos(new_angle) * speed
                self.vy = math.sin(new_angle) * speed
                self.angle = new_angle
    
    def update_trail(self):
        """Update bullet trail effect."""
        if len(self.trail) >= self.max_trail_length:
            self.trail.pop(0)
        self.trail.append((self.x, self.y))
    
    def render(self, screen: pygame.Surface):
        """Render the bullet."""
        if not self.active:
            return
        
        # Draw trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(128 * (i / len(self.trail)) if len(self.trail) > 0 else 1)
            size = max(1, int(3 * (i / len(self.trail)) if len(self.trail) > 0 else 1))
            pygame.draw.circle(screen, self.color, (int(tx), int(ty)), size)
        
        # Draw bullet
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw glow effect
        glow_surface = pygame.Surface((self.width + 4, self.height + 4), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*self.color, 128), (2, 2, self.width, self.height))
        screen.blit(glow_surface, (self.rect.x - 2, self.rect.y - 2))


class PlayerBullet(Bullet):
    """Player bullet type."""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, damage: float, weapon_level: int = 1):
        """Initialize player bullet."""
        size = (BULLET_SIZE[0] + weapon_level * 2, BULLET_SIZE[1] + weapon_level * 2)
        super().__init__(x, y, vx, vy, damage, BULLET_COLOR, size, 'player')
        self.weapon_level = weapon_level
        self.lifetime = 5.0
        
        # Visual effect based on weapon level
        if weapon_level >= 3:
            self.color = YELLOW
        if weapon_level >= 4:
            self.color = GOLD


class EnemyBullet(Bullet):
    """Enemy bullet type."""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, damage: float = ENEMY_BULLET_DAMAGE):
        """Initialize enemy bullet."""
        super().__init__(x, y, vx, vy, damage, ENEMY_BULLET_COLOR, ENEMY_BULLET_SIZE, 'enemy')
        self.lifetime = 8.0


class BossBullet(Bullet):
    """Boss bullet type with special properties."""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, damage: float, bullet_type: str = 'single'):
        """Initialize boss bullet."""
        size = (ENEMY_BULLET_SIZE[0] * 2, ENEMY_BULLET_SIZE[1] * 2)
        color = PURPLE if bullet_type == 'spread' else RED
        super().__init__(x, y, vx, vy, damage, color, size, 'boss')
        self.bullet_type = bullet_type
        self.lifetime = 10.0
        
        # Special properties based on type
        if bullet_type == 'spread':
            self.explosive = True
            self.explosion_radius = 50.0
        elif bullet_type == 'homing':
            self.homing = True
            self.homing_strength = 0.5
        elif bullet_type == 'laser':
            self.piercing = True
            self.pierce_count = 3


class BulletManager:
    """Manages all bullets in the game."""
    
    def __init__(self):
        """Initialize bullet manager."""
        self.player_bullets: List[Bullet] = []
        self.enemy_bullets: List[Bullet] = []
        self.boss_bullets: List[Bullet] = []
        self.max_bullets = MAX_BULLETS
    
    def reset(self):
        """Reset all bullets."""
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        self.boss_bullets.clear()
    
    def create_player_bullet(self, x: float, y: float, vx: float, vy: float, damage: float, weapon_level: int = 1):
        """Create a player bullet."""
        if len(self.player_bullets) < self.max_bullets:
            bullet = PlayerBullet(x, y, vx, vy, damage, weapon_level)
            self.player_bullets.append(bullet)
            return bullet
        return None
    
    def create_enemy_bullet(self, x: float, y: float, vx: float, vy: float, damage: float = ENEMY_BULLET_DAMAGE):
        """Create an enemy bullet."""
        if len(self.enemy_bullets) < self.max_bullets:
            bullet = EnemyBullet(x, y, vx, vy, damage)
            self.enemy_bullets.append(bullet)
            return bullet
        return None
    
    def create_boss_bullet(self, x: float, y: float, vx: float, vy: float, damage: float, bullet_type: str = 'single'):
        """Create a boss bullet."""
        if len(self.boss_bullets) < self.max_bullets:
            bullet = BossBullet(x, y, vx, vy, damage, bullet_type)
            self.boss_bullets.append(bullet)
            return bullet
        return None
    
    def create_spread_pattern(self, x: float, y: float, count: int, angle_spread: float, speed: float, damage: float, owner: str = 'enemy'):
        """Create a spread pattern of bullets."""
        bullets = []
        start_angle = -angle_spread * (count - 1) / 2
        
        for i in range(count):
            angle = start_angle + i * angle_spread
            angle_rad = math.radians(angle)
            vx = math.cos(angle_rad) * speed
            vy = math.sin(angle_rad) * speed
            
            if owner == 'player':
                bullet = self.create_player_bullet(x, y, vx, vy, damage)
            elif owner == 'boss':
                bullet = self.create_boss_bullet(x, y, vx, vy, damage, 'spread')
            else:
                bullet = self.create_enemy_bullet(x, y, vx, vy, damage)
            
            if bullet:
                bullets.append(bullet)
        
        return bullets
    
    def create_spiral_pattern(self, x: float, y: float, count: int, base_angle: float, speed: float, damage: float, owner: str = 'boss'):
        """Create a spiral pattern of bullets."""
        bullets = []
        angle_step = 360.0 / count
        
        for i in range(count):
            angle = base_angle + i * angle_step
            angle_rad = math.radians(angle)
            vx = math.cos(angle_rad) * speed
            vy = math.sin(angle_rad) * speed
            
            bullet = self.create_boss_bullet(x, y, vx, vy, damage, 'spread')
            if bullet:
                bullets.append(bullet)
        
        return bullets
    
    def create_homing_bullets(self, x: float, y: float, count: int, target: tuple, speed: float, damage: float):
        """Create homing bullets that track a target."""
        bullets = []
        
        for i in range(count):
            # Spread initial angles
            angle_offset = (i - count / 2) * 15.0
            angle = math.degrees(math.atan2(target[1] - y, target[0] - x)) + angle_offset
            angle_rad = math.radians(angle)
            vx = math.cos(angle_rad) * speed
            vy = math.sin(angle_rad) * speed
            
            bullet = self.create_boss_bullet(x, y, vx, vy, damage, 'homing')
            if bullet:
                bullet.homing_target = target
                bullets.append(bullet)
        
        return bullets
    
    def update(self, dt: float, player_pos: tuple = None):
        """Update all bullets."""
        # Update player bullets
        for bullet in self.player_bullets[:]:
            if player_pos and bullet.homing:
                bullet.homing_target = player_pos
            bullet.update(dt)
            if not bullet.active:
                self.player_bullets.remove(bullet)
        
        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            if player_pos and bullet.homing:
                bullet.homing_target = player_pos
            bullet.update(dt)
            if not bullet.active:
                self.enemy_bullets.remove(bullet)
        
        # Update boss bullets
        for bullet in self.boss_bullets[:]:
            if player_pos and bullet.homing:
                bullet.homing_target = player_pos
            bullet.update(dt)
            if not bullet.active:
                self.boss_bullets.remove(bullet)
    
    def cull_off_screen(self):
        """Remove bullets that are off-screen."""
        margin = 200
        for bullet_list in [self.player_bullets, self.enemy_bullets, self.boss_bullets]:
            for bullet in bullet_list[:]:
                if (bullet.x < -margin or bullet.x > SCREEN_WIDTH + margin or
                    bullet.y < -margin or bullet.y > SCREEN_HEIGHT + margin):
                    bullet.active = False
                    bullet_list.remove(bullet)
    
    def render(self, screen: pygame.Surface):
        """Render all bullets."""
        # Render player bullets
        for bullet in self.player_bullets:
            if bullet.active:
                bullet.render(screen)
        
        # Render enemy bullets
        for bullet in self.enemy_bullets:
            if bullet.active:
                bullet.render(screen)
        
        # Render boss bullets
        for bullet in self.boss_bullets:
            if bullet.active:
                bullet.render(screen)
    
    def get_all_bullets(self) -> List[Bullet]:
        """Get all active bullets."""
        return [b for b in self.player_bullets + self.enemy_bullets + self.boss_bullets if b.active]
    
    def count_active_bullets(self) -> int:
        """Count all active bullets."""
        return len(self.get_all_bullets())

