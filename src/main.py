import pygame
import random
import math
import sys
from variables import *
from Plants import *
from Herbivores import *
from Predators import *
from Graphs import *
from Tornado import *

pygame.init()

base_font = pygame.font.Font(None, 32)
pygame.font.init()
font = pygame.font.Font(None, 36)
text = font.render("Hold here", True, (0, 0, 0))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Ecosystem Simulator")
clock = pygame.time.Clock()
image1 = pygame.image.load("tornado.png")

running = True
dragging1 = False
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

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging1:
                if area_x <= image1_x <= area_x + area_w - image1.get_width() and area_y <= image1_y <= area_y + area_h - image1.get_height():
                    image1_x, image1_y = start_x1, start_y1
                    image1 = pygame.image.load("tornado.png")
                    print("Tornado")
                else:
                    image1_x, image1_y = start_x1, start_y1
                dragging1 = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging1:
                mouse_x, mouse_y = event.pos
                image1_x = mouse_x - mouse_offset_x1
                image1_y = mouse_y - mouse_offset_y1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if draw == 1:
                if button_rect.collidepoint(event.pos):
                    simulation_running = not simulation_running
                    button_text = "Start" if button_text == "Pause" else "Pause"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect2.collidepoint(event.pos):
                simulation_started = not simulation_started
                button_text2 = "Drew" if button_text2 == "Draw" else "Draw"
                draw = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect3.collidepoint(event.pos):
                plot_results(herbivores_counts, predators_counts, plants_counts)
                pygame.quit()

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
            
        if event.type == pygame.MOUSEBUTTONDOWN: #humidity
            if input_rect5.collidepoint(event.pos):
                active5 = True
            else:
                active5 = False

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
                if active5:
                    humidity = humidity[:-1]
            else:
                if active:
                    initial_plants += event.unicode
                if active2:
                    initial_herbivores += event.unicode
                if active3:
                    initial_predators += event.unicode
                if active4:
                    temperature += event.unicode
                if active5:
                    humidity += event.unicode
            
    screen.fill(BACKGROUND_COLOR)
    screen.blit(image1, (image1_x, image1_y))
    draw_button(screen, button_rect, button_text)
    draw_button(screen, button_rect2, button_text2)
    draw_button(screen, button_rect3, button_text3)
    pygame.gfxdraw.rectangle(screen, pygame.Rect(389, SCREEN_HEIGHT - 591, SCREEN_WIDTH, 583), BORDER_COLOR) #simulation border
            
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

        if int(humidity) > 100 or int(humidity) < 0:
            print("Invalid humidity value")
        if 90 <= int(humidity) <= 100:
            PLANT_COLOR = (89,96,24)
            PLANT_COLOR2 = (0, 0, 0)
        else:
            PLANT_COLOR = (0, 255, 0)
            PLANT_COLOR2 = (128, 0, 128)

        for plant in plants:
            plant.grow()
        
            if random.random() < PLANT_REPRODUCTION_RATE / 5:
                new_plant = plant.generate_new_plant()
                if new_plant is not None:
                    plants.append(new_plant)
                    plants_count += 1
                    
        for herbivore in herbivores:
            if not 90 <= int(humidity) <= 100:
                herbivore.move_towards_food(plants)
            herbivore.move(HERBIVORE_SPEED, ENERGY_DEPLETION_FACTOR)
            herbivore.energy -= HERBIVORE_ENERGY_COST

            for plant in plants:
                if not 90 <= int(humidity) <= 100:
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
            if not 90 <= int(humidity) <= 100:
                predator.move_towards_food(herbivores)
            predator.move(PREDATOR_SPEED, ENERGY_DEPLETION_FACTOR)
            predator.energy -= PREDATOR_ENERGY_COST

            for herbivore in herbivores:
                if not 90 <= int(humidity) <= 100:
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
            tornado_plants(plants, image1_x, image1_y, radius, speed, attraction_speed, plant_angles)
            tornado_herbivores(herbivores, image1_x, image1_y, radius, speed, attraction_speed, herbivore_angles)
            tornado_predators(predators, image1_x, image1_y, radius, speed, attraction_speed, predator_angles)
        
        herbivores_counts.append(herbivores_count)
        predators_counts.append(predators_count)
        plants_counts.append(plants_count)

    if button_text2 == "Drew":
        plants = [Plant(random.randint(390, SCREEN_WIDTH), random.randint(SCREEN_HEIGHT - 590, 590), PLANT_ENERGY) for _ in range(int(initial_plants))]
        herbivores = [Herbivore(random.randint(390, SCREEN_WIDTH), random.randint(SCREEN_HEIGHT - 590, 590), HERBIVORE_ENERGY) for _ in range(int(initial_herbivores))]
        predators = [Predator(random.randint(390, SCREEN_WIDTH), random.randint(SCREEN_HEIGHT - 590, 590), PREDATOR_ENERGY) for _ in range(int(initial_predators))]
        simulation_started = False
        button_text2 = "Draw"
        plants_count = int(initial_plants)
        herbivores_count = int(initial_herbivores)
        predators_count = int(initial_predators)

    if not simulation_started:
        if button_text2 == "Draw":
            for plant in plants:
                plant.draw(screen, PLANT_COLOR, PLANT_COLOR2)

            for herbivore in herbivores:
                herbivore.draw(screen)
                
            for predator in predators:
                predator.draw(screen)

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
        
    if active5:
        color5 = color_active5
    else:
        color5 = color_passive5

    draw_text_box(screen, base_font, initial_plants, color, input_rect) #plants
    draw_text_box(screen, base_font, initial_herbivores, color2, input_rect2) #herbivores
    draw_text_box(screen, base_font, initial_predators, color3, input_rect3) #predators
    draw_text_box(screen, base_font, temperature, color4, input_rect4) #temperature
    draw_text_box(screen, base_font, humidity, color5, input_rect5) #humidity

    if (dragging1 and area_x <= image1_x <= area_x + area_w - image1.get_width() and area_y <= image1_y <= area_y + area_h - image1.get_height()):
        screen.blit(text, (area_x + (area_w - text.get_width()) // 2, area_y + (area_h - text.get_height()) // 2))

    inscription = font.render("Plants:", True, color_passive)
    screen.blit(inscription, (10, 120))
    inscription = font.render("Herbivores:", True, color_passive2)
    screen.blit(inscription, (10, 190))
    inscription = font.render("Predators:", True, color_passive3)
    screen.blit(inscription, (10, 260))
    inscription = font.render("Temperature:", True, color_passive4)
    screen.blit(inscription, (10, 330))
    inscription = font.render("Humidity:", True, color_passive5)
    screen.blit(inscription, (10, 400))

    plants_alive = font.render(str(plants_count), True, PLANT_COLOR)
    screen.blit(plants_alive, (350, 150))
    herbivores_alive = font.render(str(herbivores_count), True, HERBIVORE_COLOR)
    screen.blit(herbivores_alive, (350, 220))
    predators_alive = font.render(str(predators_count), True, PREDATOR_COLOR)
    screen.blit(predators_alive, (350, 290))

    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()

