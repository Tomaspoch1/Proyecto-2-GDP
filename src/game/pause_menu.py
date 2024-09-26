# pause_menu.py
import pygame

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 30)  # Tamaño de fuente más pequeño
        self.running = True

    def display(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False  # Cerrar el juego
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # Presionar c para continuar
                        return "continuar"
                    if event.key == pygame.K_r:  # Presionar R para reiniciar
                        return 'restart'
                    if event.key == pygame.K_q:  # Presionar M para volver al menú principal
                        return 'end'
            
            # Dibuja la pantalla de pausa
            self.screen.fill((0, 0, 0))  # Fondo negro
            pause_text = self.font.render("PAUSA", True, (255, 255, 255))
            continue_text = self.font.render("Presiona C para Continuar", True, (255, 255, 255))
            restart_text = self.font.render("Presiona R para Reiniciar", True, (255, 255, 255))
            main_menu_text = self.font.render("Presiona Q para Finalizar", True, (255, 255, 255))

            # Posiciona los textos en la pantalla
            self.screen.blit(pause_text, (self.screen.get_width() // 2 - pause_text.get_width() // 2, 150))
            self.screen.blit(continue_text, (self.screen.get_width() // 2 - continue_text.get_width() // 2, 250))
            self.screen.blit(restart_text, (self.screen.get_width() // 2 - restart_text.get_width() // 2, 300))
            self.screen.blit(main_menu_text, (self.screen.get_width() // 2 - main_menu_text.get_width() // 2, 350))
            
            pygame.display.flip()
