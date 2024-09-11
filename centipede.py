import pygame

class Centipede:
    def __init__(self, length, size, speed, screen_width):
        self.size = size
        self.speed = speed
        self.screen_width = screen_width
        self.segments = self.create_centipede(length)

    def create_centipede(self, length):
        segments = []
        for i in range(length):
            segment_x = self.screen_width // 2 - i * self.size
            segment_y = self.size
            segments.append(pygame.Rect(segment_x, segment_y, self.size, self.size))
        return segments

    def move(self):
        for segment in self.segments:
            segment.x += self.speed
        if self.segments[0].x < 0 or self.segments[0].x > self.screen_width - self.size:
            self.speed *= -1
            for segment in self.segments:
                segment.y += self.size

    def draw(self, screen, color):
        for segment in self.segments:
            pygame.draw.rect(screen, color, segment)
