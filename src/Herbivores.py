import pygame
import random
import math
from variables import *

class Herbivore:
    def __init__(self, x, y, energy, color=HERBIVORE_COLOR):
        self.x = x
        self.y = y
        self.energy = energy
        self.angle = random.uniform(0, 2 * math.pi)
        self.gender = random.choice(["male", "female"])
        self.color = self.adjust_color_by_gender(color)

    def adjust_color_by_gender(self, color):
        if self.gender == "male":
            return (30,144,255)  # Darker shade
        else:
            return (173, 216, 230)  # Lighter shade

    def draw(self, screen):
        MALE_SIZE = 9
        FEMALE_SIZE = 6

        size = MALE_SIZE if self.gender == 'male' else FEMALE_SIZE

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

    def move(self, HERBIVORE_SPEED, ENERGY_DEPLETION_FACTOR):
        dx = HERBIVORE_SPEED * math.cos(self.angle)
        dy = HERBIVORE_SPEED * math.sin(self.angle)
        new_x = self.x + dx
        new_y = self.y + dy
        if new_x > SCREEN_WIDTH:
            new_x = SCREEN_WIDTH
        elif new_x < 390:
            new_x = 390
        if new_y > SCREEN_HEIGHT - 10:
            new_y = SCREEN_HEIGHT - 10
        elif new_y < SCREEN_HEIGHT - 590:
            new_y = SCREEN_HEIGHT - 590
        self.x = new_x
        self.y = new_y
        self.energy *= ENERGY_DEPLETION_FACTOR 

    def turn(self):
        self.angle += random.uniform(-math.pi / 16, math.pi / 16)

    def eat(self, plant):
        distance = math.sqrt((self.x - plant.x) ** 2 + (self.y - plant.y) ** 2)
        if distance <= 15:
            self.energy += plant.energy
            return True
        else:
            return False
    
    def move_towards_food(self, plants):
        nearest_plant = None
        min_distance = float('inf')

        for plant in plants:
            distance = math.sqrt((self.x - plant.x) ** 2 + (self.y - plant.y) ** 2)
            if distance < min_distance and distance <= HERBIVORE_SIGHT_RANGE:
                min_distance = distance
                nearest_plant = plant

        if nearest_plant is not None:
            self.angle = math.atan2(nearest_plant.y - self.y, nearest_plant.x - self.x)
        else:
            self.turn()

    def reproduce(self):
        if self.gender == "female":
            if self.energy >= HERBIVORE_FOOD_THRESHOLD + REPRODUCTION_ENERGY_COST:
                self.energy -= REPRODUCTION_ENERGY_COST
                return Herbivore(self.x, self.y, self.energy / 2)
            else:
                return None

