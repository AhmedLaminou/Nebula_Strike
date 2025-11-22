"""
TestCopilotGame - Boss System
Manages boss battles with special attack patterns and behaviors.
"""

import pygame
import math
import random
from typing import List, Tuple, Optional
from settings import *
from utils import clamp, distance, normalize_vector
from bullets import BulletManager
from particles import ParticleManager


class Boss:
    """Base boss class with advanced AI and attack patterns."""
    
    def __init__(self, x: float, y: float, boss_type: str = BOSS_TYPE_BASIC):
        """Initialize a boss."""
        self.x = float(x)
        self.y = float(y)
        self.boss_type = boss_type
        self.active = True
        self.alive = True
        
        # Stats
        self.setup_stats(boss_type)
        
        # Movement
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.speed = BOSS_SPEED
        self.target_x = SCREEN_WIDTH // 2
        self.target_y = 150
        self.movement_pattern = 'hover'
        self.pattern_timer = 0.0
        
        # Combat
        self.fire_cooldown = 0.0
        self.fire_rate = 1.5
        self.attack_pattern = BOSS_ATTACK_SINGLE
        self.attack_timer = 0.0
        self.attack_phase = 0
        self.max_phases = 3
        
        # Visual
        self.width, self.height = BOSS_SIZE
        self.color = BOSS_COLOR
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.rect.center = (int(self.x), int(self.y))
        
        # Animation
        self.animation_frame = 0
        self.animation_time = 0.0
        self.blink_timer = 0.0
        self.shield_active = False
        self.shield_alpha = 128
        
        # Special properties
        self.collision_damage = BOSS_DAMAGE
        self.score_value = BOSS_SCORE
        
        # Phase tracking
        self.phase_thresholds = [
            self.max_health * 0.66,
            self.max_health * 0.33,
            self.max_health * 0.1
        ]
        self.current_phase = 0
    
    def setup_stats(self, boss_type: str):
        """Setup boss stats based on type."""
        base_health = 500
        
        if boss_type == BOSS_TYPE_TWIN:
            self.max_health = base_health * 0.7
            self.health = self.max_health
            self.width = BOSS_SIZE[0] * 0.8
            self.height = BOSS_SIZE[1] * 0.8
            self.attack_pattern = BOSS_ATTACK_SPREAD
        elif boss_type == BOSS_TYPE_MEGA:
            self.max_health = base_health * 2
            self.health = self.max_health
            self.width = BOSS_SIZE[0] * 1.5
            self.height = BOSS_SIZE[1] * 1.5
            self.attack_pattern = BOSS_ATTACK_SPIRAL
        elif boss_type == BOSS_TYPE_FINAL:
            self.max_health = base_health * 3
            self.health = self.max_health
            self.width = BOSS_SIZE[0] * 1.8
            self.height = BOSS_SIZE[1] * 1.8
            self.attack_pattern = BOSS_ATTACK_WAVE
        else:  # Basic boss
            self.max_health = base_health
            self.health = self.max_health
            self.attack_pattern = BOSS_ATTACK_SINGLE
        
        self.base_health = self.max_health
    
    def update(self, dt: float, player_pos: Optional[Tuple[float, float]], 
               bullet_manager: BulletManager, particle_manager: ParticleManager, sound_manager):
        """Update boss state and behavior."""
        if not self.active:
            return
        
        # Check phase changes
        self.check_phase_change()
        
        # Update AI
        self.update_ai(dt, player_pos)
        
        # Update movement
        self.update_movement(dt)
        
        # Update attacks
        self.update_attacks(dt, player_pos, bullet_manager, particle_manager, sound_manager)
        
        # Update animation
        self.update_animation(dt)
        
        # Update rect
        self.rect.center = (int(self.x), int(self.y))
        
        # Keep in bounds
        self.x = clamp(self.x, self.width // 2, SCREEN_WIDTH - self.width // 2)
        self.y = clamp(self.y, 50, SCREEN_HEIGHT // 3)
    
    def check_phase_change(self):
        """Check if boss should change phase."""
        for i, threshold in enumerate(self.phase_thresholds):
            if self.health <= threshold and i > self.current_phase:
                self.current_phase = i + 1
                self.fire_rate *= 0.8  # Faster attacks
                self.speed *= 1.2  # Faster movement
                self.shield_active = True
    
    def update_ai(self, dt: float, player_pos: Optional[Tuple[float, float]]):
        """Update boss AI behavior."""
        self.pattern_timer += dt
        
        if player_pos:
            # Track player position
            dist = distance((self.x, self.y), player_pos)
            
            if self.movement_pattern == 'hover':
                # Hover around center
                self.target_x = SCREEN_WIDTH // 2 + math.sin(self.pattern_timer) * 200
                self.target_y = 150 + math.cos(self.pattern_timer * 0.5) * 50
            elif self.movement_pattern == 'chase':
                # Chase player (if close)
                if dist < 300:
                    self.target_x = player_pos[0]
                    self.target_y = 150
            elif self.movement_pattern == 'dodge':
                # Dodge away from player
                if dist < 400:
                    dx = self.x - player_pos[0]
                    if abs(dx) < 100:
                        self.target_x = SCREEN_WIDTH // 2 + (200 if dx > 0 else -200)
    
    def update_movement(self, dt: float):
        """Update boss movement."""
        # Smooth movement to target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        
        # Apply smooth interpolation
        self.velocity_x = dx * 2.0
        self.velocity_y = dy * 2.0
        
        # Apply speed limit
        speed = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)
        if speed > self.speed:
            scale = self.speed / speed
            self.velocity_x *= scale
            self.velocity_y *= scale
        
        # Apply velocity
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
    
    def update_attacks(self, dt: float, player_pos: Optional[Tuple[float, float]], 
                      bullet_manager: BulletManager, particle_manager: ParticleManager, sound_manager):
        """Update boss attack patterns."""
        self.attack_timer += dt
        self.fire_cooldown -= dt
        
        if self.fire_cooldown <= 0 and player_pos:
            # Determine attack based on phase and pattern
            phase_modifier = min(self.current_phase, 2)
            
            if self.attack_pattern == BOSS_ATTACK_SINGLE:
                self.attack_single(player_pos, bullet_manager, sound_manager)
            elif self.attack_pattern == BOSS_ATTACK_SPREAD:
                self.attack_spread(player_pos, bullet_manager, sound_manager)
            elif self.attack_pattern == BOSS_ATTACK_SPIRAL:
                self.attack_spiral(player_pos, bullet_manager, sound_manager)
            elif self.attack_pattern == BOSS_ATTACK_WAVE:
                self.attack_wave(player_pos, bullet_manager, sound_manager)
            elif self.attack_pattern == BOSS_ATTACK_HOMING:
                self.attack_homing(player_pos, bullet_manager, sound_manager)
            
            # Set cooldown based on phase
            self.fire_cooldown = self.fire_rate / (1 + phase_modifier * 0.3)
    
    def attack_single(self, target_pos: Tuple[float, float], bullet_manager: BulletManager, sound_manager):
        """Single shot attack."""
        dx = target_pos[0] - self.x
        dy = target_pos[1] - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist > 0:
            vx = (dx / dist) * ENEMY_BULLET_SPEED
            vy = (dy / dist) * ENEMY_BULLET_SPEED
            bullet_manager.create_boss_bullet(self.x, self.y + self.height // 2, vx, vy, BOSS_DAMAGE, 'single')
            if sound_manager:
                sound_manager.play_sound('boss_shoot')
    
    def attack_spread(self, target_pos: Tuple[float, float], bullet_manager: BulletManager, sound_manager):
        """Spread shot attack."""
        count = 5 + self.current_phase * 2
        angle_spread = 60.0
        bullet_manager.create_spread_pattern(
            self.x, self.y + self.height // 2, count, angle_spread, ENEMY_BULLET_SPEED, BOSS_DAMAGE, 'boss'
        )
        if sound_manager:
            sound_manager.play_sound('boss_shoot')
    
    def attack_spiral(self, target_pos: Tuple[float, float], bullet_manager: BulletManager, sound_manager):
        """Spiral pattern attack."""
        count = 8 + self.current_phase * 2
        base_angle = self.attack_timer * 180.0  # Rotate over time
        bullet_manager.create_spiral_pattern(
            self.x, self.y + self.height // 2, count, base_angle, ENEMY_BULLET_SPEED, BOSS_DAMAGE, 'boss'
        )
        if sound_manager:
            sound_manager.play_sound('boss_shoot')
    
    def attack_wave(self, target_pos: Tuple[float, float], bullet_manager: BulletManager, sound_manager):
        """Wave pattern attack."""
        # Create sine wave of bullets
        wave_count = 7
        for i in range(wave_count):
            offset = (i - wave_count / 2) * 50
            angle = math.sin(self.attack_timer * 2.0 + i) * 30.0
            angle_rad = math.radians(angle)
            vx = math.cos(angle_rad) * ENEMY_BULLET_SPEED * 0.5
            vy = math.sin(angle_rad) * ENEMY_BULLET_SPEED + ENEMY_BULLET_SPEED * 0.5
            bullet_manager.create_boss_bullet(
                self.x + offset, self.y + self.height // 2, vx, vy, BOSS_DAMAGE, 'spread'
            )
        if sound_manager:
            sound_manager.play_sound('boss_shoot')
    
    def attack_homing(self, target_pos: Tuple[float, float], bullet_manager: BulletManager, sound_manager):
        """Homing bullet attack."""
        count = 3 + self.current_phase
        bullet_manager.create_homing_bullets(
            self.x, self.y + self.height // 2, count, target_pos, ENEMY_BULLET_SPEED * 0.7, BOSS_DAMAGE
        )
        if sound_manager:
            sound_manager.play_sound('boss_shoot')
    
    def update_animation(self, dt: float):
        """Update animation frames."""
        self.animation_time += dt
        if self.animation_time >= 1.0 / ANIMATION_FPS:
            self.animation_frame = (self.animation_frame + 1) % 4
            self.animation_time = 0.0
        
        # Blink when damaged
        if self.blink_timer > 0:
            self.blink_timer -= dt
            self.shield_alpha = int(128 + 127 * math.sin(self.blink_timer * 20))
    
    def take_damage(self, amount: float):
        """Apply damage to boss."""
        if not self.active:
            return
        
        self.health -= amount
        self.blink_timer = 0.3
        self.shield_active = True
        
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.active = False
    
    def is_dead(self) -> bool:
        """Check if boss is dead."""
        return not self.alive or self.health <= 0
    
    def render(self, screen: pygame.Surface):
        """Render the boss."""
        if not self.active:
            return
        
        # Draw shield
        if self.shield_active:
            shield_surface = pygame.Surface((self.width + 30, self.height + 30), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (*PURPLE, self.shield_alpha), 
                             (self.width // 2 + 15, self.height // 2 + 15), 
                             (self.width + self.height) // 2, 5)
            screen.blit(shield_surface, (self.rect.x - 15, self.rect.y - 15))
        
        # Draw boss body
        # Main body
        pygame.draw.ellipse(screen, self.color, self.rect)
        
        # Detail lines
        for i in range(3):
            y_offset = self.rect.height // 4 * (i + 1)
            pygame.draw.line(screen, WHITE, 
                           (self.rect.left, self.rect.top + y_offset),
                           (self.rect.right, self.rect.top + y_offset), 2)
        
        # Center core
        core_size = self.width // 3
        core_rect = pygame.Rect(
            self.rect.centerx - core_size // 2,
            self.rect.centery - core_size // 2,
            core_size, core_size
        )
        pygame.draw.ellipse(screen, RED, core_rect)
        pygame.draw.ellipse(screen, YELLOW, core_rect, 2)
        
        # Draw health bar
        self.render_health_bar(screen)
    
    def render_health_bar(self, screen: pygame.Surface):
        """Render boss health bar."""
        bar_width = 300
        bar_height = 20
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 10
        
        # Background
        pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Health fill
        health_ratio = self.health / self.max_health
        fill_width = int(bar_width * health_ratio)
        
        # Color based on health
        if health_ratio > 0.66:
            health_color = GREEN
        elif health_ratio > 0.33:
            health_color = YELLOW
        else:
            health_color = RED
        
        if fill_width > 0:
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Phase indicator
        phase_text = f"Phase {self.current_phase + 1}/{self.max_phases}"
        font = pygame.font.Font(None, 24)
        text_surface = font.render(phase_text, True, WHITE)
        screen.blit(text_surface, (bar_x + bar_width // 2 - text_surface.get_width() // 2, bar_y + 25))


class BossManager:
    """Manages boss battles in the game."""
    
    def __init__(self):
        """Initialize boss manager."""
        self.active_boss: Optional[Boss] = None
        self.bosses_defeated = 0
        self.level = 1
    
    def reset(self):
        """Reset boss manager."""
        self.active_boss = None
        self.bosses_defeated = 0
    
    def set_level(self, level: int):
        """Set current level."""
        self.level = level
    
    def spawn_boss(self, boss_type: str = None):
        """Spawn a boss."""
        if self.active_boss:
            return  # Boss already active
        
        # Choose boss type if not specified
        if not boss_type:
            boss_type = self.choose_boss_type()
        
        # Spawn at top center
        x = SCREEN_WIDTH // 2
        y = 100
        
        boss = Boss(x, y, boss_type)
        
        # Scale stats based on level
        level_multiplier = 1.0 + (self.level - 1) * BOSS_HEALTH_INCREASE_PER_LEVEL
        boss.max_health = int(boss.max_health * level_multiplier)
        boss.health = boss.max_health
        boss.base_health = boss.max_health
        boss.score_value = int(boss.score_value * level_multiplier)
        
        self.active_boss = boss
        return boss
    
    def choose_boss_type(self) -> str:
        """Choose boss type based on level."""
        if self.level < 5:
            return BOSS_TYPE_BASIC
        elif self.level < 10:
            return random.choice([BOSS_TYPE_BASIC, BOSS_TYPE_TWIN])
        elif self.level < 15:
            return random.choice([BOSS_TYPE_TWIN, BOSS_TYPE_MEGA])
        else:
            if self.level % 20 == 0:
                return BOSS_TYPE_FINAL
            return random.choice([BOSS_TYPE_TWIN, BOSS_TYPE_MEGA])
    
    def update(self, dt: float, player_pos: Optional[Tuple[float, float]], 
              bullet_manager: BulletManager, particle_manager: ParticleManager, sound_manager):
        """Update active boss."""
        if self.active_boss:
            self.active_boss.update(dt, player_pos, bullet_manager, particle_manager, sound_manager)
            
            # Check if boss is defeated
            if self.active_boss.is_dead():
                # Create explosion
                if particle_manager:
                    particle_manager.create_explosion(
                        self.active_boss.rect.centerx, self.active_boss.rect.centery,
                        EXPLOSION_PARTICLE_COUNT * 5, EXPLOSION_COLOR
                    )
                if sound_manager:
                    sound_manager.play_sound('boss_defeat')
                
                self.bosses_defeated += 1
                self.active_boss = None
    
    def render(self, screen: pygame.Surface):
        """Render active boss."""
        if self.active_boss:
            self.active_boss.render(screen)
    
    def has_active_boss(self) -> bool:
        """Check if there's an active boss."""
        return self.active_boss is not None and self.active_boss.active
    
    def get_active_boss(self) -> Optional[Boss]:
        """Get the active boss."""
        return self.active_boss if self.has_active_boss() else None

