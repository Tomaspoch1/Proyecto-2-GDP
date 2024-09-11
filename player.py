import pygame

class Player:
    def __init__(self, x, y, size, speed, screen_width):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.screen_width = screen_width
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < self.screen_width - self.size:
            self.x += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
