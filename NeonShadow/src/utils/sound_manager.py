# src/utils/sound_manager.py
import pygame

class SoundManager:
    def __init__(self):
        self.volume = 0.5
        self.bg_music_path = '../data/audio/main.ogg'
        self.sounds = {}
        self.load_assets()

    def load_assets(self):
        # In a real 5k line project, this would scan directories
        # Here we setup safu-guards for missing files
        try:
            pygame.mixer.music.load(self.bg_music_path)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(loops=-1)
        except:
            print("Info: Background music not found.")

        sound_names = ['slash', 'fireball', 'heal', 'upgrade', 'death']
        for name in sound_names:
            try:
                self.sounds[name] = pygame.mixer.Sound(f'../data/audio/{name}.wav')
                self.sounds[name].set_volume(self.volume)
            except:
                # Create a dummy empty sound object if file is missing
                # This prevents the game from crashing
                self.sounds[name] = DummySound()

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()

class DummySound:
    def play(self):
        pass
    def set_volume(self, v):
        pass
