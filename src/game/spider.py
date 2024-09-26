import pygame
import random
import os
import sys

# Configuración de las rutas de los recursos
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Rutas de las imágenes
image1_path = os.path.join(base_path, "..", "..", "assets", "spider.png")


class Spider:
    def __init__(self, screen_width, screen_height, size, speed):
        self.size = size
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = pygame.Rect(random.randint(0, screen_width - size), screen_height - size * 2, size, size)

        # Cargar la imagen de la araña y redimensionarla
        self.image = pygame.image.load(image1_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))  # Redimensionar la imagen al tamaño de la araña

        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 0, 1])

    def move(self):
        # Mover en la dirección actual
        self.rect.x += self.direction_x * self.speed
        
        # Cambiar de dirección si toca los lados de la pantalla
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.direction_x *= -1

        # Permitir movimiento vertical solo si está dentro de la parte inferior de la pantalla
        self.rect.y += self.direction_y * self.speed

        # Asegurarse de que se mueva hacia abajo si toca la parte superior
        if self.rect.top <= 0:
            self.direction_y = 1

        # Asegurarse de que se mueva hacia arriba si toca la parte inferior
        if self.rect.bottom >= self.screen_height:
            self.direction_y = -1  # Mover hacia arriba

        # Cambiar la dirección vertical aleatoriamente
        if random.randint(0, 100) < 5:  # 5% de probabilidad
            self.direction_y = random.choice([-1, 0, 1])

        # Evitar que la araña se quede atascada en la parte superior o inferior
        if self.rect.top <= 0:
            self.rect.top = 1  # Evita que se quede pegada al techo
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height - 1  # Evita que se quede pegada al fondo

    def draw(self, screen):
        # Dibujar la imagen de la araña en la pantalla
        screen.blit(self.image, self.rect.topleft)

    def is_hit(self, bullet):
        return self.rect.colliderect(bullet.rect)
