import pygame

class StoryScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.story = [
            "Bienvenue dans l'aventure d'Ahmed Laminou!",
            "Vous incarnez un héros qui doit traverser des plateformes,",
            "ramasser des pièces et éviter de dangereux ennemis.",
            "Chaque niveau devient plus difficile...",
            "Bonne chance!",
            "Appuie sur ECHAP pour revenir au menu."
        ]

    def draw(self):
        self.screen.fill((10, 10, 30))
        for i, line in enumerate(self.story):
            label = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(label, (self.screen.get_width()//2 - label.get_width()//2, 120 + i*50))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
        return False
