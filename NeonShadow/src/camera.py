# src/camera.py
import pygame
from settings import *


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Creating the floor (Map Backround)
        # In production, load a giant map image here
        self.floor_surf = pygame.Surface((4000, 4000))
        self.floor_surf.fill('#1a1a1a')  # Dark grey floor
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # Calculate Offset based on player position
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Draw Floor first
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # Sort sprites by centerY (Y-Sort algorithm)
        # This ensures sprites 'lower' on screen appear 'in front' of higher ones
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

            # Optional: Draw rectangles for debugging if needed
            # pygame.draw.rect(self.display_surface, 'red', offset_pos, 1)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
# Complex Camera Logic
