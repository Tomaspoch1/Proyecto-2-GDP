import pygame
from assets.config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, RED, GREEN
from src.game.player import Player
from src.game.bullet import BulletManager
from src.game.centi import Centi
from src.game.spider import Spider
from src.utils.utils import draw_text
import random

class Game:
    def __init__(self, screen, difficulty):
        self.screen = screen
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.font = pygame.font.SysFont(None, 55)
        self.game_over = False
        self.score = 0  # Inicializa la puntuación en 0
        self.point_messages = []  # Almacena los mensajes de puntos
        
        # Inicializa el jugador
        self.player = Player(
            self.screen_width // 2, self.screen_height - 50, 20, 5, self.screen_width, self.screen_height
        )

        # Inicializa el administrador de balas
        self.bullet_manager = BulletManager(bullet_delay=500)

        # Inicializa el grupo de ciempiés
        self.centipedes = pygame.sprite.Group()
        self.CENTIS_NUMBERS = difficulty
        CENTI_SPEED = 5
        for m in range(self.CENTIS_NUMBERS):
            centi = Centi(
                20 * m, -20, self.screen_width, self.screen_height, CENTI_SPEED
            )
            self.centipedes.add(centi)

        # Inicializa la araña
        self.spider = None
        self.spawn_timer = 0
        self.spawn_interval = random.randint(2000, 5000)

        # Temporizador de reaparición
        self.respawn_time = 1000  # Tiempo de reaparición en milisegundos
        self.respawn_timer = 0  # Temporizador para el tiempo de reaparición
        self.player_alive = True  # Para manejar el estado del jugador

    def run(self):
        if not self.game_over:
            self.screen.fill(BLACK)
            self.handle_events()
            self.bullet_manager.update(self.screen_height)
            self.centipedes.update()
            self.check_collisions()
            self.draw_objects()
            self.spawn_spider()
            if self.spider:
                self.spider.move()
            self.draw_score()
            self.update_point_messages()
            self.handle_respawn()  # Maneja la reaparición del jugador
        else:
            self.show_game_over()

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if self.player_alive:  # Permite el movimiento solo si el jugador está vivo
            self.player.move(keys)
            if keys[pygame.K_SPACE]:
                self.bullet_manager.shoot(
                    self.player.rect.centerx - 2.5, self.player.rect.top
                )
        if keys[pygame.K_ESCAPE]:
            self.game_over = True

    def spawn_spider(self):
        if self.spider is None:
            self.spawn_timer += pygame.time.Clock().tick(60)
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                self.spider = Spider(self.screen_width, self.screen_height, 30, 2)
                self.spawn_interval = random.randint(2000, 5000)

    def check_collisions(self):
        for bullet in self.bullet_manager.bullets:
            for segment in self.centipedes:
                if bullet.rect.colliderect(segment):
                    self.bullet_manager.bullets.remove(bullet)
                    self.centipedes.remove(segment)
                    self.add_points_centipede(segment.rect.center)
                    break

            # Collision between bullet and spider
            if self.spider and self.spider.is_hit(bullet):
                self.bullet_manager.bullets.remove(bullet)
                spider_center = self.spider.rect.center
                self.add_points_spider(spider_center)  # Añade puntos al matar una araña
                self.spider = None
                break

        # Collision between player and spider
        if self.spider and self.spider.rect.colliderect(self.player.rect):
            self.player.lives -= 1  # Resta una vida al jugador
            if self.player.lives <= 0:
                self.game_over = True  # Termina el juego si no quedan vidas
            else:
                self.reset_player()  # Resetea la posición del jugador y la araña
                
        # Nueva verificación de colisión entre la nave y los segmentos del centipede
        for segment in self.centipedes:
            if self.player.rect.colliderect(segment.rect):
                self.player.lives -= 1  # Resta una vida al jugador
                if self.player.lives <= 0:
                    self.game_over = True  # Termina el juego si no quedan vidas
                self.centipedes.remove(segment)  # O elimina el segmento que colisionó
                break

        if not self.centipedes:
            self.game_over = True  # Termina el juego si el centipede está vacío

    def add_points_centipede(self, position):
        self.score += 150  # Suma 150 puntos por matar un centipede
        self.point_messages.append((150, list(position)))  # Añade un mensaje en la posición del centipede
        print(f"Puntos por matar centipede: {self.score}")  # Para depuración

    def add_points_spider(self, position):
        self.score += 100  # Suma 100 puntos por matar una araña
        self.point_messages.append((100, list(position)))  # Añade un mensaje en la posición de la araña
        print(f"Puntos por matar araña: {self.score}")  # Para depuración

    def draw_objects(self):
        self.player.draw(self.screen, GREEN)
        self.bullet_manager.draw(self.screen, WHITE)
        self.centipedes.draw(self.screen)

        if self.spider:
            self.spider.draw(self.screen, RED)
            
        self.draw_score()
            
    def draw_score(self):
        small_font = pygame.font.SysFont(None, 30)  # Define una fuente más pequeña
        score_text = small_font.render(f"Puntuación: {self.score}", True, WHITE)
        lives_text = small_font.render(f' Vidas: {self.player.lives}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10 + score_text.get_width() + 10, 10))  # Posición en la pantalla

    def update_point_messages(self):
        # Actualiza y dibuja mensajes de puntuación
        for message in self.point_messages[:]:  # Itera sobre una copia para evitar errores al modificar la lista
            points, pos = message
            message_text = self.font.render(f"+{points}", True, WHITE)
            self.screen.blit(message_text, (pos[0], pos[1]))  # Dibuja el mensaje en la posición del objeto
            pos[1] -= 1  # Mueve el mensaje hacia arriba
            if pos[1] < 0:  # Elimina el mensaje si se ha movido fuera de la pantalla
                self.point_messages.remove(message)

    def reset_player(self):
        self.player.rect.x = self.screen_width // 2 - self.player.size // 2  # Reinicia la posición del jugador
        self.player.rect.y = self.screen_height - self.player.size  # Mantenlo en la parte inferior
        self.spider = None  # Haz que la araña desaparezca
        pygame.time.set_timer(pygame.USEREVENT, 5000)  # Espera 1 segundo antes de reaparecer

    def handle_respawn(self):
        if not self.player_alive:
            current_time = pygame.time.get_ticks()
            if current_time - self.respawn_timer >= self.respawn_time:  # Comprueba si ha pasado el tiempo de reaparición
                self.player_alive = True  # El jugador reaparece
                self.reset_player()  # Reinicia al jugador

    def show_game_over(self):
        self.screen.fill(BLACK)
        draw_text('¡Juego Terminado!', self.font, RED, self.screen, self.screen_width // 2, self.screen_height // 2)
        draw_text(f'Puntuación Final: {self.score}', self.font, WHITE, self.screen, self.screen_width // 2, self.screen_height // 2 + 50)
