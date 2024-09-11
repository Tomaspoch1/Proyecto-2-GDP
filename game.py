import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, RED, GREEN
from player import Player
from bullet import Bullet
from centipede import Centipede
from utils import draw_text

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.font = pygame.font.SysFont(None, 55)
        self.game_over = False
        
        # Inicializa el jugador
        self.player = Player(self.screen_width // 2, self.screen_height - 50, 50, 5, self.screen_width)
        
        # Inicializa las balas
        self.bullet_speed = -7
        self.bullets = []
        
        # Inicializa el centipede
        self.centipede = Centipede(10, 20, 3, self.screen_width)

    def run(self):
        if not self.game_over:
            self.screen.fill(BLACK)
            self.handle_events()
            self.move_bullets()
            self.centipede.move()
            self.check_collisions()
            self.draw_objects()
        else:
            self.show_game_over()

    def handle_events(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        if keys[pygame.K_SPACE]:
            self.fire_bullet()
        if keys[pygame.K_ESCAPE]:
            self.game_over = True

    def fire_bullet(self):
        x = self.player.rect.centerx - 2.5
        y = self.player.rect.top
        self.bullets.append(Bullet(x, y, 5, 10, self.bullet_speed))

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.move()
            if bullet.is_off_screen(self.screen_height):
                self.bullets.remove(bullet)

    def check_collisions(self):
        for bullet in self.bullets:
            for segment in self.centipede.segments:
                if bullet.rect.colliderect(segment):
                    self.bullets.remove(bullet)
                    self.centipede.segments.remove(segment)
                    break
        if not self.centipede.segments:
            self.game_over = True  # Termina el juego si el centipede está vacío

    def draw_objects(self):
        self.player.draw(self.screen, GREEN)
        for bullet in self.bullets:
            bullet.draw(self.screen, WHITE)
        self.centipede.draw(self.screen, RED)

    def show_game_over(self):
        self.screen.fill(BLACK)
        draw_text('¡Juego Terminado!', self.font, RED, self.screen, self.screen_width // 2, self.screen_height // 2)

  