import pygame
from src.utils.utils import draw_text

class Menu:
    def __init__(self, screen, screen_width, screen_height, difficulty=["Normal", 10]):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont(None, 30)  # Tamaño de fuente más pequeño
        self.difficulty_font = pygame.font.SysFont(None, 30)  # Tamaño de fuente para la dificultad
        self.active = True  # Indica si el menú está activo
        self.difficulty = difficulty  # Agrega el atributo de dificultad
        self.in_instructions = False  # Bandera para saber si está en la pantalla de instrucciones

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if self.in_instructions:
                    self.handle_instructions(event)
                else:
                    self.handle_menu(event)
                    if not self.active:
                        return self.difficulty[1]
                        
            self.screen.fill((0, 0, 0))

            if self.in_instructions:
                self.show_instructions()
            else:
                self.show_main_menu()
            
            pygame.display.flip()

    def handle_menu(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.active = False  # Cambia a la pantalla de juego
                return
            elif event.key == pygame.K_2:
                self.start_difficulty_menu()
            elif event.key == pygame.K_3:
                self.in_instructions = True  # Cambia a la pantalla de instrucciones
            elif event.key == pygame.K_4:
                pygame.quit()
                exit()

    def handle_instructions(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.in_instructions = False  # Regresa al menú principal

    def show_main_menu(self):
        draw_text('Centipede Game', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 4)
        
        # Dibuja la dificultad en la esquina superior derecha
        difficulty_text = f"Dificultad: {self.difficulty[0]}"
        draw_text(difficulty_text, self.difficulty_font, (255, 255, 255), self.screen, self.screen_width - 150, 30)

        draw_text('1. Jugar', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 - 50)
        draw_text('2. Dificultad', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2)
        draw_text('3. Instrucciones', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 + 50)
        draw_text('4. Salir', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 + 100)

    def show_instructions(self):
        draw_text('Instrucciones del juego', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 4)
        
        # Dividir el texto en dos líneas
        draw_text('Usa las flechas para', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2)
        draw_text('mover el jugador', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 + 30)  # Ajustar la posición Y para que esté abajo
        draw_text('Presiona espacio para disparar', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 + 80)
        draw_text('Para pausar el juego presione ESC', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 + 130)
        draw_text('Presiona ESC para volver al menú', self.font, (255, 255, 255), self.screen, self.screen_width // 2, self.screen_height // 2 + 180)
        


    def start_difficulty_menu(self):
        from src.menus.difficulty import DifficultyMenu
        difficulty_menu = DifficultyMenu(self.screen, self.screen_width, self.screen_height)  # Crea una instancia de DifficultyMenu
        difficulty_option = difficulty_menu.run()  # Ejecuta el menú de dificultad
        print(difficulty_option)
        self.difficulty = difficulty_option
