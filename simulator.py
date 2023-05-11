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
HERBIVORE_COLOR = (0, 0, 255) # Red
PREDATOR_COLOR = (255, 0, 0) # Blue
HERBIVORE_SPEED = 3
HERBIVORE_ENERGY = 50
HERBIVORE_SIGHT_RANGE = 100
HERBIVORE_FOOD_THRESHOLD = 50
PREDATOR_SPEED = 1
PREDATOR_ENERGY = 200
PREDATOR_SIGHT_RANGE = 150
PREDATOR_FOOD_THRESHOLD = 100
PLANT_ENERGY = 100
PLANT_GROWTH_RATE = 0.1
HERBIVORE_ENERGY_COST = 0.7
PREDATOR_ENERGY_COST = 0.05  
ENERGY_DEPLETION_FACTOR = 1
REPRODUCTION_ENERGY_COST = 200
INITIAL_PLANTS = 30
INITIAL_HERBIVORES = 5
INITIAL_PREDATORS = 1
PLANT_REPRODUCTION_RATE = 0.01

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Ecosystem Simulator")
clock = pygame.time.Clock()


class Plant:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy

    def draw(self, screen):
        radius = max(1, min(3, int(self.energy / 20)))
        pygame.gfxdraw.filled_circle(screen, self.x, self.y, radius, PLANT_COLOR)
        pygame.gfxdraw.aacircle(screen, self.x, self.y, radius, PLANT_COLOR)

    def generate_new_plant(plant):
        new_x = plant.x + random.randint(-200, 200)
        new_y = plant.y + random.randint(-200, 200)
        if 400 <= new_x <= SCREEN_WIDTH and 0 <= new_y <= SCREEN_HEIGHT - 250:
            return Plant(new_x, new_y, plant.energy / 200)
        else:
            return None

    def grow(self):
        self.energy = min(self.energy + PLANT_GROWTH_RATE * self.energy, 100)
            
class Herbivore:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy
        self.direction = random.uniform(0, 2 * math.pi)

    def draw(self, screen):
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), 6, HERBIVORE_COLOR)
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), 6, HERBIVORE_COLOR)

    def move(self):
        dx = HERBIVORE_SPEED * math.cos(self.direction)
        dy = HERBIVORE_SPEED * math.sin(self.direction)
        new_x = self.x + dx
        new_y = self.y + dy
        if new_x > SCREEN_WIDTH:
            new_x = SCREEN_WIDTH
        elif new_x < 400:
            new_x = 400
        if new_y > SCREEN_HEIGHT - 250:
            new_y = SCREEN_HEIGHT - 250
        elif new_y < 0:
            new_y = 0
        self.x = new_x
        self.y = new_y
        self.energy *= ENERGY_DEPLETION_FACTOR 

    def turn(self):
        self.direction += random.uniform(-math.pi / 16, math.pi / 16)

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
            self.direction = math.atan2(nearest_plant.y - self.y, nearest_plant.x - self.x)
        else:
            self.turn()

    def reproduce(self):
        if self.energy >= HERBIVORE_FOOD_THRESHOLD + REPRODUCTION_ENERGY_COST:
            self.energy -= REPRODUCTION_ENERGY_COST
            return Herbivore(self.x, self.y, self.energy / 2)
        else:
            return None

class Predator:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy
        self.direction = random.uniform(0, 2 * math.pi)

    def draw(self, screen):
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), 10, PREDATOR_COLOR)
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), 10, PREDATOR_COLOR)

    def move(self):
        dx = PREDATOR_SPEED * math.cos(self.direction)
        dy = PREDATOR_SPEED * math.sin(self.direction)
        new_x = self.x + dx
        new_y = self.y + dy
        if new_x > SCREEN_WIDTH:
            new_x = SCREEN_WIDTH
        elif new_x < 400:
            new_x = 400
        if new_y > SCREEN_HEIGHT - 250:
            new_y = SCREEN_HEIGHT - 250
        elif new_y < 0:
            new_y = 0
        self.x = new_x
        self.y = new_y
        self.energy *= ENERGY_DEPLETION_FACTOR  
    
    def turn(self):
        self.direction += random.uniform(-math.pi / 16, math.pi / 16)

    def eat(self, herbivore):
        distance = math.sqrt((self.x - herbivore.x) ** 2 + (self.y - herbivore.y) ** 2)
        if distance <= 20:
            self.energy += herbivore.energy
            return True
        else:
            return False

    def move_towards_food(self, herbivores):
        nearest_herbivore = None
        min_distance = float('inf')

        for herbivore in herbivores:
            distance = math.sqrt((self.x - herbivore.x) ** 2 + (self.y - herbivore.y) ** 2)
            if distance < min_distance and distance <= PREDATOR_SIGHT_RANGE:
                min_distance = distance
                nearest_herbivore = herbivore

        if nearest_herbivore is not None:
            self.direction = math.atan2(nearest_herbivore.y - self.y, nearest_herbivore.x - self.x)
        else:
            self.turn()

    def reproduce(self):
        if self.energy >= PREDATOR_FOOD_THRESHOLD + REPRODUCTION_ENERGY_COST:
            self.energy -= REPRODUCTION_ENERGY_COST
            return Predator(self.x, self.y, self.energy / 2)
        else:
            return None
    
plants = [Plant(random.randint(400, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT - 250), PLANT_ENERGY) for _ in range(INITIAL_PLANTS)]
herbivores = [Herbivore(random.randint(400, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT - 250), HERBIVORE_ENERGY) for _ in range(INITIAL_HERBIVORES)]
predators = [Predator(random.randint(400, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT - 250), PREDATOR_ENERGY) for _ in range(INITIAL_PREDATORS)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for plant in plants:
        plant.grow()
        
        if random.random() < PLANT_REPRODUCTION_RATE / 5:
            new_plant = plant.generate_new_plant()
            if new_plant is not None:
                plants.append(new_plant)


    for herbivore in herbivores:
        herbivore.move_towards_food(plants)
        herbivore.move()
        herbivore.energy -= HERBIVORE_ENERGY_COST

        for plant in plants:
            if herbivore.eat(plant):
                plants.remove(plant)

        new_herbivore = herbivore.reproduce()
        if new_herbivore is not None:
            herbivores.append(new_herbivore)

        if herbivore.energy <= 10:
            herbivores.remove(herbivore)

    for predator in predators:
        predator.move_towards_food(herbivores)
        predator.move()
        predator.energy -= PREDATOR_ENERGY_COST

        for herbivore in herbivores:
            if predator.eat(herbivore):
                herbivores.remove(herbivore)

        new_predator = predator.reproduce()
        if new_predator is not None:
            predators.append(new_predator)

        if predator.energy <= 10:
            predators.remove(predator)

    screen.fill(BACKGROUND_COLOR)

    for plant in plants:
        plant.draw(screen)

    for herbivore in herbivores:
        herbivore.draw(screen)

    for predator in predators:
        predator.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
