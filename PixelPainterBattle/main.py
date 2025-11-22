import pygame
from painter import PainterGame
import sys

if __name__ == "__main__":
    pygame.init()
    # Paramètres par défaut (à remplacer par lecture config Tkinter)
    grid_size = (20, 15)
    cell_size = 32
    player_colors = [(255, 80, 80), (80, 120, 255)]
    screen = pygame.display.set_mode((grid_size[0]*cell_size, grid_size[1]*cell_size))
    pygame.display.set_caption("Pixel Painter Battle")
    clock = pygame.time.Clock()
    game = PainterGame(screen, grid_size, cell_size, player_colors)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()
