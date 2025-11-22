import pygame
import random
from entities import PLATFORM_WIDTH, PLATFORM_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, Platform, Coin, Enemy

class Level:
    def __init__(self, number):
        self.number = number
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

    def generate(self):
        # Génération de plateformes
        for i in range(8 + self.number):
            x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
            y = 100 + i * 50 - self.number * 2
            self.platforms.add(Platform(x, y))
        # Sol
        self.platforms.add(Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20))
        # Génération de pièces
        for i in range(10 + self.number * 2):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 100)
            self.coins.add(Coin(x, y))
        # Génération d'ennemis
        for i in range(4 + self.number):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 200)
            self.enemies.add(Enemy(x, y))
        return self.platforms, self.coins, self.enemies
