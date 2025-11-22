# src/level.py (UPDATED)
import pygame
from settings import *
from src.entities.player import Player
from src.entities.enemy import Enemy  # <-- New Import
from src.items.magic import MagicPlayer  # <-- New Import
from particles import AnimationPlayer  # <-- Import from root level
from src.camera import YSortCameraGroup
from src.ui import UI
from src.upgrade import Upgrade  # <-- New Import for Phase 3
from src.inventory import Inventory  # <-- New Import for Phase 4
from src.data.world_map import WORLD_MAP  # <-- New Import for Phase 5
from src.npc import NPC  # <-- New Import for Phase 5
from src.dialogue import DialogueBox  # <-- New Import for Phase 5
from random import randint, choice


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # Sprite Group Setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Systems
        self.ui = UI()
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
        self.dialogue_box = DialogueBox()  # <--- New UI System (Phase 5)

        self.create_map()

        # --- NEW CODE START (Phase 3 & 4 & 5) ---
        # Game States: 'playing', 'upgrade', 'inventory'
        self.game_state = 'playing'

        self.upgrade = Upgrade(self.player)
        self.inventory = Inventory(self.player)  # <--- Instantiate Inventory (Phase 4)
        # --- NEW CODE END ---

    def create_map(self):
        # Parse the WORLD_MAP list (Phase 5)
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'rock')

                elif col == 'p':
                    self.player = Player(
                        (x, y),
                        [self.visible_sprites],
                        self.obstacle_sprites,
                        self.create_attack,
                        self.destroy_attack,
                        self.create_magic
                    )

                elif col == 's':
                    Enemy('squid', (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_player, self.trigger_death_particles, self.add_exp)

                elif col == 'r':
                    Enemy('raccoon', (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_player, self.trigger_death_particles, self.add_exp)

                elif col == 'n':
                    NPC((x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites,
                        ["Welcome to the Neon Dungeon.", "Be careful, the squids are aggressive.", "Press 'Q' to switch weapons."])

    # --- Magic & Attack Methods ---
    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

        # if style == 'ice': ... (Add future spells here)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    # --- Player Interaction Methods ---
    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])

    def add_exp(self, amount):
        self.player.exp += amount

    # --- Game Loop ---
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                # Check collision with all attackable sprites (Enemies)
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if hasattr(target_sprite, 'sprite_type') and target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def toggle_menu(self):
        # Cycle states: Playing -> Upgrade -> Inventory -> Playing
        if self.game_state == 'playing':
            self.game_state = 'upgrade'
        elif self.game_state == 'upgrade':
            self.game_state = 'inventory'
        else:
            self.game_state = 'playing'

    def check_npc_interaction(self):
        # Simple interaction logic: If close and press Space (Phase 5)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.player.attacking:
            collided_interaction_sprite = pygame.sprite.spritecollide(self.player, self.attackable_sprites, False)
            if collided_interaction_sprite:
                for sprite in collided_interaction_sprite:
                    if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'npc':
                        self.dialogue_box.start_dialogue(sprite.text_list)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        self.dialogue_box.display()  # Always try to display if active (Phase 5)

        # State Machine
        if self.game_state == 'playing':
            if self.dialogue_box.active:
                # Freeze game while talking
                pass
            else:
                self.visible_sprites.update()
                self.visible_sprites.enemy_update(self.player)
                self.player_attack_logic()
                self.check_npc_interaction()

        elif self.game_state == 'upgrade':
            self.upgrade.display()

        elif self.game_state == 'inventory':
            self.inventory.update()


# Helper classes re-declared here to ensure the file runs standalone
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.image.fill('brown')  # Rock color
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]

        self.image = pygame.Surface((40, 40))
        self.image.fill('white')

        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))