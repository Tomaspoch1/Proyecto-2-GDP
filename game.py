import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, RED, GREEN
from player import Player
from bullet import BulletManager
from spider import Spider
from centi import Centi  # Asegúrate de que está importando la nueva clase Centi
from utils import draw_text
from mushroom import Mushroom, MushroomManager

import random


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.font = pygame.font.SysFont(None, 55)
        self.game_over = False

        # Inicializa el jugador
        self.player = Player(
            self.screen_width // 2, self.screen_height - 50, 30, 5, self.screen_width
        )

        # Inicializa el administrador de balas
        self.bullet_manager = BulletManager(bullet_delay=500)

        # Inicializa el grupo de ciempiés
        self.centipedes = pygame.sprite.Group()
        self.CENTIS_NUMBERS = 12
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

        # Inicializa el administrador de los champiñones
        self.mushroom_manager = MushroomManager(self.screen_width, self.screen_height, 20, 15)

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
        else:
            self.show_game_over()

    def handle_events(self):
        keys = pygame.key.get_pressed()
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
            hit_list = pygame.sprite.spritecollide(bullet, self.centipedes, True)
            if hit_list:
                self.bullet_manager.bullets.remove(bullet)
                if len(self.centipedes) == 0:  # No centipedes left
                    self.game_over = True

            # Collision between bullet and spider
            if self.spider and self.spider.is_hit(bullet):
                self.bullet_manager.bullets.remove(bullet)
                self.spider = None
                break

        # Check bullet and mushroom collision
        self.mushroom_manager.check_collision_with_bullets(self.bullet_manager.bullets)
        
        # Collision with spider
        if self.spider:
            # Collision between spider and player
            if self.spider and self.player.rect.colliderect(self.spider.rect):
                self.game_over = True

            # Collision between spider and mushroom
            hit_mushrooms = pygame.sprite.spritecollide(self.spider, self.mushroom_manager.mushrooms, False)
            if hit_mushrooms:
                for mushroom in hit_mushrooms:
                    self.mushroom_manager.mushrooms.remove(mushroom)

        # Check if all centipedes are gone
        if len(self.centipedes) == 0:
            self.game_over = True

    def draw_objects(self):
        self.player.draw(self.screen, GREEN)
        self.bullet_manager.draw(self.screen, WHITE)
        self.centipedes.draw(self.screen)

        if self.spider:
            self.spider.draw(self.screen, RED)

        self.mushroom_manager.draw(self.screen, GREEN)

    def show_game_over(self):
        self.screen.fill(BLACK)
        draw_text(
            "¡Juego Terminado!",
            self.font,
            RED,
            self.screen,
            self.screen_width // 2,
            self.screen_height // 2,
        )
