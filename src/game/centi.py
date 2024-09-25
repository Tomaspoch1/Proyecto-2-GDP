import pygame
import os
import sys

# Configuración de las rutas de los recursos
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Rutas de las imágenes
image1_path = os.path.join(base_path, "assets", "centipede1.png")
image2_path = os.path.join(base_path, "assets", "centipede2.png")


class Centi(pygame.sprite.Sprite):
    gif_delay = 0
    gif_counter = 0
    gif = []

    def __init__(self, x, y, SCREEN_WIDTH, SCREEN_HEIGHT, SPEED):
        super().__init__()  # Inicializa el sprite
        self.img_size = (20, 20)

        # Carga las imágenes usando las rutas definidas
        self.image = pygame.image.load(image1_path)
        self.gif.append(pygame.image.load(image1_path))
        self.gif.append(pygame.image.load(image2_path))

        # Configura la transparencia de las imágenes
        transparency_color = self.image.get_at((1, 1))
        self.image.set_colorkey(transparency_color)
        for i in range(2):
            self.gif[i].set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.left_right = 1
        self.up_down = 1
        self.vertical_move = 0
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SPEED = SPEED

    def update(self):
        # Gif
        self.gif_delay += 1
        if self.gif_delay % 4 == 0:
            self.image = self.gif[self.gif_counter]
            self.gif_counter += 1
            self.gif_delay = 0
            if self.gif_counter == 2:
                self.gif_counter = 0
        
        # Lógica de movimiento
        if self.vertical_move > 0:
            self.vertical_move -= 1

        if self.left_right == 1 and self.vertical_move == 0:
            self.rect.x += self.SPEED
            # Verificación de colisión con la pared derecha
            if self.rect.x > self.SCREEN_WIDTH:
                self.rect.x -= self.SPEED
                self.collide()
                self.vertical_move -= 1
                if self.rect.y >= self.SCREEN_HEIGHT:
                    self.up_down = 0
                    self.rect.x -= self.SPEED
        elif self.left_right == 0 and self.vertical_move == 0:
            self.rect.x -= self.SPEED
            # Verificación de colisión con la pared izquierda
            if self.rect.x < 0:
                self.rect.x += self.SPEED
                self.collide()
                self.vertical_move -= 1
                if self.rect.y >= self.SCREEN_HEIGHT:
                    self.up_down = 0

    def collide(self):
        self.vertical_move = 2
        if self.left_right == 1:
            self.left_right = 0
            if self.up_down == 1:
                self.rect.y += 20
            else:
                self.rect.y -= 20
        elif self.left_right == 0:
            self.left_right = 1
            if self.up_down == 1:
                self.rect.y += 20
            else:
                self.rect.y -= 20

    def __str__(self) -> str:
        return f"X: {self.rect.x} Y: {self.rect.y}"
