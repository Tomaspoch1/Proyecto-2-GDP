import pygame
import sys

class DifficultyMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width  # Agregado
        self.screen_height = screen_height  # Agregado
        self.font = pygame.font.Font(None, 30)  # Tamaño de fuente más pequeño
        self.options = [["Facil", 5], ["Normal", 10], ["Difícil", 15]]
        self.selected_option = 0
        self.active = True

    def run(self):
        while self.active:
            self.screen.fill((0, 0, 0))  # Color de fondo negro
            self.display_options()
            difficulty_option = self.handle_input()
            pygame.display.flip()
            if difficulty_option != None:
                self.active = False 
                return difficulty_option

    def display_options(self):  
        # Calcular el tamaño total de las opciones para centrar
        total_height = len(self.options[0]) * 70  # Altura total considerando margen
        start_y = (self.screen.get_height() - total_height) // 2  # Centrar verticalmente

        level_text = self.font.render("NIVELES", True, (255, 255, 255))
        
        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_option else (255, 255, 255)
            length = self.get_centipede_length(i)
            text = f"{option[0]}: Centipede de largo {length}"
            rendered_text = self.font.render(text, True, color)

            # Calcular posición para centrar
            text_rect = rendered_text.get_rect(center=(self.screen.get_width() // 2, start_y + i * 70 + 35))
            self.screen.blit(rendered_text, text_rect)  # Posicionar el texto
            
            self.screen.blit(level_text, (self.screen.get_width() // 2 - level_text.get_width() // 2, 150))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_option]
                    
    
    def get_centipede_length(self, option_index):
        if option_index == 0:  # Facil
            return 5
        elif option_index == 1:  # Normal
            return 10
        elif option_index == 2:  # Dificil
            return 15
