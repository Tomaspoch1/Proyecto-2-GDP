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
