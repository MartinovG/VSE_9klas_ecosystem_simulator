import math
from variables import *
import random
from Plants import *
from Herbivores import *
from Predators import *

death_probability = 0.1

def tornado_plants(plants, mouse_x, mouse_y, radius, speed, attraction_speed, plant_angles):
    for i, plant in enumerate(plants):
        dx = (mouse_x - plant.x)
        dy = (mouse_y - plant.y)
        distance = math.sqrt(dx**2 + dy**2)
        angle = plant_angles[i]

        if distance <= radius:
            if random.random() < death_probability:
                plants.remove(plant)
            new_angle = angle + speed
            new_distance = distance - attraction_speed
            new_x = mouse_x + math.cos(new_angle) * new_distance
            new_y = mouse_y + math.sin(new_angle) * new_distance

            new_x = max(390, min(new_x, SCREEN_WIDTH))
            new_y = max(SCREEN_HEIGHT - 590, min(new_y, 590))

            plant.x, plant.y = new_x, new_y
            plant_angles[i] = new_angle

def tornado_herbivores(herbivores, mouse_x, mouse_y, radius, speed, attraction_speed, herbivore_angles):
    for i, herbivore in enumerate(herbivores):
        dx = (mouse_x - herbivore.x)
        dy = (mouse_y - herbivore.y)
        distance = math.sqrt(dx**2 + dy**2)
        angle = herbivore_angles[i]

        if distance <= radius:
            if random.random() < death_probability:
                herbivores.remove(herbivore)
            new_angle = angle + speed
            new_distance = distance - attraction_speed
            new_x = mouse_x + math.cos(new_angle) * new_distance
            new_y = mouse_y + math.sin(new_angle) * new_distance

            new_x = max(390, min(new_x, SCREEN_WIDTH))
            new_y = max(SCREEN_HEIGHT - 590, min(new_y, 590))

            herbivore.x, herbivore.y = new_x, new_y
            herbivore_angles[i] = new_angle

def tornado_predators(predators, mouse_x, mouse_y, radius, speed, attraction_speed, predator_angles):
    for i, predator in enumerate(predators):
        dx = (mouse_x - predator.x)
        dy = (mouse_y - predator.y)
        distance = math.sqrt(dx**2 + dy**2)
        angle = predator_angles[i]

        if distance <= radius:
            if random.random() < death_probability:
                predators.remove(predator)
            new_angle = angle + speed
            new_distance = distance - attraction_speed
            new_x = mouse_x + math.cos(new_angle) * new_distance
            new_y = mouse_y + math.sin(new_angle) * new_distance

            new_x = max(390, min(new_x, SCREEN_WIDTH))
            new_y = max(SCREEN_HEIGHT - 590, min(new_y, 590))

            predator.x, predator.y = new_x, new_y
            predator_angles[i] = new_angle
   