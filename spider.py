import pygame
import random

class Spider:
    def __init__(self, screen_width, screen_height, size, speed):
        self.size = size
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = pygame.Rect(random.randint(0, screen_width - size), screen_height - size * 2, size, size)
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 0, 1])

    def move(self):
        # Move in current direction
        self.rect.x += self.direction_x * self.speed
        
        # Change direction if touches the side of the screen
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.direction_x *= -1

        if self.rect.top > 0:
            self.rect.y += self.direction_y * self.speed

        if self.rect.top <= 0:
            self.direction_y = 1

        if self.rect.bottom >= self.screen_height:
            self.direction_y = -1  # Mueve hacia arriba

        # Change vertical direction
        if random.randint(0, 100) < 5:  # 5%
            self.direction_y = random.choice([-1, 0, 1])

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)

    def is_hit(self, bullet):
        return self.rect.colliderect(bullet.rect)

