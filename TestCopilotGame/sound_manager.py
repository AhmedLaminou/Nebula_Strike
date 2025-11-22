"""
TestCopilotGame - Sound Manager
Handles all audio including music and sound effects.
"""

import pygame
import os
from typing import Dict, Optional
from settings import *


class SoundManager:
    """Manages all game audio."""
    
    def __init__(self):
        """Initialize sound manager."""
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Audio state
        self.sound_enabled = SOUND_ENABLED
        self.music_enabled = MUSIC_ENABLED
        self.sfx_volume = SFX_VOLUME
        self.music_volume = MUSIC_VOLUME
        
        # Sound effects dictionary
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        
        # Music
        self.current_music: Optional[str] = None
        self.music_playing = False
        self.music_looping = False
        
        # Load sounds
        self.load_sounds()
    
    def load_sounds(self):
        """Load all sound effects."""
        # Sound file mapping
        sound_files = {
            'shoot': 'assets/sounds/shoot.wav',
            'hit': 'assets/sounds/hit.wav',
            'explosion': 'assets/sounds/explosion.wav',
            'player_hit': 'assets/sounds/player_hit.wav',
            'powerup': 'assets/sounds/powerup.wav',
            'boss_shoot': 'assets/sounds/boss_shoot.wav',
            'boss_defeat': 'assets/sounds/boss_defeat.wav',
            'game_over': 'assets/sounds/game_over.wav',
            'level_complete': 'assets/sounds/level_complete.wav',
        }
        
        # Try to load sounds, use placeholder if file not found
        for sound_name, file_path in sound_files.items():
            try:
                if os.path.exists(file_path):
                    sound = pygame.mixer.Sound(file_path)
                    sound.set_volume(self.sfx_volume)
                    self.sounds[sound_name] = sound
                else:
                    # Create placeholder sound
                    self.sounds[sound_name] = None
            except:
                self.sounds[sound_name] = None
    
    def load_music(self, music_name: str) -> Optional[str]:
        """Load music track."""
        music_files = {
            'menu': 'assets/music/menu.ogg',
            'gameplay': 'assets/music/gameplay.ogg',
            'boss': 'assets/music/boss.ogg',
            'game_over': 'assets/music/game_over.ogg',
        }
        
        return music_files.get(music_name)
    
    def play_sound(self, sound_name: str):
        """Play a sound effect."""
        if not self.sound_enabled:
            return
        
        sound = self.sounds.get(sound_name)
        if sound:
            try:
                sound.play()
            except:
                pass  # Ignore errors
    
    def play_music(self, music_name: str, loop: bool = False):
        """Play background music."""
        if not self.music_enabled:
            return
        
        music_file = self.load_music(music_name)
        if music_file:
            try:
                if os.path.exists(music_file):
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.set_volume(self.music_volume)
                    loops = -1 if loop else 0
                    pygame.mixer.music.play(loops)
                    self.current_music = music_name
                    self.music_playing = True
                    self.music_looping = loop
            except:
                pass  # Ignore errors
    
    def stop_music(self):
        """Stop background music."""
        pygame.mixer.music.stop()
        self.current_music = None
        self.music_playing = False
    
    def pause_music(self):
        """Pause background music."""
        if self.music_playing:
            pygame.mixer.music.pause()
    
    def resume_music(self):
        """Resume background music."""
        if self.music_playing:
            pygame.mixer.music.unpause()
    
    def toggle_sound(self):
        """Toggle sound effects on/off."""
        self.sound_enabled = not self.sound_enabled
    
    def toggle_music(self):
        """Toggle music on/off."""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_music()
        elif self.current_music and not self.music_playing:
            self.play_music(self.current_music, self.music_looping)
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        
        # Update all sounds
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.sfx_volume)
    
    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def get_sound_enabled(self) -> bool:
        """Get sound enabled state."""
        return self.sound_enabled
    
    def get_music_enabled(self) -> bool:
        """Get music enabled state."""
        return self.music_enabled

