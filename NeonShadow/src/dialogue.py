# src/dialogue.py
import pygame
from settings import *

class DialogueBox:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont(UI_FONT, UI_FONT_SIZE)

        self.height = 150
        self.width = WINDOW_WIDTH - 100
        self.left = 50
        self.top = WINDOW_HEIGHT - self.height - 20

        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.active = False
        self.text = []
        self.text_index = 0
        self.cooldown = 0

    def start_dialogue(self, text_list):
        self.active = True
        self.text = text_list
        self.text_index = 0

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and pygame.time.get_ticks() - self.cooldown > 300:
            self.cooldown = pygame.time.get_ticks()
            if self.text_index < len(self.text) - 1:
                self.text_index += 1
            else:
                self.active = False # Close dialogue

    def display(self):
        if self.active:
            self.input()

            # Draw Box
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.rect, 4)

            # Render Text
            current_text = self.text[self.text_index]
            text_surf = self.font.render(current_text, False, TEXT_COLOR)
            text_rect = text_surf.get_rect(topleft = (self.rect.x + 20, self.rect.y + 20))
            self.display_surface.blit(text_surf, text_rect)

            # Render 'Next' Indicator
            if self.text_index < len(self.text) - 1:
                next_surf = self.font.render("PRESS SPACE", False, 'gold')
                next_rect = next_surf.get_rect(bottomright = (self.rect.right - 20, self.rect.bottom - 20))
                self.display_surface.blit(next_surf, next_rect)
