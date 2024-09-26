import pygame
import os
import sys

# Configuración de las rutas de los recursos
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Rutas de las imágenes
image1_path = os.path.join(base_path, "assets", "player.png")


class Player:
    def __init__(self, x, y, size, speed, screen_width, screen_height):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.alive = True  # Marca al jugador como vivo por defecto
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.image = pygame.image.load(image1_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))  # Redimensionar la imagen al tamaño de la araña

    def move(self, keys):
        # Movimiento horizontal
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < self.screen_width - self.size:
            self.x += self.speed

        # Movimiento vertical (solo en el rango permitido)
        if keys[pygame.K_UP] and self.y > self.screen_height - self.screen_height / 4:  # Permitir mover hacia arriba
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < self.screen_height - self.size:  # Permitir mover hacia abajo
            self.y += self.speed  # Permitir el movimiento hacia abajo dentro del rango

        # Actualiza la posición del rectángulo
        self.rect.topleft = (self.x, self. y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)