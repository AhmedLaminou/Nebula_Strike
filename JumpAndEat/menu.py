import pygame
import math

class Menu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.options = ["Jouer", "Stats", "Paramètres", "Histoire", "Quitter"]
        self.selected = 0
        self.bg_color = (30, 30, 30)
        self.highlight_color = (255, 215, 0)
        self.anim_timer = 0
        self.music_played = False

    def draw(self):
        # Animation de fond simple (dégradé mouvant)
        for y in range(self.screen.get_height()):
            color = (30, 30 + int(20 * math.sin(y/30 + self.anim_timer/10)), 60)
            pygame.draw.line(self.screen, color, (0, y), (self.screen.get_width(), y))
        self.anim_timer += 1
        # Titre
        title = self.font.render("Ahmed Laminou Platformer", True, self.highlight_color)
        self.screen.blit(title, (self.screen.get_width()//2 - title.get_width()//2, 80))
        mx, my = pygame.mouse.get_pos()
        for i, option in enumerate(self.options):
            is_selected = (i == self.selected)
            # Effet de survol souris
            label = self.font.render(option, True, self.highlight_color if is_selected else (220, 220, 220))
            scale = 1.15 if is_selected else 1.0
            label = pygame.transform.smoothscale(label, (int(label.get_width()*scale), int(label.get_height()*scale)))
            x = self.screen.get_width()//2 - label.get_width()//2
            y = 200 + i*60
            self.screen.blit(label, (x, y))
            # Rectangle de surbrillance pour la souris
            rect = label.get_rect(topleft=(x, y))
            if rect.collidepoint(mx, my):
                pygame.draw.rect(self.screen, (255,255,255,40), rect, 2)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            for i, option in enumerate(self.options):
                label = self.font.render(option, True, (255,255,255))
                scale = 1.15 if i == self.selected else 1.0
                label = pygame.transform.smoothscale(label, (int(label.get_width()*scale), int(label.get_height()*scale)))
                x = self.screen.get_width()//2 - label.get_width()//2
                y = 200 + i*60
                rect = label.get_rect(topleft=(x, y))
                if rect.collidepoint(mx, my):
                    self.selected = i
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for i, option in enumerate(self.options):
                label = self.font.render(option, True, (255,255,255))
                scale = 1.15 if i == self.selected else 1.0
                label = pygame.transform.smoothscale(label, (int(label.get_width()*scale), int(label.get_height()*scale)))
                x = self.screen.get_width()//2 - label.get_width()//2
                y = 200 + i*60
                rect = label.get_rect(topleft=(x, y))
                if rect.collidepoint(mx, my):
                    return option
        return None
