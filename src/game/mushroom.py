import pygame
import random

class Mushroom:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.health = 2  # Mushrooms can take a few hits before being destroyed

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
    
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            return True  # Mushroom is destroyed
        return False  # Mushroom still has health left

class MushroomManager:
    def __init__(self, screen_width, screen_height, mushroom_size, num_mushrooms):
        self.mushrooms = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.mushroom_size = mushroom_size
        self.num_mushrooms = num_mushrooms
        self.populate_mushrooms()

    def populate_mushrooms(self):
        for _ in range(self.num_mushrooms):
            x = random.randint(0, self.screen_width - self.mushroom_size)
            y = random.randint(self.mushroom_size, self.screen_height * 2 // 3)  # Mushrooms spawn in the top two-thirds
            mushroom = Mushroom(x, y, self.mushroom_size)
            self.mushrooms.append(mushroom)

    def draw(self, screen, color):
        for mushroom in self.mushrooms:
            mushroom.draw(screen, color)

    def check_collision_with_bullets(self, bullets):
        for bullet in bullets:
            for mushroom in self.mushrooms:
                if bullet.rect.colliderect(mushroom.rect):
                    if mushroom.take_damage():
                        self.mushrooms.remove(mushroom)  # Remove mushroom if destroyed
                    bullets.remove(bullet)  # Remove the bullet after collision
                    break  # Stop checking further once the bullet hits a mushroom

