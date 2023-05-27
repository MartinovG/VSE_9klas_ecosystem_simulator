import math
from variables import *
from main import plant_angles, herbivore_angles, predator_angles

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

def tornado_plants(plants, mouse_x, mouse_y, radius, speed, attraction_speed):
    for i, plant in enumerate(plants):
        dx = (mouse_x - plant.x)
        dy = (mouse_y - plant.y)
        distance = math.sqrt(dx**2 + dy**2)
        angle = plant_angles[i]

        if distance <= radius:
            new_angle = angle + speed
            new_distance = distance - attraction_speed
            new_x = mouse_x + math.cos(new_angle) * new_distance
            new_y = mouse_y + math.sin(new_angle) * new_distance

            new_x = max(390, min(new_x, SCREEN_WIDTH))
            new_y = max(SCREEN_HEIGHT - 590, min(new_y, 590))

            plant.x, plant.y = new_x, new_y
            plant_angles[i] = new_angle

def tornado_herbivores(herbivores, mouse_x, mouse_y, radius, speed, attraction_speed):
    for i, herbivore in enumerate(herbivores):
        dx = (mouse_x - herbivore.x)
        dy = (mouse_y - herbivore.y)
        distance = math.sqrt(dx**2 + dy**2)
        angle = herbivore_angles[i]

        if distance <= radius:
            new_angle = angle + speed
            new_distance = distance - attraction_speed
            new_x = mouse_x + math.cos(new_angle) * new_distance
            new_y = mouse_y + math.sin(new_angle) * new_distance

            new_x = max(390, min(new_x, SCREEN_WIDTH))
            new_y = max(SCREEN_HEIGHT - 590, min(new_y, 590))

            herbivore.x, herbivore.y = new_x, new_y
            herbivore_angles[i] = new_angle

def tornado_predators(predators, mouse_x, mouse_y, radius, speed, attraction_speed):
    for i, predator in enumerate(predators):
        dx = (mouse_x - predator.x)
        dy = (mouse_y - predator.y)
        distance = math.sqrt(dx**2 + dy**2)
        angle = predator_angles[i]

        if distance <= radius:
            new_angle = angle + speed
            new_distance = distance - attraction_speed
            new_x = mouse_x + math.cos(new_angle) * new_distance
            new_y = mouse_y + math.sin(new_angle) * new_distance

            new_x = max(390, min(new_x, SCREEN_WIDTH))
            new_y = max(SCREEN_HEIGHT - 590, min(new_y, 590))

            predator.x, predator.y = new_x, new_y
            predator_angles[i] = new_angle
   