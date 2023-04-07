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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Ecosystem Simulator")
clock = pygame.time.Clock()

class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen ):
        radius = 5
        pygame.gfxdraw.filled_circle(screen, self.x, self.y, radius, PLANT_COLOR)

plants = [Plant(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(10)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:        
            pygame.quit()
            quit()
    
    screen.fill(BACKGROUND_COLOR)
        
    for plant in plants:
        plant.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

