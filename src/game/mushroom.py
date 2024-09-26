import pygame
import sys
import os
import random  # Para generar posiciones aleatorias

# Configuración de las rutas de los recursos
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))
    
image_mashroom1_path = os.path.join(base_path, "assets", "mashroom1.png")  # Carga la imagen del hongo

image_mashroom2_path = os.path.join(base_path, "assets", "mashroom2.png")  # Carga la imagen del hongo

image_mashroom3_path = os.path.join(base_path, "assets", "mashroom3.png")  # Carga la imagen del hongo

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #imagen 1
        self.image1 = pygame.image.load(image_mashroom1_path).convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, (20, 20))
        self.rect = self.image1.get_rect(topleft=(x, y))
        
        #imagen2
        self.image2 = pygame.image.load(image_mashroom2_path).convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (20, 20))
        self.rect = self.image2.get_rect(topleft=(x, y))
        
        #imagen3
        self.image3 = pygame.image.load(image_mashroom3_path).convert_alpha()
        self.image3 = pygame.transform.scale(self.image3, (20, 20))
        self.rect = self.image3.get_rect(topleft=(x, y))
        
        self.health = 3  # Los champiñones pueden recibir algunos golpes antes de ser destruidos
        
        


    def draw(self, screen):
        if self.health == 3:
            screen.blit(self.image1, self.rect.topleft)
            
        elif self.health == 2:
            screen.blit(self.image2, self.rect.topleft)
        
        else:
            screen.blit(self.image3, self.rect.topleft)
            
    def take_damage(self, screen):
        self.health -= 1
        if self.health <= 0:
            return True  # Champiñón destruido
        else:
            self.draw(screen)
        return False  # Champiñón sigue con salud

    
class MushroomManager:
    def __init__(self, screen_width, screen_height, cuantity):
        self.mushroom_group = pygame.sprite.Group()
        self.mushroom_size = 20  # Tamaño del champiñón
        self.cols = screen_width // 20  # Espacio entre champiñones horizontalmente
        self.rows = screen_height // 20  # Espacio entre champiñones verticalmente

        # Definir el límite inferior para las posiciones de los champiñones
        self.min_y = screen_height * 3 // 4  # Último cuarto de la pantalla

        # Lista de todas las posiciones posibles en la cuadrícula, asegurando que los champiñones no se coloquen fuera de la pantalla
        self.possible_positions = [
            (col * self.mushroom_size, row * self.mushroom_size)
            for row in range(self.rows)
            for col in range(self.cols)
            if row * self.mushroom_size <= self.min_y - 15 and col * self.mushroom_size + self.mushroom_size <= screen_width  # Asegurar que el champiñón no exceda el ancho de la pantalla
        ]
        
        
        # Barajar las posiciones para que queden aleatorias
        random.shuffle(self.possible_positions)
        
        self.create_mushrooms(cuantity)

    def create_mushrooms(self, cuantity):      
        # Seleccionar 15 posiciones aleatorias de la lista posible, asegurándose de que haya suficientes posiciones
        position_selected = random.sample(self.possible_positions, min(cuantity, len(self.possible_positions)))

        # Crear champiñones en posiciones aleatorias
        for position in position_selected:
            x, y = position  # Obtener una posición aleatoria
            mushroom = Mushroom(x, y)  # Crea el champiñón en la posición calculada
            self.mushroom_group.add(mushroom)  # Añade el champiñón al grupo
            self.possible_positions.remove(position)

    def draw(self, screen):
        for mushroom in self.mushroom_group:
            mushroom.draw(screen)

    def check_collision_with_bullets(self, bullets, screen):
        for bullet in bullets:
            # Comprobar colisiones con los champiñones
            collided_mushrooms = pygame.sprite.spritecollide(bullet, self.mushroom_group, False)
            for mushroom in collided_mushrooms:
                if mushroom.take_damage(screen):
                    x = mushroom.rect.x
                    y = mushroom.rect.y
                    position = mushroom.rect.center
                    self.possible_positions.append((x,y))
                    self.mushroom_group.remove(mushroom)  # Eliminar el champiñón si está destruido
                    bullets.remove(bullet)
                    return True, position
                bullets.remove(bullet)  # Eliminar la bala después de la colisión
                break  # Detener la verificación si la bala golpea un champiñón
            return None


    def get_mushroom_group(self):
        return self.mushroom_group
