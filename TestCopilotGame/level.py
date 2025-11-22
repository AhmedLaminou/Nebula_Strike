"""
TestCopilotGame - Level Management System
Handles level progression, enemy spawning, and boss triggering.
"""

import random
from typing import Optional
from settings import *


class LevelManager:
    """Manages level progression and spawning logic."""
    
    def __init__(self):
        """Initialize level manager."""
        self.current_level = 1
        self.enemies_spawned = 0
        self.enemies_required = 0
        self.enemies_defeated = 0
        self.level_complete = False
        self.boss_spawned = False
        self.boss_defeated = False
        
        # Level progression
        self.wave_count = 0
        self.current_wave = 0
        self.enemies_per_wave = ENEMY_COUNT_PER_WAVE
        self.wave_complete = False
        self.wave_timer = 0.0
        self.wave_delay = 2.0
        
        # Boss spawning
        self.boss_spawn_level = BOSS_SPAWN_LEVEL
        self.boss_spawned_this_level = False
    
    def reset(self):
        """Reset level manager."""
        self.enemies_spawned = 0
        self.enemies_required = 0
        self.enemies_defeated = 0
        self.level_complete = False
        self.boss_spawned = False
        self.boss_defeated = False
        self.wave_count = 0
        self.current_wave = 0
        self.wave_complete = False
        self.wave_timer = 0.0
        self.boss_spawned_this_level = False
    
    def set_level(self, level: int):
        """Set the current level and calculate requirements."""
        self.current_level = level
        self.reset()
        
        # Calculate enemies required for this level
        self.enemies_required = int(
            ENEMY_COUNT_PER_WAVE * (LEVEL_ENEMY_COUNT_MULTIPLIER ** (level - 1))
        )
        
        # Calculate number of waves
        self.enemies_per_wave = int(
            ENEMY_COUNT_PER_WAVE * (LEVEL_ENEMY_COUNT_MULTIPLIER ** ((level - 1) * 0.5))
        )
        self.wave_count = max(1, (self.enemies_required + self.enemies_per_wave - 1) // self.enemies_per_wave)
        
        # Boss spawning
        self.boss_spawn_level = BOSS_SPAWN_LEVEL
        if level >= self.boss_spawn_level:
            self.boss_spawn_level = level
        
        # Reset boss flag
        self.boss_spawned_this_level = False
    
    def update(self, dt: float, active_enemies: int, defeated_count: int):
        """Update level progress."""
        self.enemies_defeated = defeated_count
        
        # Check if wave is complete
        if active_enemies == 0 and not self.wave_complete:
            self.wave_timer += dt
            if self.wave_timer >= self.wave_delay:
                self.wave_complete = True
                self.current_wave += 1
                self.wave_timer = 0.0
        
        # Check if level is complete
        if self.enemies_defeated >= self.enemies_required:
            if not self.boss_spawn_level or self.boss_spawned_this_level:
                # All enemies defeated and boss handled
                self.level_complete = True
        else:
            self.level_complete = False
    
    def should_spawn_enemies(self) -> bool:
        """Check if more enemies should be spawned."""
        if self.level_complete:
            return False
        
        # Spawn enemies in waves
        if self.current_wave < self.wave_count:
            if self.wave_complete or self.current_wave == 0:
                return True
        
        return False
    
    def get_enemies_to_spawn(self) -> int:
        """Get number of enemies to spawn in current wave."""
        if not self.should_spawn_enemies():
            return 0
        
        remaining = self.enemies_required - self.enemies_spawned
        return min(self.enemies_per_wave, remaining)
    
    def mark_enemy_spawned(self):
        """Mark that an enemy was spawned."""
        self.enemies_spawned += 1
        self.wave_complete = False
        self.wave_timer = 0.0
    
    def mark_boss_spawned(self):
        """Mark that boss was spawned."""
        self.boss_spawned = True
        self.boss_spawned_this_level = True
    
    def mark_boss_defeated(self):
        """Mark that boss was defeated."""
        self.boss_defeated = True
        self.level_complete = True
    
    def should_spawn_boss(self) -> bool:
        """Check if boss should be spawned."""
        # Boss spawns when all enemies are defeated
        if self.current_level >= self.boss_spawn_level:
            if not self.boss_spawned_this_level:
                if self.enemies_defeated >= self.enemies_required:
                    return True
        
        return False
    
    def get_boss_type(self) -> str:
        """Get boss type for current level."""
        # Boss type based on level
        if self.current_level < 5:
            return BOSS_TYPE_BASIC
        elif self.current_level < 10:
            return random.choice([BOSS_TYPE_BASIC, BOSS_TYPE_TWIN])
        elif self.current_level < 15:
            return random.choice([BOSS_TYPE_TWIN, BOSS_TYPE_MEGA])
        elif self.current_level < 20:
            if self.current_level % 5 == 0:
                return BOSS_TYPE_FINAL
            return random.choice([BOSS_TYPE_TWIN, BOSS_TYPE_MEGA])
        else:
            if self.current_level % 10 == 0:
                return BOSS_TYPE_FINAL
            return random.choice([BOSS_TYPE_TWIN, BOSS_TYPE_MEGA, BOSS_TYPE_FINAL])
    
    def is_level_complete(self) -> bool:
        """Check if level is complete."""
        return self.level_complete
    
    def complete_boss(self):
        """Complete boss fight."""
        self.mark_boss_defeated()
    
    def get_level_progress(self) -> float:
        """Get level completion progress (0.0 to 1.0)."""
        if self.enemies_required == 0:
            return 1.0
        return min(1.0, self.enemies_defeated / self.enemies_required)
    
    def get_level_info(self) -> dict:
        """Get information about current level."""
        return {
            'level': self.current_level,
            'enemies_defeated': self.enemies_defeated,
            'enemies_required': self.enemies_required,
            'wave': self.current_wave,
            'waves_total': self.wave_count,
            'progress': self.get_level_progress(),
            'boss_spawned': self.boss_spawned_this_level,
            'complete': self.level_complete
        }

