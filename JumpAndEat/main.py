import pygame
import random
import os
from entities import PLATFORM_WIDTH, PLATFORM_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, Platform, Coin, Enemy
from other import Level
from another import ScoreManager
from menu import Menu
from stats import StatsScreen
from settings import SettingsScreen
from story import StoryScreen

# Initialisation de Pygame
pygame.init()

# Constantes
FPS = 60
GRAVITY = 0.5
PLAYER_SPEED = 5
JUMP_POWER = 12

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ahmed Laminou Platformer")
clock = pygame.time.Clock()

# Initialisation du mixer pour le son
pygame.mixer.init()

# Sons
JUMP_SOUND = pygame.mixer.Sound(os.path.join("assets", "jump.wav"))
COIN_SOUND = pygame.mixer.Sound(os.path.join("assets", "coin.wav"))
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join("assets", "gameover.wav"))
ENEMY_HIT_SOUND = pygame.mixer.Sound(os.path.join("assets", "hit.mp3"))

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.vel_y = 0
        self.on_ground = False
        self.score = 0
        self.lives = 3

    def update(self, platforms, coins, enemies):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED
        self.rect.x += dx

        # Gravité
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Collision plateformes
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

        # Collision pièces
        for coin in coins:
            if self.rect.colliderect(coin.rect):
                coin.kill()
                self.score += 10

        # Collision ennemis
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.lives -= 1
                self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
                if self.lives <= 0:
                    self.kill()

        # Limites écran
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top > SCREEN_HEIGHT:
            self.lives -= 1
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
            if self.lives <= 0:
                self.kill()

    def jump(self, platforms):
        self.rect.y += 2
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.vel_y = -JUMP_POWER
        self.rect.y -= 2

# Boucle principale
BUTTON_FONT = pygame.font.SysFont(None, 40)
MENU_FONT = pygame.font.SysFont(None, 48)

def draw_button(surface, text, x, y, w, h, color, text_color):
    pygame.draw.rect(surface, color, (x, y, w, h))
    label = BUTTON_FONT.render(text, True, text_color)
    surface.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return pygame.Rect(x, y, w, h)

def draw_hud(surface, player):
    font = pygame.font.SysFont(None, 32)
    score_text = font.render(f"Score: {player.score}", True, BLACK)
    lives_text = font.render(f"Lives: {player.lives}", True, BLACK)
    surface.blit(score_text, (10, 10))
    surface.blit(lives_text, (10, 40))

def main():
    running = True
    state = "menu"  # menu, game, stats, settings, story, pause
    level_num = 1
    score_manager = ScoreManager()
    menu = Menu(screen, MENU_FONT)
    stats_screen = StatsScreen(screen, MENU_FONT)
    settings_screen = SettingsScreen(screen, MENU_FONT)
    story_screen = StoryScreen(screen, MENU_FONT)
    while running:
        if state == "menu":
            menu.draw()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                result = menu.handle_event(event)
                if result == "Jouer":
                    state = "game"
                elif result == "Stats":
                    state = "stats"
                elif result == "Paramètres":
                    state = "settings"
                elif result == "Histoire":
                    state = "story"
                elif result == "Quitter":
                    running = False
        elif state == "stats":
            stats_screen.draw()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if stats_screen.handle_event(event):
                    state = "menu"
        elif state == "settings":
            settings_screen.draw()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if settings_screen.handle_event(event):
                    state = "menu"
        elif state == "story":
            story_screen.draw()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if story_screen.handle_event(event):
                    state = "menu"
        elif state == "game":
            # Gestion des niveaux
            level = Level(level_num)
            platforms, coins, enemies = level.generate()
            player = Player()
            player_group = pygame.sprite.Group(player)
            game_over = False
            paused = False
            while state == "game":
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        state = "menu"
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and player.on_ground:
                            player.jump(platforms)
                            JUMP_SOUND.play()
                        if event.key == pygame.K_p:
                            paused = not paused
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        if restart_btn.collidepoint(mx, my):
                            game_over = True
                            state = "game"
                            level_num = 1
                        if quit_btn.collidepoint(mx, my):
                            running = False
                            state = "menu"
                if paused:
                    draw_button(screen, "Continuer", 350, 250, 120, 50, GREEN, WHITE)
                    pygame.display.flip()
                    continue
                # Update
                player_group.update(platforms, coins, enemies)
                enemies.update()

                # Dessin
                screen.fill(WHITE)
                platforms.draw(screen)
                coins.draw(screen)
                enemies.draw(screen)
                player_group.draw(screen)
                draw_hud(screen, player)
                # Boutons
                restart_btn = draw_button(screen, "Recommencer", 300, 500, 150, 50, BLUE, WHITE)
                quit_btn = draw_button(screen, "Quitter", 500, 500, 120, 50, RED, WHITE)
                if not player.alive():
                    GAME_OVER_SOUND.play()
                    font = pygame.font.SysFont(None, 64)
                    text = font.render("Game Over!", True, RED)
                    screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 32))
                    score_manager.add_score(player.score)
                    draw_button(screen, "Rejouer", 325, 350, 150, 50, GREEN, WHITE)
                    draw_button(screen, "Quitter", 500, 350, 120, 50, RED, WHITE)
                    pygame.display.flip()
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                waiting = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mx, my = pygame.mouse.get_pos()
                                if 325 <= mx <= 475 and 350 <= my <= 400:
                                    waiting = False
                                    level_num = 1
                                if 500 <= mx <= 620 and 350 <= my <= 400:
                                    running = False
                                    waiting = False
                # Passage au niveau suivant
                if len(coins) == 0:
                    level_num += 1
                    break
                pygame.display.flip()
        else:
            running = False
    pygame.quit()

if __name__ == "__main__":
    main()
