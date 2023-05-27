import pygame
import random
import math
import sys
from variables import *
from Plants import *
from Herbivores import *
from Predators import *

pygame.init()

base_font = pygame.font.Font(None, 32)
pygame.font.init()
font = pygame.font.Font(None, 36)
text = font.render("Hold here", True, (0, 0, 0))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Ecosystem Simulator")
clock = pygame.time.Clock()
image1 = pygame.image.load("tornado.png")
image2 = pygame.image.load("fire.png")

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
   
plants = [Plant(random.randint(390, SCREEN_WIDTH), random.randint(SCREEN_HEIGHT - 590, 590), PLANT_ENERGY) for _ in range(int(initial_plants))]
herbivores = [Herbivore(random.randint(390, SCREEN_WIDTH), random.randint(SCREEN_HEIGHT - 590, 590), HERBIVORE_ENERGY) for _ in range(int(initial_herbivores))]
predators = [Predator(random.randint(390, SCREEN_WIDTH), random.randint(SCREEN_HEIGHT - 590, 590), PREDATOR_ENERGY) for _ in range(int(initial_predators))]

running = True
dragging1 = False
dragging2 = False
mouse_down = False
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if image1_x <= mouse_x <= image1_x + image1.get_width() and image1_y <= mouse_y <= image1_y + image1.get_height():
                dragging1 = True
                mouse_offset_x1 = mouse_x - image1_x
                mouse_offset_y1 = mouse_y - image1_y

            if image2_x <= mouse_x <= image2_x + image2.get_width() and image2_y <= mouse_y <= image2_y + image2.get_height():
                dragging2 = True
                mouse_offset_x2 = mouse_x - image2_x
                mouse_offset_y2 = mouse_y - image2_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging1:
                if area_x <= image1_x <= area_x + area_w - image1.get_width() and area_y <= image1_y <= area_y + area_h - image1.get_height():
                    image1_x, image1_y = start_x1, start_y1
                    image1 = pygame.image.load("tornado.png")
                    print("Tornado")
                else:
                    image1_x, image1_y = start_x1, start_y1
                dragging1 = False

            if dragging2:
                if area_x <= image2_x <= area_x + area_w - image2.get_width() and area_y <= image2_y <= area_y + area_h - image2.get_height():
                    image2_x, image2_y = start_x2, start_y2
                    image2 = pygame.image.load("fire.png")
                else:
                    image2_x, image2_y = start_x2, start_y2
                dragging2 = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging1:
                mouse_x, mouse_y = event.pos
                image1_x = mouse_x - mouse_offset_x1
                image1_y = mouse_y - mouse_offset_y1

            if dragging2:
                mouse_x, mouse_y = event.pos
                image2_x = mouse_x - mouse_offset_x2
                image2_y = mouse_y - mouse_offset_y2

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                simulation_running = not simulation_running
                button_text = "Start" if button_text == "Pause" else "Pause"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect2.collidepoint(event.pos):
                simulation_started = not simulation_started
                button_text2 = "Finish" if button_text2 == "Begin" else "Begin"

        if event.type == pygame.MOUSEBUTTONDOWN: #plants
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
                
        if event.type == pygame.MOUSEBUTTONDOWN: #herbivores 
            if input_rect2.collidepoint(event.pos):
                active2 = True
            else:
                active2 = False

        if event.type == pygame.MOUSEBUTTONDOWN: #predators
            if input_rect3.collidepoint(event.pos):
                active3 = True
            else:
                active3 = False

        if event.type == pygame.MOUSEBUTTONDOWN: #temperature
            if input_rect4.collidepoint(event.pos):
                active4 = True
            else:
                active4 = False


        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:
                if active:
                    initial_plants = initial_plants[:-1]
                if active2:
                    initial_herbivores = initial_herbivores[:-1]
                if active3:
                    initial_predators = initial_predators[:-1]
                if active4:
                    temperature = temperature[:-1]
            else:
                if active:
                    initial_plants += event.unicode
                if active2:
                    initial_herbivores += event.unicode
                if active3:
                    initial_predators += event.unicode
                if active4:
                    temperature += event.unicode
            
            plants_count = int(initial_plants)
            herbivores_count = int(initial_herbivores)
            predators_count = int(initial_predators)

    screen.fill(BACKGROUND_COLOR)
    screen.blit(image1, (image1_x, image1_y))
    screen.blit(image2, (image2_x, image2_y))
    draw_button(screen, button_rect, button_text)
    draw_button(screen, button_rect2, button_text2)
    pygame.gfxdraw.rectangle(screen, pygame.Rect(389, SCREEN_HEIGHT - 591, SCREEN_WIDTH, 583), BORDER_COLOR) #simulation border

    if not simulation_started:
        if button_text2 == "Begin":
            for plant in plants:
                plant.draw(screen)

            for herbivore in herbivores:
                herbivore.draw(screen)
                
            for predator in predators:
                predator.draw(screen)

    if not simulation_running:

        if -20 <= int(temperature) <= 20:
            HERBIVORE_SPEED = 0.1 + (int(temperature) + 20) * (1 - 0.1) / (20 - (-20))
            PREDATOR_SPEED = 0.1 + (int(temperature) + 20) * (0.5 - 0.1) / (20 - (-20))
        elif 20 < int(temperature) <= 50:
            HERBIVORE_SPEED = 1 - (int(temperature) - 20) * (1 - 0.1) / (50 - 20)
            PREDATOR_SPEED = 0.5 - (int(temperature) - 20) * (0.5 - 0.1) / (50 - 20)
        elif int(temperature) <= -25 or int(temperature) >= 55:
            ENERGY_DEPLETION_FACTOR = 0.001
        else:
            HERBIVORE_SPEED = 0.1
            PREDATOR_SPEED = 0.1

        for plant in plants:
            plant.grow()
        
            if random.random() < PLANT_REPRODUCTION_RATE / 5:
                new_plant = plant.generate_new_plant()
                if new_plant is not None:
                    plants.append(new_plant)
                    plants_count += 1
                    
        for herbivore in herbivores:
            herbivore.move_towards_food(plants)
            herbivore.move()
            herbivore.energy -= HERBIVORE_ENERGY_COST

            for plant in plants:
                if herbivore.eat(plant):
                    plants.remove(plant)
                    plants_count -= 1

            new_herbivore = herbivore.reproduce()
            if new_herbivore is not None:
                herbivores.append(new_herbivore)
                herbivores_count += 1

            if herbivore.energy <= 50:
                herbivores.remove(herbivore)
                herbivores_count -= 1

        for predator in predators:
            predator.move_towards_food(herbivores)
            predator.move()
            predator.energy -= PREDATOR_ENERGY_COST

            for herbivore in herbivores:
                if predator.eat(herbivore):
                    herbivores.remove(herbivore)
                    herbivores_count -= 1

            new_predator = predator.reproduce()
            if new_predator is not None:
                predators.append(new_predator)
                predators_count += 1

            if predator.energy <= 50:
                predators.remove(predator)
                predators_count -= 1

        new_herbivores = []
        new_predators = []

        for h1 in herbivores:
            for h2 in herbivores:
                if h1 != h2 and h1.distance_to(h2) < MATING_DISTANCE:
                    offspring = h1.mate(h2)
                    if offspring:
                        new_herbivores.append(offspring)
                        herbivores_count += 1

        for p1 in predators:
            for p2 in predators:
                if p1 != p2 and p1.distance_to(p2) < MATING_DISTANCE:
                    offspring = p1.mate(p2)
                    if offspring:
                        new_predators.append(offspring)
                        predators_count += 1
        
        plant_angles = [random.uniform(0, 2 * math.pi) for _ in range(int(plants_count + 1000))]
        herbivore_angles = [random.uniform(0, 2 * math.pi) for _ in range(int(herbivores_count + 1000))]
        predator_angles = [random.uniform(0, 2 * math.pi) for _ in range(int(predators_count + 1000))]

        if 390 <= image1_x <= SCREEN_WIDTH and SCREEN_HEIGHT - 590 <= image1_y <= SCREEN_HEIGHT - 10:
            tornado_plants(plants, image1_x, image1_y, radius, speed, attraction_speed)
            tornado_herbivores(herbivores, image1_x, image1_y, radius, speed, attraction_speed)
            tornado_predators(predators, image1_x, image1_y, radius, speed, attraction_speed)

    elif button_text2 == "Finish":
        plants = [Plant(random.randint(390, SCREEN_WIDTH), random.randint(SCREEN_HEIGHT - 590, 590), PLANT_ENERGY) for _ in range(int(initial_plants))]
        herbivores = [Herbivore(random.randint(390, SCREEN_WIDTH), random.randint(SCREEN_HEIGHT - 590, 590), HERBIVORE_ENERGY) for _ in range(int(initial_herbivores))]
        predators = [Predator(random.randint(390, SCREEN_WIDTH), random.randint(SCREEN_HEIGHT - 590, 590), PREDATOR_ENERGY) for _ in range(int(initial_predators))]
        simulation_started = False
        button_text2 = "Begin"

    if active:
        color = color_active
    else:
        color = color_passive
    
    if active2:
        color2 = color_active2
    else:
        color2 = color_passive2
		
    if active3:
        color3 = color_active3
    else:
        color3 = color_passive3

    if active4:
        color4 = color_active4
    else:
        color4 = color_passive4

    draw_text_box(screen, base_font, initial_plants, color, input_rect) #plants
    draw_text_box(screen, base_font, initial_herbivores, color2, input_rect2) #herbivores
    draw_text_box(screen, base_font, initial_predators, color3, input_rect3) #predators
    draw_text_box(screen, base_font, temperature, color4, input_rect4) #temperature

    if (dragging1 and area_x <= image1_x <= area_x + area_w - image1.get_width() and area_y <= image1_y <= area_y + area_h - image1.get_height()) or \
       (dragging2 and area_x <= image2_x <= area_x + area_w - image2.get_width() and area_y <= image2_y <= area_y + area_h - image2.get_height()):
        screen.blit(text, (area_x + (area_w - text.get_width()) // 2, area_y + (area_h - text.get_height()) // 2))

    plants_alive = font.render(str(plants_count), True, PLANT_COLOR)
    screen.blit(plants_alive, (350, 300))
    herbivores_alive = font.render(str(herbivores_count), True, HERBIVORE_COLOR)
    screen.blit(herbivores_alive, (350, 400))
    predators_alive = font.render(str(predators_count), True, PREDATOR_COLOR)
    screen.blit(predators_alive, (350, 500))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
