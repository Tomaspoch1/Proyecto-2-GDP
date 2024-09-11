import pygame
import sys
from menu import Menu
from game import Game
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

# Inicializa pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Centipede Game")

def main():
    clock = pygame.time.Clock()
    menu = Menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    game = Game(screen)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Si el menú está activo
        if menu.active:
            menu.run()
            if not menu.active:  # Si el menú está inactivo, inicializa el juego
                game = Game(screen)
        else:
            if game:  # Asegúrate de que el juego se haya inicializado
                game.run()
            else:
                menu.active = True  # Regresa al menú si el juego no está inicializado
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
