import pygame
import random

class PainterGame:
    def __init__(self, screen, grid_size, cell_size, player_colors):
        self.screen = screen
        self.grid_w, self.grid_h = grid_size
        self.cell_size = cell_size
        self.player_colors = player_colors
        self.grid = [[None for _ in range(self.grid_h)] for _ in range(self.grid_w)]
        self.players = [
            {'pos': [0, 0], 'color': player_colors[0], 'score': 0},
            {'pos': [self.grid_w-1, self.grid_h-1], 'color': player_colors[1], 'score': 0}
        ]
        self.turn = 0
        self.bonus = None
        self.bonus_timer = 0
        self.game_time = 60 * 30  # 30 secondes à 60 FPS
        self.font = pygame.font.SysFont('arial', 24)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.turn == 0:
            if event.key == pygame.K_UP:
                self.players[0]['pos'][1] = max(0, self.players[0]['pos'][1]-1)
            elif event.key == pygame.K_DOWN:
                self.players[0]['pos'][1] = min(self.grid_h-1, self.players[0]['pos'][1]+1)
            elif event.key == pygame.K_LEFT:
                self.players[0]['pos'][0] = max(0, self.players[0]['pos'][0]-1)
            elif event.key == pygame.K_RIGHT:
                self.players[0]['pos'][0] = min(self.grid_w-1, self.players[0]['pos'][0]+1)
            elif event.key == pygame.K_SPACE:
                self.paint(0)
                self.turn = 1
        if event.type == pygame.MOUSEBUTTONDOWN and self.turn == 1:
            mx, my = pygame.mouse.get_pos()
            gx, gy = mx // self.cell_size, my // self.cell_size
            self.players[1]['pos'] = [gx, gy]
            self.paint(1)
            self.turn = 0

    def paint(self, player_idx):
        x, y = self.players[player_idx]['pos']
        if self.grid[x][y] != self.player_colors[player_idx]:
            self.grid[x][y] = self.player_colors[player_idx]
            self.players[player_idx]['score'] += 1

    def update(self):
        self.game_time -= 1
        if self.game_time <= 0:
            self.end_game()
        # Bonus aléatoire (exemple)
        if self.bonus is None and random.random() < 0.005:
            self.bonus = (random.randint(0, self.grid_w-1), random.randint(0, self.grid_h-1))
            self.bonus_timer = 180
        if self.bonus:
            self.bonus_timer -= 1
            if self.bonus_timer <= 0:
                self.bonus = None

    def draw(self):
        for x in range(self.grid_w):
            for y in range(self.grid_h):
                color = self.grid[x][y] if self.grid[x][y] else (220,220,220)
                pygame.draw.rect(self.screen, color, (x*self.cell_size, y*self.cell_size, self.cell_size-1, self.cell_size-1))
        # Joueurs
        for idx, p in enumerate(self.players):
            pygame.draw.rect(self.screen, p['color'], (p['pos'][0]*self.cell_size, p['pos'][1]*self.cell_size, self.cell_size, self.cell_size), 3)
        # Bonus
        if self.bonus:
            bx, by = self.bonus
            pygame.draw.circle(self.screen, (255,255,0), (bx*self.cell_size+self.cell_size//2, by*self.cell_size+self.cell_size//2), self.cell_size//3)
        # Scores
        s1 = self.font.render(f"J1: {self.players[0]['score']}", True, self.player_colors[0])
        s2 = self.font.render(f"J2: {self.players[1]['score']}", True, self.player_colors[1])
        self.screen.blit(s1, (10, 10))
        self.screen.blit(s2, (self.screen.get_width()-s2.get_width()-10, 10))
        # Timer
        timer = self.font.render(f"Temps: {self.game_time//60}", True, (0,0,0))
        self.screen.blit(timer, (self.screen.get_width()//2-timer.get_width()//2, 10))

    def end_game(self):
        # Affichage du gagnant (à améliorer)
        winner = 0 if self.players[0]['score'] > self.players[1]['score'] else 1
        msg = self.font.render(f"Joueur {winner+1} gagne !", True, (0,200,0))
        self.screen.blit(msg, (self.screen.get_width()//2-msg.get_width()//2, self.screen.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.event.post(pygame.event.Event(pygame.QUIT))
