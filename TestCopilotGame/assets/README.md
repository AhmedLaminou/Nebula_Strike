# Assets Folder

This folder contains all game assets including images, sounds, and music.

## Structure

- `images/` - All image files (sprites, backgrounds, UI elements)
- `sounds/` - Sound effects (WAV format recommended)
- `music/` - Background music (OGG format recommended)

## Required Assets

### Images
The game will work without images (using colored shapes), but you can add:
- Player ship sprite
- Enemy sprites
- Boss sprites
- Power-up icons
- Background images
- UI elements

### Sounds
- `shoot.wav` - Player shooting sound
- `hit.wav` - Bullet hit sound
- `explosion.wav` - Explosion sound
- `player_hit.wav` - Player taking damage
- `powerup.wav` - Power-up collected
- `boss_shoot.wav` - Boss shooting
- `boss_defeat.wav` - Boss defeated
- `game_over.wav` - Game over sound
- `level_complete.wav` - Level complete sound

### Music
- `menu.ogg` - Main menu music
- `gameplay.ogg` - Gameplay music
- `boss.ogg` - Boss battle music
- `game_over.ogg` - Game over music

## Notes

- If assets are missing, the game will still run using placeholder graphics and silent sounds
- Supported image formats: PNG, JPG
- Supported audio formats: WAV, OGG
- All paths are relative to the TestCopilotGame folder

