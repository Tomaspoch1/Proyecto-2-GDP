import pygame

class Player:
    def __init__(self, x, y, size, speed, screen_width, screen_height):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lives = 3
        self.alive = True  # Marca al jugador como vivo por defecto
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

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

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
