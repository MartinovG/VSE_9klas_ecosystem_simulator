import pygame
from variables import *

def plot_results(herbivores_counts, predators_counts, plants_counts):
    import matplotlib.pyplot as plt

    time_steps = list(range(len(herbivores_counts)))

    plt.plot(time_steps, herbivores_counts, label="Herbivores", color="blue")
    plt.plot(time_steps, predators_counts, label="Predators", color="red")
    plt.plot(time_steps, plants_counts, label="Plants", color="green")

    plt.xlabel("Time Steps")
    plt.ylabel("Count")
    plt.title("Population Dynamics")
    plt.legend()

    plt.show()

def draw_button(screen, button_rect, text): #simulation control buttons
    pygame.draw.rect(screen, (100, 100, 100), button_rect, 0)
    pygame.draw.rect(screen, (200, 200, 200), button_rect, 1)

    font = pygame.font.Font(None, 24)
    label = font.render(text, 1, (255, 255, 255))
    screen.blit(label, (button_rect.x + button_rect.width // 2 - label.get_width() // 2,
                        button_rect.y + button_rect.height // 2 - label.get_height() // 2))

def draw_text_box(screen, base_font, text, color, input_rect): #animal number control text boxes
    pygame.draw.rect(screen, color, input_rect)
    text_surface = base_font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    input_rect.w = max(100, text_surface.get_width() + 10)