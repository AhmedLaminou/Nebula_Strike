# Nebula Strike - Space Shooter

A comprehensive space shooter game built with Pygame featuring multiple enemy types, power-ups, boss battles, particle effects, and more.

## Features

- **Multiple Enemy Types**: Basic, Fast, Tank, Shooter, Kamikaze, Swarm, and Elite enemies
- **Boss Battles**: Epic boss fights with special attack patterns
- **Power-Up System**: Health, Speed, Damage, Shield, Rapid Fire, and Multi-Shot power-ups
- **Particle Effects**: Explosions, trails, sparks, and visual effects
- **Level Progression**: Increasing difficulty with multiple levels
- **Score System**: High score tracking and persistence
- **UI System**: Main menu, pause screen, game over screen, options, and high scores
- **Sound System**: Background music and sound effects (requires audio files)
- **Parallax Background**: Scrolling starfield with multiple layers

## Installation

1. Install Python 3.8 or higher
2. Create and activate virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install directly:
   ```bash
   pip install pygame
   ```

## Running the Game

```bash
python main.py
```

## Controls

- **WASD / Arrow Keys**: Move player ship
- **Space / Left Mouse**: Shoot
- **ESC**: Pause game / Return to menu
- **ENTER**: Start game / Continue after game over
- **H**: View high scores (from menu)
- **O**: View options (from menu)
- **Shift**: Activate special ability (if available)

## Game Structure

### Core Files
- `main.py` - Main game loop and state management
- `settings.py` - All game constants and configuration
- `utils.py` - Utility functions and helper classes

### Game Systems
- `player.py` - Player ship with movement, shooting, and upgrades
- `enemies.py` - Enemy types and AI behaviors
- `bullets.py` - Bullet system for all entities
- `bosses.py` - Boss battles and special attacks
- `powerups.py` - Power-up system and effects
- `particles.py` - Particle effects and animations
- `background.py` - Scrolling starfield and parallax layers

### Game Management
- `level.py` - Level progression and spawning logic
- `ui.py` - User interface and menu system
- `sound_manager.py` - Audio management
- `save_system.py` - High score persistence

## Assets

The game includes placeholder graphics and will run without external assets. However, you can add:

### Images
Place images in `assets/images/`:
- Player and enemy sprites
- Boss sprites
- Power-up icons
- UI elements

### Sounds
Place sound effects in `assets/sounds/`:
- `shoot.wav`, `hit.wav`, `explosion.wav`, etc.

### Music
Place music tracks in `assets/music/`:
- `menu.ogg`, `gameplay.ogg`, `boss.ogg`, `game_over.ogg`

See `assets/README.md` for more details.

## Gameplay

1. **Start**: Press ENTER or click "Start Game" from the main menu
2. **Survive**: Destroy enemies while avoiding their attacks
3. **Collect Power-ups**: Grab power-ups to enhance your abilities
4. **Defeat Bosses**: Face powerful bosses every few levels
5. **Progress**: Advance through increasingly difficult levels
6. **Score**: Achieve the highest score possible!

## Code Statistics

This project contains over 5000 lines of code across multiple modules:
- Main game loop and state management
- Multiple enemy types with AI
- Complex bullet system
- Boss battles with attack patterns
- Particle effects system
- UI and menu system
- Sound and save systems

## Requirements

- Python 3.8+
- Pygame 2.1.0+

## License

This project is created as a demonstration game for learning Pygame development.

## Author

Created as Nebula Strike - A comprehensive Pygame space shooter project.

