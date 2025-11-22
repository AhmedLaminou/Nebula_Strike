# src/ui.py
import pygame
from settings import *


class UI:
    def __init__(self):

        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont(UI_FONT, UI_FONT_SIZE)

        # Bar Setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # Convert dictionary weapon data to graphics (placeholders)
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            # Logic to load actual image would go here
            surf = pygame.Surface((40, 40))
            surf.fill('gray')
            self.weapon_graphics.append(surf)

    def show_bar(self, current, max_amount, bg_rect, color):
        # Draw BG
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Converting stats to pixels
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Draw Bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        # Draw Border
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(f'EXP: {int(exp)}', False, TEXT_COLOR)
        x = self.display_surface.get_width() - 20
        y = self.display_surface.get_height() - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched)  # Bottom left

        # In real code, blit the self.weapon_graphics[weapon_index] here
        text_surf = self.font.render(list(weapon_data.keys())[weapon_index], False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(text_surf, text_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(80, 635, has_switched)  # Next to weapon

        text_surf = self.font.render(list(magic_data.keys())[magic_index], False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(text_surf, text_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
# HUD, Inventory, Menus
