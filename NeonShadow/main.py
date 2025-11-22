# main.py
import pygame, sys
from settings import *
from src.level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Neon Shadow: The Protocol')
        self.clock = pygame.time.Clock()
        self.level = Level()

        # Audio Placeholder
        # main_sound = pygame.mixer.Sound('../data/audio/main.ogg')
        # main_sound.play(loops = -1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()  # <--- Toggle Upgrade Menu

            self.screen.fill('black')  # Fill background
            self.level.run()  # Update Level
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
# Entry Point
