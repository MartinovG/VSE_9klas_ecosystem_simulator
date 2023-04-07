import pygame
import pygame.gfxdraw
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = ('#FFFFFF') # White
PLANT_COLOR = (0, 255, 0) # Green
HERBIVORE_COLOR = (0, 0, 255) # Red
PREDATOR_COLOR = (255, 0, 0) # Blue

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Ecosystem Simulator")
clock = pygame.time.Clock()

class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen ):
        pygame.gfxdraw.filled_circle(screen, self.x, self.y, 5, PLANT_COLOR)
        pygame.gfxdraw.aacircle(screen, self.x, self.y, 5, PLANT_COLOR)

class Herbivore:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), 10, HERBIVORE_COLOR)
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), 10, HERBIVORE_COLOR)

class Predator:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), 10, PREDATOR_COLOR)
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), 10, PREDATOR_COLOR)

plants = [Plant(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(10)]
herbivores = [Herbivore(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(5)]
predators = [Predator(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(3)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:        
            pygame.quit()
            quit()
    
    screen.fill(BACKGROUND_COLOR)
        
    for plant in plants:
        plant.draw(screen)

    for herbivore in herbivores:
        herbivore.draw(screen)
    
    for predator in predators:
        predator.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

