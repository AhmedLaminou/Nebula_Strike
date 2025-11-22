import pygame

class SettingsScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.options = ["Volume: +", "Volume: -", "Retour"]
        self.selected = 0
        self.volume = 1.0

    def draw(self):
        self.screen.fill((40, 40, 40))
        title = self.font.render("Paramètres", True, (255, 215, 0))
        self.screen.blit(title, (self.screen.get_width()//2 - title.get_width()//2, 80))
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (180, 180, 180)
            label = self.font.render(option, True, color)
            self.screen.blit(label, (self.screen.get_width()//2 - label.get_width()//2, 200 + i*60))
        info = self.font.render(f"Volume actuel: {int(self.volume*100)}%", True, (180,180,180))
        self.screen.blit(info, (self.screen.get_width()//2 - info.get_width()//2, 450))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected == 0:
                    self.volume = min(1.0, self.volume + 0.1)
                    pygame.mixer.music.set_volume(self.volume)
                elif self.selected == 1:
                    self.volume = max(0.0, self.volume - 0.1)
                    pygame.mixer.music.set_volume(self.volume)
                elif self.selected == 2:
                    return True
        return False
