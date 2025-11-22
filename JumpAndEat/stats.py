import pygame
from another import ScoreManager

class StatsScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.score_manager = ScoreManager()

    def draw(self):
        self.screen.fill((20, 20, 40))
        title = self.font.render("Statistiques", True, (255, 215, 0))
        self.screen.blit(title, (self.screen.get_width()//2 - title.get_width()//2, 80))
        scores = self.score_manager.get_scores()
        for i, score in enumerate(scores):
            label = self.font.render(f"{i+1}. Score : {score}", True, (255,255,255))
            self.screen.blit(label, (self.screen.get_width()//2 - label.get_width()//2, 180 + i*40))
        info = self.font.render("Appuie sur ECHAP pour revenir", True, (180,180,180))
        self.screen.blit(info, (self.screen.get_width()//2 - info.get_width()//2, 500))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
        return False
