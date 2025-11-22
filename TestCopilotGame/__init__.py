"""
TestCopilotGame - Space Shooter Game
A comprehensive Pygame-based space shooter game.

This package contains all game modules and can be imported as a Python package.
"""

__version__ = "1.0.0"
__author__ = "TestCopilotGame Team"
__description__ = "A comprehensive space shooter game built with Pygame"

# Import main game classes for easy access
try:
    from .main import Game, GameState, main
    from .player import Player
    from .enemies import Enemy, EnemyManager
    from .bullets import Bullet, BulletManager, PlayerBullet, EnemyBullet, BossBullet
    from .powerups import PowerUp, PowerUpManager
    from .particles import Particle, ParticleManager
    from .background import BackgroundManager, Star, Nebula
    from .bosses import Boss, BossManager
    from .ui import UIManager, Button
    from .level import LevelManager
    from .sound_manager import SoundManager
    from .save_system import SaveSystem
    from .settings import *
    from .utils import *
except ImportError:
    # If imports fail, modules will be imported individually
    pass

__all__ = [
    'Game',
    'GameState',
    'main',
    'Player',
    'Enemy',
    'EnemyManager',
    'Bullet',
    'BulletManager',
    'PowerUp',
    'PowerUpManager',
    'Particle',
    'ParticleManager',
    'BackgroundManager',
    'Boss',
    'BossManager',
    'UIManager',
    'LevelManager',
    'SoundManager',
    'SaveSystem',
]

