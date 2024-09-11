import pygame
from utils import draw_text

class Menu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont(None, 55)
        self.active = True  # Indica si el menú está activo

    
    def run(self):
        self.screen.fill((0, 0, 0))
        draw_text('Centipede Game', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 4)
        draw_text('1. Jugar', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 - 50)
        draw_text('2. Instrucciones', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2)
        draw_text('3. Salir', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 + 50)
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_1]:
            self.active = False  # Cambia a la pantalla de juego
        elif keys[pygame.K_2]:
            self.show_instructions()
        elif keys[pygame.K_3]:
            pygame.quit()
            exit()

    def show_instructions(self):
        self.screen.fill((0, 0, 0))
        draw_text('Instrucciones del juego', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 4)
        draw_text('Usa las flechas para mover el jugador', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2)
        draw_text('Presiona espacio para disparar', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 + 50)
        self.draw_text('Presiona ESC para volver al menú', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 + 100)
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            self.active = True  # Regresa al menú principal
