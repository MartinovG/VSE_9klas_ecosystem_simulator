import pygame
import random

pygame.init()

screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
snake_timer = 0
wolf_timer = 0
rabbit_timer = 0
fox_timer = 0
bear_timer = 0
border_color = ('#808080')
border_thickness = 2

pygame.draw.rect(screen, border_color, (290, 10, 700, 400), border_thickness)

pygame.display.set_caption("Ecosystem Simulator")

clock = pygame.time.Clock()

color1 = ('#0000FF') # Blue
color2 = ('#FF0000') # Red
color3 = ('#00FF00') # Green
color4 = ('#FFFFFF') # White
color5 = ('#FFFF00') #Yellow

def snake(x, y, color):
    for i in range(x, x+10):
        for j in range(y, y+10):
            screen.set_at((i, j), color)

def wolf(x, y, color):
    for i in range(x, x+10):
        for j in range(y, y+10):
            screen.set_at((i, j), color)

def rabbit(x, y, color):
    for i in range(x, x+10):
        for j in range(y, y+10):
            screen.set_at((i, j), color)

def fox(x, y, color):
    for i in range(x, x+10):
        for j in range(y, y+10):
            screen.set_at((i, j), color)

def bear(x, y, color):
    for i in range(x, x+10):
        for j in range(y, y+10):
            screen.set_at((i, j), color)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    x = random.randint(300, screen_width - 20)
    y = random.randint(20, screen_height - 300)

    if random.random() < 0.2:
        if random.random() < 0.2:
            snake(x, y, color1)
        elif random.random() < 0.4:
            wolf(x, y, color2)
        elif random.random() < 0.6:
            rabbit(x, y, color3)
        elif random.random() < 0.8:
            fox(x, y, color4)
        else:
            bear(x, y, color5)

    pygame.display.flip()

    clock.tick(60)
