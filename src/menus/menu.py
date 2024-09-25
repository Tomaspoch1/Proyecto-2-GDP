import pygame
from src.utils.utils import draw_text

class Menu:
    def __init__(self, screen, screen_width, screen_height, difficulty=["Normal", 10]):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont(None, 55)
        self.difficulty_font = pygame.font.SysFont(None, 30)
        self.active = True  # Indica si el menú está activo
        self.difficulty = difficulty  # Agrega el atributo de dificultad

    def run(self):
        self.screen.fill((0, 0, 0))
        draw_text('Centipede Game', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 4)
        
        # Dibuja la dificultad en la esquina superior derecha
        difficulty_text = f"Dificultad: {self.difficulty[0]}"
        draw_text(difficulty_text, self.difficulty_font, (255, 255, 255), self.screen, self.screen_width - 150, 30)

        draw_text('1. Jugar', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 - 50)
        draw_text('2. Dificultad', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2)
        draw_text('3. Instrucciones', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 + 50)
        draw_text('4. Salir', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 + 100)

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_1]:
            self.active = False  # Cambia a la pantalla de juego
            return self.difficulty[1]
        elif keys[pygame.K_2]:
            self.start_difficulty_menu()
        elif keys[pygame.K_3]:
            self.show_instructions()
        elif keys[pygame.K_4]:
            pygame.quit()
            exit()

        pygame.display.flip()

    def start_difficulty_menu(self):
        from src.menus.difficulty import DifficultyMenu
        difficulty_menu = DifficultyMenu(self.screen, self.screen_width, self.screen_height)  # Crea una instancia de DifficultyMenu
        difficulty_option = difficulty_menu.run()  # Ejecuta el menú de dificultad
        print(difficulty_option)
        self.difficulty = difficulty_option

    def show_instructions(self):
        self.screen.fill((0, 0, 0))
        draw_text('Instrucciones del juego', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 4)
        draw_text('Usa las flechas para mover el jugador', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2)
        draw_text('Presiona espacio para disparar', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 + 50)
        draw_text('Presiona ESC para volver al menú', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 + 100)
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            self.active = True  # Regresa al menú principal
