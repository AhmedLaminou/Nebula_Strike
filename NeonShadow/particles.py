# src/particles.py
import pygame
from src.support import import_folder
from random import choice, randint


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # Magic
            'flame': import_folder('../data/graphics/particles/flame/frames'),
            'aura': import_folder('../data/graphics/particles/aura'),
            'heal': import_folder('../data/graphics/particles/heal/frames'),

            # Attacks
            'claw': import_folder('../data/graphics/particles/claw'),
            'slash': import_folder('../data/graphics/particles/slash'),
            'sparkle': import_folder('../data/graphics/particles/sparkle'),
            'leaf_attack': import_folder('../data/graphics/particles/leaf_attack'),
            'thunder': import_folder('../data/graphics/particles/thunder'),

            # Monster Deaths
            'squid': import_folder('../data/graphics/particles/smoke_orange'),
            'raccoon': import_folder('../data/graphics/particles/raccoon'),
            'spirit': import_folder('../data/graphics/particles/nova'),
            'bamboo': import_folder('../data/graphics/particles/bamboo'),

            # Environmental (Leaves)
            'leaf': (
                import_folder('../data/graphics/particles/leaf1'),
                import_folder('../data/graphics/particles/leaf2'),
                import_folder('../data/graphics/particles/leaf3'),
                import_folder('../data/graphics/particles/leaf4'),
                import_folder('../data/graphics/particles/leaf5'),
                import_folder('../data/graphics/particles/leaf6'),
                self.reflect_images(import_folder('../data/graphics/particles/leaf1')),
                self.reflect_images(import_folder('../data/graphics/particles/leaf2')),
                self.reflect_images(import_folder('../data/graphics/particles/leaf3')),
                self.reflect_images(import_folder('../data/graphics/particles/leaf4')),
                self.reflect_images(import_folder('../data/graphics/particles/leaf5')),
                self.reflect_images(import_folder('../data/graphics/particles/leaf6'))
            )
        }

        # Failsafe for missing assets (generates colored squares)
        if not self.frames['flame']:
            self.generate_placeholders()

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def generate_placeholders(self):
        # Creates a dummy 4-frame animation for every missing key
        for key in self.frames.keys():
            if not self.frames[key]:
                dummy_list = []
                for i in range(4):
                    surf = pygame.Surface((20, 20))
                    surf.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
                    dummy_list.append(surf)
                self.frames[key] = dummy_list

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()  # Destroys itself after one loop
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()