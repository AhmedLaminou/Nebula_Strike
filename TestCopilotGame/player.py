"""
TestCopilotGame - Player Class
Handles player ship movement, shooting, upgrades, and state.
"""

import pygame
import math
from typing import List
from settings import *
from utils import clamp, distance


class Player:
    """Player ship with movement, shooting, and upgrade systems."""
    
    def __init__(self, x: float, y: float):
        """Initialize the player ship."""
        self.x = float(x)
        self.y = float(y)
        self.width = PLAYER_SIZE[0]
        self.height = PLAYER_SIZE[1]
        
        # Create rect for collision
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.rect.center = (int(self.x), int(self.y))
        
        # Stats
        self.max_health = PLAYER_HEALTH
        self.health = self.max_health
        self.speed = PLAYER_SPEED
        self.base_speed = PLAYER_SPEED
        
        # Shooting
        self.bullet_damage = BULLET_DAMAGE
        self.base_damage = BULLET_DAMAGE
        self.fire_cooldown = 0.0
        self.bullet_cooldown_time = BULLET_COOLDOWN
        self.can_shoot = True
        
        # Weapon upgrades
        self.weapon_level = 1
        self.max_weapon_level = WEAPON_LEVEL_MAX
        self.multi_shot = False
        self.multi_shot_count = 1
        self.multi_shot_angle = 0
        self.rapid_fire = False
        
        # Power-ups
        self.speed_multiplier = 1.0
        self.damage_multiplier = 1.0
        self.shield_active = False
        self.shield_duration = 0.0
        self.shield_health = 0
        self.shield_max_health = 50
        
        # State
        self.alive = True
        self.invulnerable = False
        self.invulnerability_timer = 0.0
        self.invulnerability_duration = PLAYER_INVULNERABILITY_TIME
        self.blink_timer = 0.0
        self.blink_interval = PLAYER_BLINK_INTERVAL
        self.visible = True
        
        # Movement
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.acceleration = 2000.0
        self.friction = 0.85
        
        # Visual
        self.color = PLAYER_COLOR
        self.base_color = PLAYER_COLOR
        self.shield_color = SHIELD_POWERUP_COLOR
        self.angle = -math.pi / 2  # Face upward
        self.thrust_particles = []
        
        # Input state
        self.keys = pygame.key.get_pressed()
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.shooting = False
        
        # Animation
        self.animation_frame = 0
        self.animation_time = 0.0
        
        # Trail effect
        self.trail_positions = []
        self.max_trail_length = 5
        
        # Special abilities
        self.special_ability_cooldown = 0.0
        self.special_ability_duration = 0.0
        self.has_special_ability = False
        self.special_ability_active = False
        self.special_ability_type = None  # 'shield', 'burst', 'laser'
    
    def update(self, dt: float, bullet_manager, sound_manager):
        """Update player state and handle input."""
        # Get input
        self.keys = pygame.key.get_pressed()
        self.handle_input()
        
        # Update movement
        self.update_movement(dt)
        
        # Update shooting
        self.update_shooting(dt, bullet_manager, sound_manager)
        
        # Update power-ups
        self.update_powerups(dt)
        
        # Update invulnerability
        self.update_invulnerability(dt)
        
        # Update special abilities
        self.update_special_abilities(dt)
        
        # Update trail
        self.update_trail()
        
        # Update animation
        self.update_animation(dt)
        
        # Update rect
        self.rect.center = (int(self.x), int(self.y))
        
        # Clamp to screen
        self.x = clamp(self.x, self.width // 2, SCREEN_WIDTH - self.width // 2)
        self.y = clamp(self.y, self.height // 2, SCREEN_HEIGHT - self.height // 2)
    
    def handle_input(self):
        """Handle keyboard input for movement and shooting."""
        # Movement - WASD or Arrow keys
        self.moving_left = (self.keys[pygame.K_a] or self.keys[pygame.K_LEFT])
        self.moving_right = (self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT])
        self.moving_up = (self.keys[pygame.K_w] or self.keys[pygame.K_UP])
        self.moving_down = (self.keys[pygame.K_s] or self.keys[pygame.K_DOWN])
        
        # Shooting - Space or mouse
        mouse_buttons = pygame.mouse.get_pressed()
        self.shooting = (self.keys[pygame.K_SPACE] or mouse_buttons[0])
        
        # Special ability - Shift
        if self.keys[pygame.K_LSHIFT] or self.keys[pygame.K_RSHIFT]:
            self.activate_special_ability()
    
    def update_movement(self, dt: float):
        """Update player movement with acceleration and friction."""
        # Calculate target velocity
        target_vx = 0.0
        target_vy = 0.0
        
        if self.moving_left:
            target_vx = -self.speed * self.speed_multiplier
        elif self.moving_right:
            target_vx = self.speed * self.speed_multiplier
        
        if self.moving_up:
            target_vy = -self.speed * self.speed_multiplier
        elif self.moving_down:
            target_vy = self.speed * self.speed_multiplier
        
        # Apply acceleration
        if target_vx != 0:
            self.velocity_x = lerp(self.velocity_x, target_vx, dt * self.acceleration / self.speed)
        else:
            self.velocity_x *= self.friction
        
        if target_vy != 0:
            self.velocity_y = lerp(self.velocity_y, target_vy, dt * self.acceleration / self.speed)
        else:
            self.velocity_y *= self.friction
        
        # Apply velocity
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Update angle for visual direction
        if self.velocity_x != 0 or self.velocity_y != 0:
            self.angle = math.atan2(self.velocity_y, self.velocity_x) + math.pi / 2
        else:
            # Face upward when not moving
            self.angle = -math.pi / 2
    
    def update_shooting(self, dt: float, bullet_manager, sound_manager):
        """Update shooting mechanics."""
        # Update cooldown
        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt
        else:
            self.can_shoot = True
        
        # Fire bullets
        if self.shooting and self.can_shoot and self.alive:
            self.fire_bullets(bullet_manager, sound_manager)
            
            # Set cooldown
            cooldown = self.bullet_cooldown_time
            if self.rapid_fire:
                cooldown = RAPID_FIRE_COOLDOWN
            if self.weapon_level > 1:
                cooldown *= (WEAPON_UPGRADE_FIRE_RATE_INCREASE ** (self.weapon_level - 1))
            
            self.fire_cooldown = cooldown
            self.can_shoot = False
    
    def fire_bullets(self, bullet_manager, sound_manager):
        """Fire bullets from player."""
        if not bullet_manager:
            return
        
        # Calculate bullet start position
        bullet_x = self.x
        bullet_y = self.y - self.height // 2 - 10
        
        # Base damage
        damage = self.bullet_damage * self.damage_multiplier
        if self.weapon_level > 1:
            damage *= (WEAPON_UPGRADE_DAMAGE_INCREASE ** (self.weapon_level - 1))
        
        # Single shot
        if not self.multi_shot:
            bullet_manager.create_player_bullet(
                bullet_x, bullet_y, 0, -BULLET_SPEED, damage, self.weapon_level
            )
        else:
            # Multi-shot
            angle_spread = self.multi_shot_angle if self.multi_shot_angle > 0 else MULTI_SHOT_ANGLE
            count = self.multi_shot_count if self.multi_shot_count > 1 else MULTI_SHOT_COUNT
            start_angle = -angle_spread * (count - 1) / 2
            
            import math as m
            for i in range(count):
                angle = start_angle + i * angle_spread
                angle_rad = math.radians(angle)
                vx = math.sin(angle_rad) * BULLET_SPEED
                vy = -math.cos(angle_rad) * BULLET_SPEED
                bullet_manager.create_player_bullet(
                    bullet_x, bullet_y, vx, vy, damage, self.weapon_level
                )
        
        # Play sound
        if sound_manager:
            sound_manager.play_sound('shoot')
    
    def update_powerups(self, dt: float):
        """Update active power-up effects."""
        # Update shield
        if self.shield_active:
            self.shield_duration -= dt
            if self.shield_duration <= 0:
                self.shield_active = False
                self.shield_health = 0
    
    def update_invulnerability(self, dt: float):
        """Update invulnerability state and blinking."""
        if self.invulnerable:
            self.invulnerability_timer -= dt
            self.blink_timer -= dt
            
            if self.blink_timer <= 0:
                self.visible = not self.visible
                self.blink_timer = self.blink_interval
            
            if self.invulnerability_timer <= 0:
                self.invulnerable = False
                self.visible = True
        else:
            self.visible = True
    
    def update_special_abilities(self, dt: float):
        """Update special ability cooldowns and durations."""
        if self.special_ability_cooldown > 0:
            self.special_ability_cooldown -= dt
        
        if self.special_ability_active:
            self.special_ability_duration -= dt
            if self.special_ability_duration <= 0:
                self.special_ability_active = False
                self.deactivate_special_ability()
    
    def update_trail(self):
        """Update trail effect for player movement."""
        if len(self.trail_positions) >= self.max_trail_length:
            self.trail_positions.pop(0)
        self.trail_positions.append((self.x, self.y))
    
    def update_animation(self, dt: float):
        """Update animation frames."""
        self.animation_time += dt
        if self.animation_time >= 1.0 / ANIMATION_FPS:
            self.animation_frame = (self.animation_frame + 1) % 4
            self.animation_time = 0.0
    
    def take_damage(self, amount: float):
        """Apply damage to player."""
        if self.invulnerable or not self.alive:
            return
        
        # Shield absorbs damage first
        if self.shield_active and self.shield_health > 0:
            damage_to_shield = min(amount, self.shield_health)
            self.shield_health -= damage_to_shield
            amount -= damage_to_shield
            if self.shield_health <= 0:
                self.shield_active = False
        
        # Apply remaining damage to health
        if amount > 0:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.alive = False
            else:
                # Become invulnerable after taking damage
                self.invulnerable = True
                self.invulnerability_timer = self.invulnerability_duration
    
    def heal(self, amount: float):
        """Heal the player."""
        self.health = min(self.max_health, self.health + amount)
    
    def is_dead(self) -> bool:
        """Check if player is dead."""
        return not self.alive or self.health <= 0
    
    def activate_special_ability(self):
        """Activate special ability if available."""
        if not self.has_special_ability or self.special_ability_active:
            return
        if self.special_ability_cooldown > 0:
            return
        
        self.special_ability_active = True
        self.special_ability_duration = 5.0
        
        if self.special_ability_type == 'shield':
            self.shield_active = True
            self.shield_health = self.shield_max_health
            self.shield_duration = 10.0
        elif self.special_ability_type == 'burst':
            # Fire burst of bullets
            pass  # Implement in bullet manager
        elif self.special_ability_type == 'laser':
            # Activate laser
            pass  # Implement in bullet manager
    
    def deactivate_special_ability(self):
        """Deactivate special ability."""
        if self.special_ability_type == 'shield' and not self.shield_duration > 0:
            self.shield_active = False
    
    # Power-up application methods
    def apply_health_powerup(self):
        """Apply health power-up effect."""
        self.heal(HEALTH_POWERUP_HEAL)
    
    def apply_speed_powerup(self, duration: float):
        """Apply speed power-up effect."""
        self.speed_multiplier = SPEED_POWERUP_MULTIPLIER
    
    def apply_damage_powerup(self, duration: float):
        """Apply damage power-up effect."""
        self.damage_multiplier = DAMAGE_POWERUP_MULTIPLIER
    
    def apply_shield_powerup(self, duration: float):
        """Apply shield power-up effect."""
        self.shield_active = True
        self.shield_duration = duration
        self.shield_health = self.shield_max_health
    
    def apply_rapid_fire_powerup(self, duration: float):
        """Apply rapid fire power-up effect."""
        self.rapid_fire = True
    
    def apply_multi_shot_powerup(self, duration: float):
        """Apply multi-shot power-up effect."""
        self.multi_shot = True
        self.multi_shot_count = MULTI_SHOT_COUNT
        self.multi_shot_angle = MULTI_SHOT_ANGLE
    
    def upgrade_weapon(self):
        """Upgrade weapon level."""
        if self.weapon_level < self.max_weapon_level:
            self.weapon_level += 1
            self.bullet_damage = self.base_damage * (WEAPON_UPGRADE_DAMAGE_INCREASE ** (self.weapon_level - 1))
    
    def reset_powerup_effects(self):
        """Reset all temporary power-up effects."""
        self.speed_multiplier = 1.0
        self.damage_multiplier = 1.0
        self.rapid_fire = False
        self.multi_shot = False
    
    def render(self, screen: pygame.Surface):
        """Render the player ship."""
        if not self.visible:
            return
        
        # Draw trail
        self.render_trail(screen)
        
        # Draw shield
        if self.shield_active and self.shield_health > 0:
            shield_alpha = int(128 + 127 * (self.shield_health / self.shield_max_health))
            shield_surface = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (*self.shield_color, shield_alpha), 
                             (self.width // 2 + 10, self.height // 2 + 10), 
                             (self.width + self.height) // 2, 3)
            screen.blit(shield_surface, (self.rect.x - 10, self.rect.y - 10))
        
        # Draw player ship
        self.render_ship(screen)
        
        # Draw health bar if damaged
        if self.health < self.max_health:
            self.render_health_bar(screen)
    
    def render_ship(self, screen: pygame.Surface):
        """Render the player ship body."""
        # Create a simple triangle ship
        points = [
            (self.rect.centerx, self.rect.centery - self.height // 2),
            (self.rect.centerx - self.width // 2, self.rect.centery + self.height // 2),
            (self.rect.centerx + self.width // 2, self.rect.centery + self.height // 2)
        ]
        
        # Rotate points based on angle
        import math
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        cx, cy = self.rect.center
        
        rotated_points = []
        for px, py in points:
            # Translate to origin
            tx = px - cx
            ty = py - cy
            # Rotate
            rx = tx * cos_a - ty * sin_a
            ry = tx * sin_a + ty * cos_a
            # Translate back
            rotated_points.append((int(rx + cx), int(ry + cy)))
        
        # Choose color based on state
        color = self.color
        if self.invulnerable:
            # Pulsing color when invulnerable
            import time
            pulse = (time.time() * 10) % 2 < 1
            color = YELLOW if pulse else self.color
        
        pygame.draw.polygon(screen, color, rotated_points)
        pygame.draw.polygon(screen, WHITE, rotated_points, 2)
        
        # Draw engine glow
        if self.velocity_x != 0 or self.velocity_y != 0:
            engine_points = [
                (self.rect.centerx - 5, self.rect.centery + self.height // 2),
                (self.rect.centerx + 5, self.rect.centery + self.height // 2),
                (self.rect.centerx, self.rect.centery + self.height // 2 + 15)
            ]
            pygame.draw.polygon(screen, ORANGE, engine_points)
            pygame.draw.polygon(screen, YELLOW, engine_points)
    
    def render_trail(self, screen: pygame.Surface):
        """Render movement trail."""
        for i, (tx, ty) in enumerate(self.trail_positions):
            alpha = int(255 * (i / len(self.trail_positions)) * 0.3)
            size = int(5 * (i / len(self.trail_positions)))
            if size > 0:
                trail_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, (*self.color, alpha), (size, size), size)
                screen.blit(trail_surface, (tx - size, ty - size))
    
    def render_health_bar(self, screen: pygame.Surface):
        """Render health bar above player."""
        bar_width = 40
        bar_height = 5
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 15
        
        # Background
        pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Health fill
        health_ratio = self.health / self.max_health
        fill_width = int(bar_width * health_ratio)
        health_color = GREEN if health_ratio > 0.5 else (YELLOW if health_ratio > 0.25 else RED)
        if fill_width > 0:
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, fill_width, bar_height))


# Helper function for lerp (needed by player)
def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolation."""
    return start + (end - start) * t

