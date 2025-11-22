"""
Nebula Strike - Main Entry Point
A comprehensive space shooter game built with Pygame.
Features: Multiple enemy types, power-ups, boss battles, particle effects, and more.
"""

import pygame
import sys
from enum import Enum

from settings import *
from player import Player
from enemies import EnemyManager
from bullets import BulletManager
from powerups import PowerUpManager
from particles import ParticleManager
from background import BackgroundManager
from bosses import BossManager
from ui import UIManager
from level import LevelManager
from sound_manager import SoundManager
from save_system import SaveSystem
from utils import FadeTransition


class GameState(Enum):
    """Enumeration of all game states."""
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3
    OPTIONS = 4
    HIGH_SCORES = 5
    LEVEL_COMPLETE = 6
    BOSS_FIGHT = 7


class Game:
    """Main game class that manages the game loop and all game systems."""
    
    def __init__(self):
        """Initialize the game and all its systems."""
        pygame.init()
        
        # Create display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.state = GameState.MENU
        self.previous_state = None
        self.score = 0
        self.level = 1
        self.lives = STARTING_LIVES
        self.game_over_timer = 0
        
        # Initialize managers
        self.sound_manager = SoundManager()
        self.save_system = SaveSystem()
        self.background_manager = BackgroundManager()
        self.particle_manager = ParticleManager()
        self.bullet_manager = BulletManager()
        self.powerup_manager = PowerUpManager()
        self.enemy_manager = EnemyManager()
        self.boss_manager = BossManager()
        self.level_manager = LevelManager()
        self.ui_manager = UIManager()
        
        # Initialize player
        self.player = None
        self.reset_game()
        
        # Fade transition
        self.fade_transition = FadeTransition(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Pause state
        self.paused = False
        self.pause_cooldown = 0
        
        # Initialize sound
        self.sound_manager.play_music('menu', loop=True)
    
    def reset_game(self):
        """Reset all game systems for a new game."""
        self.score = 0
        self.level = 1
        self.lives = STARTING_LIVES
        
        # Reset managers
        self.bullet_manager.reset()
        self.powerup_manager.reset()
        self.enemy_manager.reset()
        self.boss_manager.reset()
        self.particle_manager.reset()
        self.level_manager.reset()
        
        # Create new player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        
        # Initialize level
        self.level_manager.set_level(self.level)
        self.enemy_manager.set_level(self.level)
        self.boss_manager.set_level(self.level)
    
    def handle_events(self):
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                        self.sound_manager.pause_music()
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                        self.sound_manager.resume_music()
                    elif self.state in [GameState.MENU, GameState.GAME_OVER, GameState.OPTIONS, GameState.HIGH_SCORES]:
                        if self.state != GameState.MENU:
                            self.state = GameState.MENU
                        else:
                            self.running = False
                
                elif event.key == pygame.K_RETURN:
                    if self.state == GameState.MENU:
                        self.start_game()
                    elif self.state == GameState.GAME_OVER:
                        if self.game_over_timer > 2.0:
                            self.save_score()
                            self.reset_game()
                            self.state = GameState.MENU
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                        self.sound_manager.resume_music()
                
                elif event.key == pygame.K_h:
                    if self.state == GameState.MENU:
                        self.state = GameState.HIGH_SCORES
                
                elif event.key == pygame.K_o:
                    if self.state == GameState.MENU:
                        self.state = GameState.OPTIONS
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.MENU:
                    mouse_pos = pygame.mouse.get_pos()
                    button = self.ui_manager.check_menu_click(mouse_pos)
                    if button == 'start':
                        self.start_game()
                    elif button == 'high_scores':
                        self.state = GameState.HIGH_SCORES
                    elif button == 'options':
                        self.state = GameState.OPTIONS
                    elif button == 'quit':
                        self.running = False
                
                elif self.state == GameState.GAME_OVER:
                    if self.game_over_timer > 2.0:
                        self.save_score()
                        self.reset_game()
                        self.state = GameState.MENU
            
            # Handle UI button clicks
            if self.state == GameState.OPTIONS:
                mouse_pos = pygame.mouse.get_pos()
                action = self.ui_manager.handle_options_click(mouse_pos)
                if action == 'back':
                    self.state = GameState.MENU
                elif action == 'toggle_sound':
                    self.sound_manager.toggle_sound()
                elif action == 'toggle_music':
                    self.sound_manager.toggle_music()
            
            if self.state == GameState.HIGH_SCORES:
                mouse_pos = pygame.mouse.get_pos()
                action = self.ui_manager.handle_high_scores_click(mouse_pos)
                if action == 'back':
                    self.state = GameState.MENU
    
    def start_game(self):
        """Start a new game."""
        self.reset_game()
        self.state = GameState.PLAYING
        self.sound_manager.play_music('gameplay', loop=True)
        self.fade_transition.start_fade_out()
    
    def update(self, dt):
        """Update all game systems."""
        dt = min(dt, 0.1)  # Cap delta time to prevent large jumps
        
        # Update fade transition
        self.fade_transition.update(dt)
        
        if self.state == GameState.PLAYING:
            # Update background
            self.background_manager.update(dt)
            
            # Update player
            if self.player:
                self.player.update(dt, self.bullet_manager, self.sound_manager)
                
                # Check player death
                if self.player.is_dead():
                    self.lives -= 1
                    if self.lives > 0:
                        # Respawn player
                        self.particle_manager.create_explosion(
                            self.player.rect.centerx, self.player.rect.centery,
                            EXPLOSION_PARTICLE_COUNT, EXPLOSION_COLOR
                        )
                        self.sound_manager.play_sound('explosion')
                        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
                    else:
                        # Game over
                        self.game_over()
            
            # Update managers
            self.bullet_manager.update(dt)
            self.powerup_manager.update(dt)
            self.enemy_manager.update(dt, self.bullet_manager, self.particle_manager, self.sound_manager)
            self.boss_manager.update(dt, self.bullet_manager, self.particle_manager, self.sound_manager)
            self.particle_manager.update(dt)
            
            # Check collisions
            self.check_collisions()
            
            # Check level progression
            if self.enemy_manager.all_enemies_defeated() and not self.boss_manager.has_active_boss():
                if self.level_manager.is_level_complete():
                    self.complete_level()
            
            # Check boss spawning
            if self.level_manager.should_spawn_boss():
                if not self.boss_manager.has_active_boss():
                    boss_type = self.level_manager.get_boss_type()
                    self.boss_manager.spawn_boss(boss_type)
                    self.state = GameState.BOSS_FIGHT
                    self.sound_manager.play_music('boss', loop=True)
            
            # Check if boss is defeated
            if self.state == GameState.BOSS_FIGHT:
                if not self.boss_manager.has_active_boss():
                    self.score += BOSS_DEFEAT_BONUS
                    self.state = GameState.PLAYING
                    self.sound_manager.play_music('gameplay', loop=True)
                    self.level_manager.complete_boss()
        
        elif self.state == GameState.GAME_OVER:
            self.game_over_timer += dt
    
    def check_collisions(self):
        """Check all collision types in the game."""
        if not self.player or self.player.is_dead():
            return
        
        player_rect = self.player.rect
        
        # Player bullets vs enemies
        for bullet in self.bullet_manager.player_bullets[:]:
            if bullet.active:
                for enemy in self.enemy_manager.enemies[:]:
                    if enemy.active and bullet.rect.colliderect(enemy.rect):
                        enemy.take_damage(bullet.damage)
                        bullet.active = False
                        if enemy.is_dead():
                            self.score += enemy.score_value
                            self.powerup_manager.spawn_powerup_chance(enemy.rect.centerx, enemy.rect.centery)
                        self.sound_manager.play_sound('hit')
                        break
        
        # Player bullets vs boss
        if self.boss_manager.has_active_boss():
            boss = self.boss_manager.get_active_boss()
            for bullet in self.bullet_manager.player_bullets[:]:
                if bullet.active and bullet.rect.colliderect(boss.rect):
                    boss.take_damage(bullet.damage)
                    bullet.active = False
                    self.particle_manager.create_hit_sparks(
                        bullet.rect.centerx, bullet.rect.centery, 5
                    )
                    self.sound_manager.play_sound('hit')
        
        # Enemy bullets vs player
        if not self.player.is_dead():
            for bullet in self.bullet_manager.enemy_bullets[:]:
                if bullet.active and bullet.rect.colliderect(player_rect):
                    self.player.take_damage(bullet.damage)
                    bullet.active = False
                    self.particle_manager.create_hit_sparks(
                        bullet.rect.centerx, bullet.rect.centery, 8
                    )
                    self.sound_manager.play_sound('player_hit')
        
        # Boss bullets vs player
        if self.boss_manager.has_active_boss() and not self.player.is_dead():
            boss = self.boss_manager.get_active_boss()
            for bullet in self.bullet_manager.boss_bullets[:]:
                if bullet.active and bullet.rect.colliderect(player_rect):
                    self.player.take_damage(bullet.damage)
                    bullet.active = False
                    self.particle_manager.create_hit_sparks(
                        bullet.rect.centerx, bullet.rect.centery, 10
                    )
                    self.sound_manager.play_sound('player_hit')
        
        # Player vs enemies
        for enemy in self.enemy_manager.enemies[:]:
            if enemy.active and not self.player.is_dead() and player_rect.colliderect(enemy.rect):
                self.player.take_damage(enemy.collision_damage)
                enemy.take_damage(1000)  # Instant kill enemy on collision
                self.particle_manager.create_explosion(
                    enemy.rect.centerx, enemy.rect.centery,
                    EXPLOSION_PARTICLE_COUNT // 2, EXPLOSION_COLOR
                )
                self.sound_manager.play_sound('explosion')
        
        # Player vs boss
        if self.boss_manager.has_active_boss() and not self.player.is_dead():
            boss = self.boss_manager.get_active_boss()
            if player_rect.colliderect(boss.rect):
                self.player.take_damage(boss.collision_damage)
                self.particle_manager.create_hit_sparks(
                    boss.rect.centerx, boss.rect.centery, 20
                )
                self.sound_manager.play_sound('player_hit')
        
        # Player vs powerups
        for powerup in self.powerup_manager.powerups[:]:
            if powerup.active and player_rect.colliderect(powerup.rect):
                powerup.apply_effect(self.player, self.bullet_manager)
                powerup.active = False
                self.particle_manager.create_collect_effect(
                    powerup.rect.centerx, powerup.rect.centery
                )
                self.sound_manager.play_sound('powerup')
    
    def complete_level(self):
        """Handle level completion."""
        self.level += 1
        self.score += LEVEL_COMPLETE_BONUS * self.level
        self.level_manager.set_level(self.level)
        self.enemy_manager.set_level(self.level)
        self.boss_manager.set_level(self.level)
        self.state = GameState.LEVEL_COMPLETE
        self.sound_manager.play_sound('level_complete')
        
        # Reset player position
        if self.player:
            self.player.rect.centerx = SCREEN_WIDTH // 2
            self.player.rect.centery = SCREEN_HEIGHT - 100
    
    def game_over(self):
        """Handle game over."""
        self.state = GameState.GAME_OVER
        self.game_over_timer = 0
        self.sound_manager.play_music('game_over', loop=True)
        self.sound_manager.play_sound('game_over')
        self.particle_manager.create_explosion(
            self.player.rect.centerx, self.player.rect.centery,
            EXPLOSION_PARTICLE_COUNT * 2, EXPLOSION_COLOR
        )
    
    def save_score(self):
        """Save high score if applicable."""
        if self.score > 0:
            self.save_system.add_score(self.score, self.level)
    
    def render(self):
        """Render all game elements."""
        self.screen.fill(BG_COLOR)
        
        if self.state == GameState.MENU:
            self.background_manager.render(self.screen)
            self.ui_manager.render_menu(self.screen, self.score, self.save_system.get_high_score())
        
        elif self.state == GameState.PLAYING or self.state == GameState.BOSS_FIGHT:
            # Render game
            self.background_manager.render(self.screen)
            self.particle_manager.render(self.screen)
            self.powerup_manager.render(self.screen)
            self.bullet_manager.render(self.screen)
            self.enemy_manager.render(self.screen)
            self.boss_manager.render(self.screen)
            if self.player:
                self.player.render(self.screen)
            self.ui_manager.render_hud(self.screen, self.player, self.score, self.lives, self.level)
        
        elif self.state == GameState.PAUSED:
            # Render game first
            self.background_manager.render(self.screen)
            self.particle_manager.render(self.screen)
            self.powerup_manager.render(self.screen)
            self.bullet_manager.render(self.screen)
            self.enemy_manager.render(self.screen)
            self.boss_manager.render(self.screen)
            if self.player:
                self.player.render(self.screen)
            self.ui_manager.render_hud(self.screen, self.player, self.score, self.lives, self.level)
            # Then overlay pause screen
            self.ui_manager.render_pause(self.screen)
        
        elif self.state == GameState.GAME_OVER:
            self.background_manager.render(self.screen)
            self.ui_manager.render_game_over(self.screen, self.score, self.level, self.save_system.get_high_score())
        
        elif self.state == GameState.LEVEL_COMPLETE:
            self.background_manager.render(self.screen)
            self.ui_manager.render_level_complete(self.screen, self.level)
        
        elif self.state == GameState.OPTIONS:
            self.background_manager.render(self.screen)
            self.ui_manager.render_options(self.screen, self.sound_manager)
        
        elif self.state == GameState.HIGH_SCORES:
            self.background_manager.render(self.screen)
            self.ui_manager.render_high_scores(self.screen, self.save_system.get_scores())
        
        # Render fade transition
        if self.fade_transition.is_active():
            self.fade_transition.render(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        # Save on exit
        self.save_score()
        pygame.quit()
        sys.exit()


def main():
    """Entry point of the game."""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)


def run_game():
    """Alternative entry point for testing."""
    main()


def get_version():
    """Get game version information."""
    return "1.0.0"


def get_build_info():
    """Get build information."""
    import os
    import datetime
    
    build_info = {
        'version': get_version(),
        'build_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'python_version': sys.version,
        'pygame_version': pygame.version.ver,
    }
    return build_info


if __name__ == '__main__':
    # Print build info in debug mode
    if DEBUG:
        build_info = get_build_info()
        print("Game Build Information:")
        for key, value in build_info.items():
            print(f"  {key}: {value}")
        print()
    
    main()

