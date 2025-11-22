# src/npc.py
import pygame
from settings import *
from src.entities.entity import Entity

class NPC(Entity):
    def __init__(self, pos, groups, obstacle_sprites, text_list):
        super().__init__(groups)
        self.sprite_type = 'npc'

        # Placeholder Graphic
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill('cyan')
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)

        self.obstacle_sprites = obstacle_sprites
        self.text_list = text_list
        self.status = 'idle'

    def update(self):
        # NPCs can wander here if we added movement logic
        pass
