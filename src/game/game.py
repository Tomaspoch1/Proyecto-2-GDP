import pygame
from assets.config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, RED, GREEN
from src.game.player import Player
from src.game.bullet import BulletManager
from src.game.spider import Spider
from src.game.centi import Centi  # Asegúrate de que está importando la nueva clase Centi
from src.utils.utils import draw_text
from src.game.mushroom import Mushroom, MushroomManager

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
        self.lives = 3 #Vidas iniciales del jugador
        self.death_time_player = 0
        self.death_time_spider = 0
        self.death_time_centi = 0
        self.player_alive = True  # Bandera para saber si el jugador está vivo
        self.spider_alive = False
        self.centi_alive = True
        
        
        # Inicializa el jugador
        self.player = Player(
            self.screen_width // 2, self.screen_height - 50, 20, 5, self.screen_width, self.screen_height
        )

        # Inicializa el administrador de balas
        self.bullet_manager = BulletManager(bullet_delay=500)

        # Inicializa el administrador de los champiñones
        self.mushroom_manager = MushroomManager(self.screen_width, self.screen_height, 15)
        
        # Inicializa el grupo de ciempiés
        self.centipedes = pygame.sprite.Group()
        self.CENTIS_NUMBERS = difficulty
        self.centi_speed = 7
        self.centipedes = pygame.sprite.Group()
        for m in range(self.CENTIS_NUMBERS):
            centi = Centi(
                20 * m, -20, self.screen_width, self.screen_height, self.centi_speed, mushroom_group=self.mushroom_manager.get_mushroom_group()
            )
            self.centipedes.add(centi)
        

        # Inicializa la araña
        self.spider = None
        self.spawn_interval_spider = random.randint(3000, 5000)
        
        #Temporizador de reaparicion centipede
        self.spawn_time_centi = 5000  # Tiempo de reaparición en milisegundos


        # Temporizador de reaparición jugador
        self.respawn_time_player = 1000  # Tiempo de reaparición en milisegundos
        
    def run(self):
        if not self.game_over:
            self.screen.fill(BLACK)
            self.handle_events()
            self.bullet_manager.update(self.screen_height)
            self.check_collisions()
            self.draw_objects()
            if self.centi_alive:
                self.centipedes.update()
            if not self.centi_alive and pygame.time.get_ticks() - self.death_time_centi > self.spawn_time_centi:
                self.spawn_centipede()
            if not self.spider_alive and pygame.time.get_ticks() - self.death_time_spider > self.spawn_interval_spider:
                self.spawn_spider()
            if self.spider:
                self.spider.move()
            self.draw_score()
            self.update_point_messages()
            self.handle_respawn()  # Maneja la reaparición del jugador y la araña
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
                
    def check_collisions(self):
        for bullet in self.bullet_manager.bullets:
            if self.centi_alive:
                for segment in self.centipedes:
                    if bullet.rect.colliderect(segment.rect):
                        self.bullet_manager.bullets.remove(bullet)
                        self.centipedes.remove(segment)
                        self.add_points_centipede(segment.rect.center)
                        self.mushroom_manager.create_mushrooms(1)
                        if len(self.centipedes) == 0:
                            self.reset_centipede()
                        break
                    
            # Collision between bullet and spider
            if self.spider and self.spider.is_hit(bullet):
                self.bullet_manager.bullets.remove(bullet)
                spider_center = self.spider.rect.center
                self.add_points_spider(spider_center)  # Añade puntos al matar una araña
                self.reset_spider()
                break
        
        
        
        
        
        # Check bullet and mushroom collision
        result = self.mushroom_manager.check_collision_with_bullets(self.bullet_manager.bullets, self.screen)
        
        if result is not None:  # Solo si hay colisión
            mushroom_position = result  # Desempaquetar los valores si hay colisión
            self.add_points_mushroom(mushroom_position[1])  # Sumar puntos y mostrar mensaje
            
        # Collision with spider with mushrooms
        if self.spider:
            # Collision between spider and mushroom
            hit_mushrooms = pygame.sprite.spritecollide(self.spider, self.mushroom_manager.mushroom_group, False)
            if hit_mushrooms:
                for mushroom in hit_mushrooms:
                    self.mushroom_manager.mushroom_group.remove(mushroom)  # Cambia a mushroom_group

        # Collision between player and spider
        if self.spider and self.spider.rect.colliderect(self.player.rect):
            self.lives -= 1  # Resta una vida al jugador
            if self.lives <= 0:
                self.game_over = True  # Termina el juego si no quedan vidas
            else:
                self.reset_player()  # Resetea la posición del jugador
                self.reset_spider()
                
        # Nueva verificación de colisión entre la nave y los segmentos del centipede
        if self.centi_alive:
            for segment in self.centipedes:
                if self.player.rect.colliderect(segment.rect):
                    self.lives -= 1  # Resta una vida al jugador
                    if self.lives <= 0:
                        self.game_over = True  # Termina el juego si no quedan vidas
                    else:
                        self.reset_player()  # Resetea la posición del jugador
                        self.reset_centipede()
                    break

                
        

    def add_points_centipede(self, position):
        self.score += 150  # Suma 150 puntos por matar un centipede
        self.point_messages.append((150, list(position)))  # Añade un mensaje en la posición del centipede
        #print(f"Puntos por matar centipede: {self.score}")  # Para depuración

    def add_points_spider(self, position):
        self.score += 100  # Suma 100 puntos por matar una araña
        self.point_messages.append((100, list(position)))  # Añade un mensaje en la posición de la araña
        print(f"Puntos por matar araña: {self.score}")  # Para depuración

    def add_points_mushroom(self, position):
        self.score += 50  # Suma 50 puntos por destruir un champiñón
        self.point_messages.append((50, list(position)))  # Añade un mensaje en la posición del champiñón
        print(f"Puntos por destruir champiñón: {self.score}")  # Para depuración

    
    def draw_objects(self):
        if self.player_alive:
            self.player.draw(self.screen)
        self.bullet_manager.draw(self.screen, WHITE)
        if self.centi_alive:
            self.centipedes.draw(self.screen)

        if self.spider:
            self.spider.draw(self.screen)
            
        self.mushroom_manager.draw(self.screen)
            
        self.draw_score()
            
    def draw_score(self):
        small_font = pygame.font.SysFont(None, 30)  # Define una fuente más pequeña
        score_text = small_font.render(f"Puntuación: {self.score}", True, WHITE)
        lives_text = small_font.render(f' Vidas: {self.lives}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10 + score_text.get_width() + 10, 10))  # Posición en la pantalla

    def update_point_messages(self):
        small_font = pygame.font.SysFont(None, 20)  # Fuente más pequeña (tamaño 20)
        # Actualiza y dibuja mensajes de puntuación
        for message in self.point_messages[:]:  # Itera sobre una copia para evitar errores al modificar la lista
            points, pos = message
            message_text = small_font.render(f"+{points}", True, WHITE)
            self.screen.blit(message_text, (pos[0], pos[1]))  # Dibuja el mensaje en la posición del objeto
            pos[1] -= 1  # Mueve el mensaje hacia arriba
            if pos[1] < 0:  # Elimina el mensaje si se ha movido fuera de la pantalla
                self.point_messages.remove(message)

    def reset_player(self):
        self.death_time_player = pygame.time.get_ticks()  # Inicia el temporizador de reaparición
        self.player_alive = False  # Marca al jugador como no vivo
                
    def reset_spider(self):
        self.death_time_spider = pygame.time.get_ticks()  # Reinicia el temporizador de reaparición        
        self.spider = None  # Elimina la araña
        self.spider_alive = False
        
    def reset_centipede(self):
        self.death_time_centi = pygame.time.get_ticks()  # Reinicia el temporizador de reaparición        
        self.centipedes = None  # Elimina la centipede
        self.centi_alive = False

    def spawn_centipede(self):
        # Inicializa el grupo de ciempiés
        self.centipedes = pygame.sprite.Group()
        for m in range(self.CENTIS_NUMBERS):
            centi = Centi(
                20 * m, -20, self.screen_width, self.screen_height, self.centi_speed, mushroom_group=self.mushroom_manager.get_mushroom_group()
            )
            self.centipedes.add(centi)
        self.centi_alive = True
        
    def handle_respawn(self):
        # Maneja la reaparición del jugador
        if not self.player_alive:
            if pygame.time.get_ticks() - self.death_time_player > self.respawn_time_player:
                self.respawn_player()

        # Maneja la reaparición de la araña
        if self.spider_alive and self.spider is None:
            if pygame.time.get_ticks() - self.death_time_spider > self.spawn_interval_spider:
                self.respawn_player()
    
    def respawn_player(self):
        # Reaparece al jugador después del temporizador
        self.player = Player(
            self.screen_width // 2, self.screen_height - 50, 20, 5, self.screen_width, self.screen_height
        )
        self.player_alive = True  # Marca al jugador como vivo

    def spawn_spider(self):
        self.spider = Spider(self.screen_width, self.screen_height, 20, 2)
        self.spider_alive = True  # Marca a la araña como viva
        
    def show_game_over(self):
        self.screen.fill(BLACK)
        draw_text('¡Juego Terminado!', self.font, RED, self.screen, self.screen_width // 2, self.screen_height // 2)
        draw_text(f'Puntuación Final: {self.score}', self.font, WHITE, self.screen, self.screen_width // 2, self.screen_height // 2 + 50)
