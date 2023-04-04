import pygame
import pygame_widgets
import random

pygame.init()

screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
button_color = ('#808080')
color1 = ('#0000FF') # Blue
color2 = ('#FF0000') # Red
color3 = ('#00FF00') # Green
color4 = ('#FFFFFF') # White
color5 = ('#FFFF00') #Yellow
border_color = ('#808080') # Grey
border_thickness = 2
font = pygame.font.Font(None, 36)
button_rect = pygame.draw.rect(screen, button_color, pygame.Rect(10, 10, 100, 50))
button_color = ('#808080')


pygame.draw.rect(screen, border_color, (290, 10, 700, 400), border_thickness)

pygame.display.set_caption("Ecosystem Simulator")

clock = pygame.time.Clock()

spawning = False

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


def draw_button_off():
    button_text = "Start!"
    text_surf = font.render(button_text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=button_rect.center)
    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(text_surf, text_rect)
    pygame.display.flip()

def draw_button_on():
    button_text = "Stop!"
    text_surf = font.render(button_text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=button_rect.center)
    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(text_surf, text_rect)
    pygame.display.flip()


def button_click():
    global spawning
    spawning = not spawning

draw_button_off()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                button_click()

    if spawning:
        draw_button_on()
    else:
        draw_button_off()

    if spawning:
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
        pygame.display.update()

    clock.tick(60)