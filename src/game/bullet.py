import pygame

class Bullet:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def is_off_screen(self, screen_height):
        return self.rect.y < 0 or self.rect.y > screen_height

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)

class BulletManager:
    def __init__(self, bullet_delay):
        self.bullets = []
        self.bullet_timer = 0
        self.bullet_delay = bullet_delay  # Tiempo en milisegundos entre disparos

    def shoot(self, x, y):
        current_time = pygame.time.get_ticks()
        if current_time - self.bullet_timer > self.bullet_delay:
            self.bullet_timer = current_time
            self.bullets.append(Bullet(x, y, 5, 10, -7))  # Ajusta las dimensiones y velocidad según necesites

    def update(self, screen_height):
        for bullet in self.bullets:
            bullet.move()
            if bullet.is_off_screen(screen_height):
                self.bullets.remove(bullet)

    def draw(self, screen, color):
        for bullet in self.bullets:
            bullet.draw(screen, color)
