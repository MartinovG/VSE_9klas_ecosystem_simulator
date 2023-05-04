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
HERBIVORE_SPEED = 2
HERBIVORE_ENERGY = 50
HERBIVORE_SIGHT_RANGE = 100
HERBIVORE_FOOD_THRESHOLD = 50
PREDATOR_SPEED = 3
PREDATOR_ENERGY = 200
PREDATOR_SIGHT_RANGE = 150
PREDATOR_FOOD_THRESHOLD = 100
PLANT_ENERGY = 100
PLANT_GROWTH_RATE = 0.1

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Ecosystem Simulator")
clock = pygame.time.Clock()

class Plant:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy

    def draw(self, screen):
        radius = max(2, min(5, int(self.energy / 20)))
        pygame.gfxdraw.filled_circle(screen, self.x, self.y, radius, PLANT_COLOR)
        pygame.gfxdraw.aacircle(screen, self.x, self.y, radius, PLANT_COLOR)

    def grow(self):
        self.energy = min(self.energy + PLANT_GROWTH_RATE * self.energy, 100)

class Herbivore:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy
        self.direction = random.uniform(0, 2 * math.pi)

    def draw(self, screen):
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), 10, HERBIVORE_COLOR)
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), 10, HERBIVORE_COLOR)

    def move(self):
        dx = HERBIVORE_SPEED * math.cos(self.direction)
        dy = HERBIVORE_SPEED * math.sin(self.direction)
        new_x = self.x + dx
        new_y = self.y + dy
        if new_x > SCREEN_WIDTH:
            new_x = SCREEN_WIDTH
        elif new_x < 0:
            new_x = 0
        if new_y > SCREEN_HEIGHT:
            new_y = SCREEN_HEIGHT
        elif new_y < 0:
            new_y = 0
        self.x = new_x
        self.y = new_y

    def turn(self):
        self.direction += random.uniform(-math.pi / 16, math.pi / 16)

    def eat(self, plant):
        distance = math.sqrt((self.x - plant.x) ** 2 + (self.y - plant.y) ** 2)
        if distance <= 15:
            self.energy += plant.energy
            return True
        else:
            return False

    def reproduce(self):
        if self.energy >= HERBIVORE_FOOD_THRESHOLD:
            self.energy /= 4
            return Herbivore(self.x, self.y, self.energy)
        else:
            return None

class Predator:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy
        self.direction = random.uniform(0, 2 * math.pi)

    def draw(self, screen):
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), 15, PREDATOR_COLOR)
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), 15, PREDATOR_COLOR)

    def move(self):
        dx = PREDATOR_SPEED * math.cos(self.direction)
        dy = PREDATOR_SPEED * math.sin(self.direction)
        new_x = self.x + dx
        new_y = self.y + dy
        if new_x > SCREEN_WIDTH:
            new_x = SCREEN_WIDTH
        elif new_x < 0:
            new_x = 0
        if new_y > SCREEN_HEIGHT:
            new_y = SCREEN_HEIGHT
        elif new_y < 0:
            new_y = 0
        self.x = new_x
        self.y = new_y
    
    def turn(self):
        self.direction += random.uniform(-math.pi / 16, math.pi / 16)

    def eat(self, herbivore):
        distance = math.sqrt((self.x - herbivore.x) ** 2 + (self.y - herbivore.y) ** 2)
        if distance <= 20:
            self.energy += herbivore.energy
            return True
        else:
            return False

    def reproduce(self):
        if self.energy >= PREDATOR_FOOD_THRESHOLD:
            self.energy /= 8
            return Predator(self.x, self.y, self.energy)
        else:
            return None

plants = [Plant(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), PLANT_ENERGY) for _ in range(10)]
herbivores = [Herbivore(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), HERBIVORE_ENERGY) for _ in range(5)]
predators = [Predator(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), PREDATOR_ENERGY) for _ in range(3)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for plant in plants:
        plant.grow()

    for herbivore in herbivores:
        herbivore.move()
        herbivore.turn()

        for plant in plants:
            if herbivore.eat(plant):
                plants.remove(plant)

        new_herbivore = herbivore.reproduce()
        if new_herbivore is not None:
            herbivores.append(new_herbivore)

        if herbivore.energy <= 10:
            herbivores.remove(herbivore)

    for predator in predators:
        predator.move()
        predator.turn()

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
