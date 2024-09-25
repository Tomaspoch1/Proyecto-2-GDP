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

        # Allow vertical movement only if within the lower part of the screen
        self.rect.y += self.direction_y * self.speed

        # Ensure it moves down if it touches the top
        if self.rect.top <= 0:
            self.direction_y = 1

        # Ensure it moves up if it touches the bottom
        if self.rect.bottom >= self.screen_height:
            self.direction_y = -1  # Move up

        # Randomly change vertical direction
        if random.randint(0, 100) < 5:  # 5% chance
            self.direction_y = random.choice([-1, 0, 1])

        # Prevent spider from getting stuck at the top or bottom
        if self.rect.top <= 0:
            self.rect.top = 1  # Prevents it from getting stuck at the ceiling
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height - 1  # Prevents it from getting stuck at the bottom

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)

    def is_hit(self, bullet):
        return self.rect.colliderect(bullet.rect)

