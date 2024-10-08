import pygame
import sys
from src.menus.menu import Menu
from src.game.game import Game
from assets.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

# Inicializa pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Centipede Game")

def main():
    clock = pygame.time.Clock()
    menu = Menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    game = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if menu.active:
            difficulty = menu.run()
            if not menu.active:  # Si el menú está inactivo, inicializa el juego
                game = Game(screen, difficulty)
        else:
            if game:  # Asegúrate de que el juego se haya inicializado
                game.run()  # Corre el juego
                if not game.active:  # Si el juego terminó, regresa al menú
                    game = None  # Reinicia el juego para que el menú se active de nuevo
                    menu.active = True  # Vuelve a activar el menú
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

