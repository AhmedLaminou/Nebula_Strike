# src/entities/enemy.py
import pygame
from settings import *
from src.entities.entity import Entity
from src.support import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):

        # General Setup
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.obstacle_sprites = obstacle_sprites

        # Graphics Setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

        # Stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # Player Interaction
        self.can_attack = True
        self.attack_time = 0
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        # Invincibility Timer
        self.vulnerable = True
        self.hit_time = 0
        self.invincibility_duration = 300

        # Sounds (Placeholders to prevent crash)
        self.death_sound = pygame.mixer.Sound
        self.hit_sound = pygame.mixer.Sound
        self.attack_sound = pygame.mixer.Sound

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        path = f'../data/graphics/monsters/{name}/'

        # Fallback if files missing: Generate colored rects based on state
        try:
            for animation in self.animations.keys():
                self.animations[animation] = import_folder(path + animation)
        except:
            pass

        # Check if animations are empty and generate fallback
        if not self.animations['idle']:
            # Procedural Generation of "Dummy" Assets
            c = 'red' if name == 'squid' else 'blue'
            for animation in self.animations.keys():
                surf = pygame.Surface((64, 64))
                surf.fill(c)
                if animation == 'attack': surf.fill('white')
                self.animations[animation] = [surf]

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()  # Inherited from Entity
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            # self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]

            if attack_type == 'weapon':
                self.health -= player.stats['attack']  # Use weapon damage logic here
            else:
                self.health -= player.stats['magic']  # Magic damage logic

            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)
            # self.death_sound.play()
            self.kill()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
# AI Logic
