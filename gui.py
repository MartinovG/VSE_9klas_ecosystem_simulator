import pygame
import random

pygame.init()

# Set the size of the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
snake_timer = 0
wolf_timer = 0
rabbit_timer = 0
fox_timer = 0
bear_timer = 0

# Set the title of the window
pygame.display.set_caption("Random Square")

# Set the clock
clock = pygame.time.Clock()

# Define colors
color1 = ('#0000FF') # Blue
color2 = ('#FF0000') # Red
color3 = ('#00FF00') # Green
color4 = ('#FFFFFF') # White
color5 = ('#FFFF00') #Yellow

# Define functions to draw squares
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

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Generate a random square position and color
    x = random.randint(0, screen_width - 10)
    y = random.randint(0, screen_height - 10)

    # Draw a random square
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

    # Update the display
    pygame.display.flip()

    # Tick the clock
    clock.tick(60)
