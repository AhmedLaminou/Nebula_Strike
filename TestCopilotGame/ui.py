"""
TestCopilotGame - UI System
Manages all UI elements including HUD, menus, and screens.
"""

import pygame
import math
from typing import List, Tuple, Optional
from settings import *
from utils import draw_text, draw_progress_bar, format_number, format_time
from player import Player
from sound_manager import SoundManager
from save_system import SaveSystem


class Button:
    """UI button class."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 color: tuple = LIGHT_GRAY, text_color: tuple = BLACK, action: str = None):
        """Initialize a button."""
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action
        self.hovered = False
        self.clicked = False
        self.font = pygame.font.Font(None, FONT_SIZE_SMALL)
    
    def update(self, mouse_pos: Tuple[int, int], mouse_clicked: bool):
        """Update button state."""
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.clicked = mouse_clicked and self.hovered
    
    def render(self, screen: pygame.Surface):
        """Render the button."""
        # Choose color based on state
        color = self.color
        if self.hovered:
            # Lighter when hovered
            color = tuple(min(255, c + 30) for c in self.color)
        
        # Draw button
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class UIManager:
    """Manages all UI elements and screens."""
    
    def __init__(self):
        """Initialize UI manager."""
        # Fonts
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.font_tiny = pygame.font.Font(None, FONT_SIZE_TINY)
        
        # Menu buttons
        self.menu_buttons: List[Button] = []
        self.options_buttons: List[Button] = []
        self.high_scores_buttons: List[Button] = []
        
        # Create buttons
        self.create_menu_buttons()
        self.create_options_buttons()
        self.create_high_scores_buttons()
        
        # UI state
        self.selected_button = 0
    
    def create_menu_buttons(self):
        """Create main menu buttons."""
        center_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2 - 50
        
        buttons = [
            ('Start Game', 'start'),
            ('High Scores', 'high_scores'),
            ('Options', 'options'),
            ('Quit', 'quit')
        ]
        
        for i, (text, action) in enumerate(buttons):
            y = start_y + i * (BUTTON_HEIGHT + BUTTON_SPACING)
            button = Button(
                center_x - BUTTON_WIDTH // 2, y,
                BUTTON_WIDTH, BUTTON_HEIGHT,
                text, LIGHT_GRAY, BLACK, action
            )
            self.menu_buttons.append(button)
    
    def create_options_buttons(self):
        """Create options screen buttons."""
        center_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT - 150
        
        self.options_buttons.append(
            Button(
                center_x - BUTTON_WIDTH // 2, start_y,
                BUTTON_WIDTH, BUTTON_HEIGHT,
                'Toggle Sound', LIGHT_GRAY, BLACK, 'toggle_sound'
            )
        )
        self.options_buttons.append(
            Button(
                center_x - BUTTON_WIDTH // 2, start_y + BUTTON_HEIGHT + BUTTON_SPACING,
                BUTTON_WIDTH, BUTTON_HEIGHT,
                'Toggle Music', LIGHT_GRAY, BLACK, 'toggle_music'
            )
        )
        self.options_buttons.append(
            Button(
                center_x - BUTTON_WIDTH // 2, start_y + (BUTTON_HEIGHT + BUTTON_SPACING) * 2,
                BUTTON_WIDTH, BUTTON_HEIGHT,
                'Back', LIGHT_GRAY, BLACK, 'back'
            )
        )
    
    def create_high_scores_buttons(self):
        """Create high scores screen buttons."""
        center_x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT - 100
        
        self.high_scores_buttons.append(
            Button(
                center_x - BUTTON_WIDTH // 2, y,
                BUTTON_WIDTH, BUTTON_HEIGHT,
                'Back', LIGHT_GRAY, BLACK, 'back'
            )
        )
    
    def check_menu_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """Check if a menu button was clicked."""
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        for button in self.menu_buttons:
            button.update(mouse_pos, mouse_clicked)
            if button.clicked:
                return button.action
        
        return None
    
    def handle_options_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """Handle options screen clicks."""
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        for button in self.options_buttons:
            button.update(mouse_pos, mouse_clicked)
            if button.clicked:
                return button.action
        
        return None
    
    def handle_high_scores_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """Handle high scores screen clicks."""
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        for button in self.high_scores_buttons:
            button.update(mouse_pos, mouse_clicked)
            if button.clicked:
                return button.action
        
        return None
    
    def render_menu(self, screen: pygame.Surface, current_score: int, high_score: int):
        """Render main menu."""
        # Title
        title_text = "SPACE SHOOTER"
        title_surface = self.font_large.render(title_text, True, CYAN)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        
        # Shadow effect
        shadow_surface = self.font_large.render(title_text, True, BLACK)
        shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + 3, 153))
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = "TestCopilotGame"
        subtitle_surface = self.font_medium.render(subtitle_text, True, WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 220))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Render buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.menu_buttons:
            button.update(mouse_pos, False)
            button.render(screen)
        
        # High score display
        if high_score > 0:
            high_score_text = f"High Score: {format_number(high_score)}"
            score_surface = self.font_small.render(high_score_text, True, GOLD)
            score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(score_surface, score_rect)
        
        # Controls hint
        controls_text = "WASD/Arrows: Move | Space: Shoot | ESC: Pause"
        controls_surface = self.font_tiny.render(controls_text, True, LIGHT_GRAY)
        controls_rect = controls_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        screen.blit(controls_surface, controls_rect)
    
    def render_hud(self, screen: pygame.Surface, player: Optional[Player], score: int, lives: int, level: int):
        """Render game HUD."""
        # Score
        score_text = f"Score: {format_number(score)}"
        score_surface = self.font_small.render(score_text, True, WHITE)
        screen.blit(score_surface, (HUD_MARGIN, HUD_MARGIN))
        
        # Level
        level_text = f"Level: {level}"
        level_surface = self.font_small.render(level_text, True, WHITE)
        screen.blit(level_surface, (HUD_MARGIN, HUD_MARGIN + 30))
        
        # Lives
        lives_text = f"Lives: {lives}"
        lives_surface = self.font_small.render(lives_text, True, WHITE)
        screen.blit(lives_surface, (HUD_MARGIN, HUD_MARGIN + 60))
        
        # Player health bar
        if player and not player.is_dead():
            bar_x = HUD_MARGIN
            bar_y = SCREEN_HEIGHT - 50
            bar_width = 200
            bar_height = 20
            
            # Background
            pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
            
            # Health fill
            health_ratio = player.health / player.max_health
            fill_width = int(bar_width * health_ratio)
            
            # Color based on health
            health_color = GREEN if health_ratio > 0.5 else (YELLOW if health_ratio > 0.25 else RED)
            if fill_width > 0:
                pygame.draw.rect(screen, health_color, (bar_x, bar_y, fill_width, bar_height))
            
            # Border
            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
            
            # Health text
            health_text = f"{int(player.health)}/{int(player.max_health)}"
            health_surface = self.font_tiny.render(health_text, True, WHITE)
            screen.blit(health_surface, (bar_x + bar_width + 10, bar_y + 5))
        
        # Weapon level
        if player and not player.is_dead():
            weapon_text = f"Weapon Lv: {player.weapon_level}"
            weapon_surface = self.font_tiny.render(weapon_text, True, WHITE)
            screen.blit(weapon_surface, (HUD_MARGIN, SCREEN_HEIGHT - 80))
        
        # Power-up indicators
        if player and not player.is_dead():
            powerup_y = SCREEN_HEIGHT - 110
            powerup_x = HUD_MARGIN
            
            if player.speed_multiplier > 1.0:
                pygame.draw.circle(screen, SPEED_POWERUP_COLOR, (powerup_x + 10, powerup_y + 10), 8)
                powerup_x += 25
            
            if player.damage_multiplier > 1.0:
                pygame.draw.circle(screen, DAMAGE_POWERUP_COLOR, (powerup_x + 10, powerup_y + 10), 8)
                powerup_x += 25
            
            if player.shield_active:
                pygame.draw.circle(screen, SHIELD_POWERUP_COLOR, (powerup_x + 10, powerup_y + 10), 8)
                powerup_x += 25
            
            if player.rapid_fire:
                pygame.draw.circle(screen, RAPID_FIRE_COLOR, (powerup_x + 10, powerup_y + 10), 8)
                powerup_x += 25
            
            if player.multi_shot:
                pygame.draw.circle(screen, MULTI_SHOT_COLOR, (powerup_x + 10, powerup_y + 10), 8)
        
        # FPS counter (if enabled)
        if SHOW_FPS:
            fps_text = f"FPS: {pygame.time.Clock().get_fps():.1f}"
            fps_surface = self.font_tiny.render(fps_text, True, LIGHT_GRAY)
            screen.blit(fps_surface, (SCREEN_WIDTH - 100, HUD_MARGIN))
    
    def render_pause(self, screen: pygame.Surface):
        """Render pause screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = "PAUSED"
        pause_surface = self.font_large.render(pause_text, True, WHITE)
        pause_rect = pause_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(pause_surface, pause_rect)
        
        # Instructions
        inst_text = "Press ESC to Resume"
        inst_surface = self.font_medium.render(inst_text, True, LIGHT_GRAY)
        inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(inst_surface, inst_rect)
    
    def render_game_over(self, screen: pygame.Surface, final_score: int, level_reached: int, high_score: int):
        """Render game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = "GAME OVER"
        game_over_surface = self.font_large.render(game_over_text, True, RED)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(game_over_surface, game_over_rect)
        
        # Final score
        score_text = f"Final Score: {format_number(final_score)}"
        score_surface = self.font_medium.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(score_surface, score_rect)
        
        # Level reached
        level_text = f"Level Reached: {level_reached}"
        level_surface = self.font_medium.render(level_text, True, WHITE)
        level_rect = level_surface.get_rect(center=(SCREEN_WIDTH // 2, 350))
        screen.blit(level_surface, level_rect)
        
        # High score
        if high_score > 0:
            high_score_text = f"High Score: {format_number(high_score)}"
            high_score_surface = self.font_medium.render(high_score_text, True, GOLD)
            high_score_rect = high_score_surface.get_rect(center=(SCREEN_WIDTH // 2, 400))
            screen.blit(high_score_surface, high_score_rect)
        
        # New high score indicator
        if final_score > 0 and final_score >= high_score:
            new_record_text = "NEW HIGH SCORE!"
            new_record_surface = self.font_medium.render(new_record_text, True, YELLOW)
            new_record_rect = new_record_surface.get_rect(center=(SCREEN_WIDTH // 2, 450))
            screen.blit(new_record_surface, new_record_rect)
        
        # Continue text
        continue_text = "Press ENTER to return to menu"
        continue_surface = self.font_small.render(continue_text, True, LIGHT_GRAY)
        continue_rect = continue_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        screen.blit(continue_surface, continue_rect)
    
    def render_level_complete(self, screen: pygame.Surface, next_level: int):
        """Render level complete screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Level complete text
        complete_text = "LEVEL COMPLETE!"
        complete_surface = self.font_large.render(complete_text, True, GREEN)
        complete_rect = complete_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(complete_surface, complete_rect)
        
        # Next level text
        next_level_text = f"Level {next_level} Starting..."
        next_level_surface = self.font_medium.render(next_level_text, True, WHITE)
        next_level_rect = next_level_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(next_level_surface, next_level_rect)
    
    def render_options(self, screen: pygame.Surface, sound_manager: SoundManager):
        """Render options screen."""
        # Title
        title_text = "OPTIONS"
        title_surface = self.font_large.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surface, title_rect)
        
        # Sound status
        sound_text = f"Sound: {'ON' if sound_manager.sound_enabled else 'OFF'}"
        sound_surface = self.font_medium.render(sound_text, True, WHITE)
        sound_rect = sound_surface.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(sound_surface, sound_rect)
        
        # Music status
        music_text = f"Music: {'ON' if sound_manager.music_enabled else 'OFF'}"
        music_surface = self.font_medium.render(music_text, True, WHITE)
        music_rect = music_surface.get_rect(center=(SCREEN_WIDTH // 2, 350))
        screen.blit(music_surface, music_rect)
        
        # Render buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.options_buttons:
            button.update(mouse_pos, False)
            button.render(screen)
    
    def render_high_scores(self, screen: pygame.Surface, scores: List[dict]):
        """Render high scores screen."""
        # Title
        title_text = "HIGH SCORES"
        title_surface = self.font_large.render(title_text, True, GOLD)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # Display scores
        start_y = 200
        spacing = 40
        
        if not scores:
            no_scores_text = "No scores yet!"
            no_scores_surface = self.font_medium.render(no_scores_text, True, LIGHT_GRAY)
            no_scores_rect = no_scores_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y))
            screen.blit(no_scores_surface, no_scores_rect)
        else:
            for i, score_entry in enumerate(scores[:MAX_HIGH_SCORES]):
                rank = i + 1
                score = score_entry.get('score', 0)
                level = score_entry.get('level', 1)
                
                # Rank and score
                score_text = f"{rank}. {format_number(score)} (Level {level})"
                score_surface = self.font_medium.render(score_text, True, WHITE if rank == 1 else LIGHT_GRAY)
                score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * spacing))
                screen.blit(score_surface, score_rect)
                
                # Highlight first place
                if rank == 1:
                    pygame.draw.circle(screen, GOLD, (SCREEN_WIDTH // 2 - 250, start_y + i * spacing), 5)
        
        # Render buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.high_scores_buttons:
            button.update(mouse_pos, False)
            button.render(screen)

