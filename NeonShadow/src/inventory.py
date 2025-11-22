# src/inventory.py
import pygame
from settings import *

class Inventory:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont(UI_FONT, UI_FONT_SIZE)

        # Grid Dimensions
        self.cols = INVENTORY_WIDTH
        self.rows = INVENTORY_HEIGHT

        # Calculate total size to center it
        self.total_width = (self.cols * (SLOT_SIZE + SLOT_PADDING)) - SLOT_PADDING
        self.total_height = (self.rows * (SLOT_SIZE + SLOT_PADDING)) - SLOT_PADDING

        self.start_x = (WINDOW_WIDTH - self.total_width) // 2
        self.start_y = (WINDOW_HEIGHT - self.total_height) // 2

        # Selection
        self.selection_index = [0, 0] # [col, row]
        self.can_move = True
        self.move_timer = 0
        self.move_cooldown = 200

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            # Horizontal Movement
            if keys[pygame.K_RIGHT] and self.selection_index[0] < self.cols - 1:
                self.selection_index[0] += 1
                self.can_move = False
                self.move_timer = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index[0] > 0:
                self.selection_index[0] -= 1
                self.can_move = False
                self.move_timer = pygame.time.get_ticks()

            # Vertical Movement
            if keys[pygame.K_DOWN] and self.selection_index[1] < self.rows - 1:
                self.selection_index[1] += 1
                self.can_move = False
                self.move_timer = pygame.time.get_ticks()
            elif keys[pygame.K_UP] and self.selection_index[1] > 0:
                self.selection_index[1] -= 1
                self.can_move = False
                self.move_timer = pygame.time.get_ticks()

            # Activate Item
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.move_timer = pygame.time.get_ticks()
                self.activate_item()

    def cooldowns(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.move_timer >= self.move_cooldown:
                self.can_move = True

    def activate_item(self):
        # Calculate linear index from 2D grid
        col = self.selection_index[0]
        row = self.selection_index[1]

        # Logic to use item would go here
        # For now, we print debug info
        print(f"Selected Slot: {col}, {row}")

        # Example: Equip Weapon if valid
        # current_item = self.player.inventory_slots[row][col]
        # if current_item: self.player.equip(current_item)

    def draw_window(self):
        # Draw a dark overlay behind the inventory
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill('black')
        overlay.set_alpha(200) # Semi-transparent
        self.display_surface.blit(overlay, (0,0))

        # Draw the Grid
        for row in range(self.rows):
            for col in range(self.cols):
                # Calculate pixel position
                x = self.start_x + (col * (SLOT_SIZE + SLOT_PADDING))
                y = self.start_y + (row * (SLOT_SIZE + SLOT_PADDING))

                rect = pygame.Rect(x, y, SLOT_SIZE, SLOT_SIZE)

                # Draw Slot Background
                pygame.draw.rect(self.display_surface, SLOT_BG_COLOR, rect)

                # Draw Selection Highlight
                if col == self.selection_index[0] and row == self.selection_index[1]:
                    pygame.draw.rect(self.display_surface, SLOT_SELECTED_COLOR, rect, 3)
                    self.draw_tooltip(x, y, col, row)
                else:
                    pygame.draw.rect(self.display_surface, SLOT_BORDER_COLOR, rect, 1)

                # Draw Item Icon (Mockup)
                # In real code: if self.player.inventory[row][col]: blit image
                pass

    def draw_tooltip(self, x, y, col, row):
        # Draws a description box next to the selected item
        text_surf = self.font.render(f"Slot [{col},{row}] - Empty", False, TEXT_COLOR)

        # Position tooltip to the right of the grid
        tooltip_rect = pygame.Rect(
            self.start_x + self.total_width + 20,
            self.start_y,
            200,
            100
        )

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, tooltip_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, tooltip_rect, 2)

        # Center Text
        text_rect = text_surf.get_rect(topleft = (tooltip_rect.left + 10, tooltip_rect.top + 10))
        self.display_surface.blit(text_surf, text_rect)

    def update(self):
        self.input()
        self.cooldowns()
        self.draw_window()
