import pygame
import random

PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w=PLATFORM_WIDTH, h=PLATFORM_HEIGHT):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
