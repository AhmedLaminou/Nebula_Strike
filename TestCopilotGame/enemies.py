"""
TestCopilotGame - Enemy System
Manages all enemy types, AI, and behaviors.
"""

import pygame
import math
import random
from typing import List, Tuple, Optional
from settings import *
from utils import clamp, distance, normalize_vector
from bullets import BulletManager


class Enemy:
    """Base enemy class for all enemy types."""
    
    def __init__(self, x: float, y: float, enemy_type: str = ENEMY_TYPE_BASIC):
        """Initialize an enemy."""
        self.x = float(x)
        self.y = float(y)
        self.enemy_type = enemy_type
        self.active = True
        self.alive = True
        
        # Stats based on type
        self.setup_stats(enemy_type)
        
        # Movement
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.speed = self.base_speed
        self.direction = -1  # Move down by default
        self.angle = math.pi / 2  # Face downward
        
        # AI
        self.ai_state = 'patrol'  # 'patrol', 'attack', 'flee', 'shoot'
        self.ai_timer = 0.0
        self.target = None
        self.patrol_path = []
        self.patrol_index = 0
        
        # Shooting
        self.can_shoot = False
        self.fire_cooldown = 0.0
        self.fire_rate = ENEMY_BULLET_COOLDOWN
        self.shoot_pattern = 'single'
        
        # Visual
        self.width, self.height = ENEMY_SIZE
        self.color = ENEMY_COLOR
        self.animation_frame = 0
        self.animation_time = 0.0
        self.blink_timer = 0.0
        
        # Create rect for collision
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.rect.center = (int(self.x), int(self.y))
        
        # Special properties
        self.collision_damage = 10
        self.explosion_on_death = True
        self.drops_powerup = False
        self.score_value = ENEMY_SCORE_BASE
        
        # Movement patterns
        self.movement_pattern = 'straight'  # 'straight', 'zigzag', 'circle', 'dive'
        self.pattern_timer = 0.0
        self.pattern_speed = 1.0
        self.zigzag_amplitude = 100
        self.zigzag_frequency = 2.0
        self.circle_radius = 150
        self.circle_angle = 0.0
    
    def setup_stats(self, enemy_type: str):
        """Setup enemy stats based on type."""
        if enemy_type == ENEMY_TYPE_FAST:
            self.max_health = FAST_ENEMY_HEALTH
            self.health = self.max_health
            self.base_speed = FAST_ENEMY_SPEED
            self.color = YELLOW
            self.score_value = FAST_ENEMY_SCORE
        elif enemy_type == ENEMY_TYPE_TANK:
            self.max_health = TANK_ENEMY_HEALTH
            self.health = self.max_health
            self.base_speed = TANK_ENEMY_SPEED
            self.color = DARK_GRAY
            self.width = ENEMY_SIZE[0] * 1.5
            self.height = ENEMY_SIZE[1] * 1.5
            self.score_value = TANK_ENEMY_SCORE
        elif enemy_type == ENEMY_TYPE_SHOOTER:
            self.max_health = SHOOTER_ENEMY_HEALTH
            self.health = self.max_health
            self.base_speed = SHOOTER_ENEMY_SPEED
            self.color = RED
            self.can_shoot = True
            self.fire_rate = 1.0 / SHOOTER_ENEMY_FIRE_RATE
            self.score_value = SHOOTER_ENEMY_SCORE
        elif enemy_type == ENEMY_TYPE_KAMIKAZE:
            self.max_health = KAMIKAZE_ENEMY_HEALTH
            self.health = self.max_health
            self.base_speed = KAMIKAZE_ENEMY_SPEED
            self.color = ORANGE
            self.ai_state = 'attack'
            self.score_value = KAMIKAZE_ENEMY_SCORE
            self.collision_damage = KAMIKAZE_EXPLOSION_DAMAGE
        elif enemy_type == ENEMY_TYPE_SWARM:
            self.max_health = SWARM_ENEMY_HEALTH
            self.health = self.max_health
            self.base_speed = SWARM_ENEMY_SPEED
            self.color = CYAN
            self.width = ENEMY_SIZE[0] * 0.7
            self.height = ENEMY_SIZE[1] * 0.7
            self.score_value = SWARM_ENEMY_SCORE
            self.movement_pattern = 'zigzag'
        elif enemy_type == ENEMY_TYPE_ELITE:
            self.max_health = ELITE_ENEMY_HEALTH
            self.health = self.max_health
            self.base_speed = ELITE_ENEMY_SPEED
            self.color = PURPLE
            self.can_shoot = True
            self.fire_rate = 1.0 / ELITE_ENEMY_FIRE_RATE
            self.shoot_pattern = 'spread'
            self.score_value = ELITE_ENEMY_SCORE
            self.movement_pattern = 'circle'
        else:  # Basic enemy
            self.max_health = ENEMY_BASE_HEALTH
            self.health = self.max_health
            self.base_speed = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
            self.color = ENEMY_COLOR
            self.score_value = ENEMY_SCORE_BASE
        
        self.speed = self.base_speed
    
    def update(self, dt: float, player_pos: Optional[Tuple[float, float]], bullet_manager: Optional[BulletManager]):
        """Update enemy state and behavior."""
        if not self.active:
            return
        
        # Update AI
        self.update_ai(dt, player_pos)
        
        # Update movement
        self.update_movement(dt)
        
        # Update shooting
        if self.can_shoot and bullet_manager:
            self.update_shooting(dt, player_pos, bullet_manager)
        
        # Update animation
        self.update_animation(dt)
        
        # Update rect
        self.rect.center = (int(self.x), int(self.y))
        
        # Check if off screen
        if self.y > SCREEN_HEIGHT + 100:
            self.active = False
    
    def update_ai(self, dt: float, player_pos: Optional[Tuple[float, float]]):
        """Update AI behavior."""
        self.ai_timer += dt
        
        # Update AI state based on distance to player
        if player_pos:
            dist = distance((self.x, self.y), player_pos)
            
            if self.enemy_type == ENEMY_TYPE_KAMIKAZE:
                # Always charge at player
                self.ai_state = 'attack'
                self.target = player_pos
            elif dist < 300:
                # Close to player - attack
                self.ai_state = 'attack'
                self.target = player_pos
            elif dist < 500 and self.can_shoot:
                # Medium distance - shoot
                self.ai_state = 'shoot'
                self.target = player_pos
            else:
                # Far away - patrol
                self.ai_state = 'patrol'
                self.target = None
    
    def update_movement(self, dt: float):
        """Update enemy movement based on pattern."""
        self.pattern_timer += dt
        
        if self.movement_pattern == 'straight':
            # Simple downward movement
            self.velocity_x = 0.0
            self.velocity_y = self.speed
            self.angle = math.pi / 2
        
        elif self.movement_pattern == 'zigzag':
            # Zigzag pattern
            self.velocity_y = self.speed
            self.velocity_x = math.sin(self.pattern_timer * self.zigzag_frequency) * self.zigzag_amplitude
            self.angle = math.atan2(self.velocity_y, self.velocity_x)
        
        elif self.movement_pattern == 'circle':
            # Circular movement
            self.circle_angle += dt * self.pattern_speed
            center_x = SCREEN_WIDTH / 2
            center_y = 200
            self.x = center_x + math.cos(self.circle_angle) * self.circle_radius
            self.y = center_y + math.sin(self.circle_angle) * self.circle_radius
            self.angle = self.circle_angle + math.pi / 2
            return  # Position already set
        
        elif self.movement_pattern == 'dive':
            # Dive at target
            if self.target:
                dx = self.target[0] - self.x
                dy = self.target[1] - self.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > 0:
                    self.velocity_x = (dx / dist) * self.speed
                    self.velocity_y = (dy / dist) * self.speed
                    self.angle = math.atan2(self.velocity_y, self.velocity_x)
        
        # Apply velocity
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Keep in bounds (except for kamikaze)
        if self.enemy_type != ENEMY_TYPE_KAMIKAZE:
            self.x = clamp(self.x, self.width // 2, SCREEN_WIDTH - self.width // 2)
    
    def update_shooting(self, dt: float, player_pos: Optional[Tuple[float, float]], bullet_manager: BulletManager):
        """Update shooting behavior."""
        if not self.can_shoot or not bullet_manager:
            return
        
        # Update cooldown
        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt
        else:
            # Can shoot
            if player_pos and self.ai_state in ['shoot', 'attack']:
                self.shoot(player_pos, bullet_manager)
                self.fire_cooldown = self.fire_rate
    
    def shoot(self, target_pos: Tuple[float, float], bullet_manager: BulletManager):
        """Fire bullets at target."""
        # Calculate direction to target
        dx = target_pos[0] - self.x
        dy = target_pos[1] - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist == 0:
            return
        
        # Normalize direction
        vx = (dx / dist) * ENEMY_BULLET_SPEED
        vy = (dy / dist) * ENEMY_BULLET_SPEED
        
        if self.shoot_pattern == 'single':
            bullet_manager.create_enemy_bullet(self.x, self.y + self.height // 2, vx, vy, ENEMY_BULLET_DAMAGE)
        elif self.shoot_pattern == 'spread':
            bullet_manager.create_spread_pattern(
                self.x, self.y + self.height // 2, 3, 30.0, ENEMY_BULLET_SPEED, ENEMY_BULLET_DAMAGE, 'enemy'
            )
    
    def update_animation(self, dt: float):
        """Update animation frames."""
        self.animation_time += dt
        if self.animation_time >= 1.0 / ANIMATION_FPS:
            self.animation_frame = (self.animation_frame + 1) % 4
            self.animation_time = 0.0
        
        # Blink when damaged
        if self.blink_timer > 0:
            self.blink_timer -= dt
    
    def take_damage(self, amount: float):
        """Apply damage to enemy."""
        if not self.active:
            return
        
        self.health -= amount
        self.blink_timer = 0.2
        
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.active = False
    
    def is_dead(self) -> bool:
        """Check if enemy is dead."""
        return not self.alive or self.health <= 0
    
    def render(self, screen: pygame.Surface):
        """Render the enemy."""
        if not self.active:
            return
        
        # Blink effect when damaged
        visible = True
        if self.blink_timer > 0:
            visible = (int(self.blink_timer * 20) % 2 == 0)
        
        if not visible:
            return
        
        # Draw enemy shape
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw outline
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Draw health bar if damaged
        if self.health < self.max_health:
            bar_width = self.width
            bar_height = 4
            bar_x = self.rect.x
            bar_y = self.rect.y - 10
            
            # Background
            pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
            
            # Health fill
            health_ratio = self.health / self.max_health
            fill_width = int(bar_width * health_ratio)
            health_color = GREEN if health_ratio > 0.5 else (YELLOW if health_ratio > 0.25 else RED)
            if fill_width > 0:
                pygame.draw.rect(screen, health_color, (bar_x, bar_y, fill_width, bar_height))


class EnemyManager:
    """Manages all enemies in the game."""
    
    def __init__(self):
        """Initialize enemy manager."""
        self.enemies: List[Enemy] = []
        self.spawn_timer = 0.0
        self.spawn_rate = ENEMY_SPAWN_RATE
        self.level = 1
        self.wave_count = 0
        self.enemies_per_wave = ENEMY_COUNT_PER_WAVE
        self.wave_spawned = 0
        self.max_enemies = MAX_ENEMIES
    
    def reset(self):
        """Reset all enemies."""
        self.enemies.clear()
        self.spawn_timer = 0.0
        self.wave_count = 0
        self.wave_spawned = 0
    
    def set_level(self, level: int):
        """Set current level and adjust spawn rates."""
        self.level = level
        self.spawn_rate = ENEMY_SPAWN_RATE * (LEVEL_ENEMY_SPAWN_RATE_MULTIPLIER ** (level - 1))
        self.enemies_per_wave = int(ENEMY_COUNT_PER_WAVE * (LEVEL_ENEMY_COUNT_MULTIPLIER ** (level - 1)))
    
    def spawn_enemy(self, enemy_type: str = None):
        """Spawn a single enemy."""
        if len(self.enemies) >= self.max_enemies:
            return None
        
        # Choose random type if not specified
        if not enemy_type:
            enemy_type = self.choose_enemy_type()
        
        # Random X position
        x = random.randint(ENEMY_SIZE[0] // 2, SCREEN_WIDTH - ENEMY_SIZE[0] // 2)
        y = -ENEMY_SIZE[1] // 2
        
        # Create enemy
        enemy = Enemy(x, y, enemy_type)
        
        # Scale stats based on level
        enemy.max_health = int(enemy.max_health * (LEVEL_ENEMY_HEALTH_MULTIPLIER ** (self.level - 1)))
        enemy.health = enemy.max_health
        enemy.speed *= (LEVEL_ENEMY_SPEED_MULTIPLIER ** (self.level - 1))
        enemy.score_value = int(enemy.score_value * (1 + (self.level - 1) * 0.2))
        
        self.enemies.append(enemy)
        return enemy
    
    def choose_enemy_type(self) -> str:
        """Choose enemy type based on level and probability."""
        # Weighted random selection based on level
        types = []
        weights = []
        
        # Basic enemies always available
        types.append(ENEMY_TYPE_BASIC)
        weights.append(0.4)
        
        # Fast enemies
        if self.level >= 2:
            types.append(ENEMY_TYPE_FAST)
            weights.append(0.2)
        
        # Tank enemies
        if self.level >= 3:
            types.append(ENEMY_TYPE_TANK)
            weights.append(0.15)
        
        # Shooter enemies
        if self.level >= 2:
            types.append(ENEMY_TYPE_SHOOTER)
            weights.append(0.15)
        
        # Kamikaze enemies
        if self.level >= 4:
            types.append(ENEMY_TYPE_KAMIKAZE)
            weights.append(0.1)
        
        # Swarm enemies
        if self.level >= 3:
            types.append(ENEMY_TYPE_SWARM)
            weights.append(0.1)
        
        # Elite enemies
        if self.level >= 5:
            types.append(ENEMY_TYPE_ELITE)
            weights.append(0.1)
        
        # Normalize weights
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        
        # Select based on weights
        r = random.random()
        cumulative = 0.0
        for i, weight in enumerate(weights):
            cumulative += weight
            if r <= cumulative:
                return types[i]
        
        return types[0]
    
    def spawn_wave(self):
        """Spawn a wave of enemies."""
        for _ in range(self.enemies_per_wave):
            # Stagger spawns slightly
            delay = random.uniform(0.0, 1.0)
            # For now, spawn immediately (in real implementation, use timer)
            self.spawn_enemy()
    
    def update(self, dt: float, player_pos: Optional[Tuple[float, float]], 
               bullet_manager: BulletManager, particle_manager, sound_manager):
        """Update all enemies."""
        # Spawn enemies
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_enemy()
            self.spawn_timer = 0.0
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(dt, player_pos, bullet_manager)
            
            # Remove inactive enemies
            if not enemy.active:
                if enemy.is_dead():
                    # Create explosion particles
                    if enemy.explosion_on_death and particle_manager:
                        particle_manager.create_explosion(
                            enemy.rect.centerx, enemy.rect.centery,
                            EXPLOSION_PARTICLE_COUNT, EXPLOSION_COLOR
                        )
                    if sound_manager:
                        sound_manager.play_sound('explosion')
                self.enemies.remove(enemy)
    
    def render(self, screen: pygame.Surface):
        """Render all enemies."""
        for enemy in self.enemies:
            if enemy.active:
                enemy.render(screen)
    
    def all_enemies_defeated(self) -> bool:
        """Check if all enemies are defeated."""
        return len([e for e in self.enemies if e.active]) == 0 and self.spawn_timer < self.spawn_rate
    
    def get_active_enemies(self) -> List[Enemy]:
        """Get all active enemies."""
        return [e for e in self.enemies if e.active]
    
    def count_active_enemies(self) -> int:
        """Count active enemies."""
        return len(self.get_active_enemies())

