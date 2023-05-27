import pygame
import pygame.gfxdraw
import random
from variables import *

class Plant:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy

    def draw(self, screen):
        radius = max(2, min(4, int(self.energy / 20)))
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), radius, PLANT_COLOR)
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), radius, PLANT_COLOR)
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), radius - 2 , PLANT_COLOR2)
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), radius - 2, PLANT_COLOR2)

    def generate_new_plant(plant):
        new_x = plant.x + random.randint(-200, 200)
        new_y = plant.y + random.randint(-200, 200)
        if 390 <= new_x <= SCREEN_WIDTH and SCREEN_HEIGHT - 590 <= new_y <= SCREEN_HEIGHT - 10:
            return Plant(new_x, new_y, plant.energy / 200)
        else:
            return None

    def grow(self):
        self.energy = min(self.energy + PLANT_GROWTH_RATE * self.energy, 100)
         