import pygame
import pygame.gfxdraw
import random
import math
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BORDER_COLOR = (0, 0, 0) # Black
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
base_font = pygame.font.Font(None, 32)
initial_plants = '0'
initial_herbivores = '0'
initial_predators = '0'
PLANT_REPRODUCTION_RATE = 0.01


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Ecosystem Simulator")
clock = pygame.time.Clock()

def draw_button(screen, button_rect, text):
    pygame.draw.rect(screen, (100, 100, 100), button_rect, 0)
    pygame.draw.rect(screen, (200, 200, 200), button_rect, 1)

    font = pygame.font.Font(None, 24)
    label = font.render(text, 1, (255, 255, 255))
    screen.blit(label, (button_rect.x + button_rect.width // 2 - label.get_width() // 2,
                        button_rect.y + button_rect.height // 2 - label.get_height() // 2))

def draw_button2(screen, button_rect, text):
    pygame.draw.rect(screen, (100, 100, 100), button_rect, 0)
    pygame.draw.rect(screen, (200, 200, 200), button_rect, 1)

    font = pygame.font.Font(None, 24)
    label = font.render(text, 1, (255, 255, 255))
    screen.blit(label, (button_rect.x + button_rect.width // 2 - label.get_width() // 2,
                        button_rect.y + button_rect.height // 2 - label.get_height() // 2))

button_width, button_height = 100, 40
button_x, button_y = 110, 10
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
simulation_running = True
button_text = "Start"
button_x2, button_y2 = 10, 10
button_rect2 = pygame.Rect(button_x2, button_y2, button_width, button_height)
simulation_started = True
button_text2 = "Finish"

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
    
plants = [Plant(random.randint(400, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT - 250), PLANT_ENERGY) for _ in range(int(initial_plants))]
herbivores = [Herbivore(random.randint(400, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT - 250), HERBIVORE_ENERGY) for _ in range(int(initial_herbivores))]
predators = [Predator(random.randint(400, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT - 250), PREDATOR_ENERGY) for _ in range(int(initial_predators))]

input_rect = pygame.Rect(200, 200, 140, 32)
color_active = pygame.Color(144, 238, 144)
color_passive = pygame.Color(69,139,0)
color = color_passive
active = False

input_rect2 = pygame.Rect(200, 250, 140, 32)
color_active2 = pygame.Color(173, 216, 230)
color_passive2 = pygame.Color(30,144,255)
color2 = color_passive2
active2 = False

input_rect3 = pygame.Rect(200, 300, 140, 32)
color_active3 = pygame.Color(250, 128, 114)
color_passive3 = pygame.Color(128, 0, 0)
color3 = color_passive3
active3 = False

running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            sys.exit()

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


        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:
                if active:
                    initial_plants = initial_plants[:-1]
                if active2:
                    initial_herbivores = initial_herbivores[:-1]
                if active3:
                    initial_predators = initial_predators[:-1]
            else:
                if active:
                    initial_plants += event.unicode
                if active2:
                    initial_herbivores += event.unicode
                if active3:
                    initial_predators += event.unicode
        

    if not simulation_running:
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
    draw_button(screen, button_rect, button_text)
    draw_button2(screen, button_rect2, button_text2)
    pygame.gfxdraw.rectangle(screen, pygame.Rect(390, SCREEN_HEIGHT - 600, SCREEN_WIDTH, 360), BORDER_COLOR) #simulation border

    if not simulation_started:
        if button_text2 == "Begin":
            for plant in plants:
                plant.draw(screen)

            for herbivore in herbivores:
                herbivore.draw(screen)

            for predator in predators:
                predator.draw(screen)
    elif button_text2 == "Finish":
        plants = [Plant(random.randint(400, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT - 250), PLANT_ENERGY) for _ in range(int(initial_plants))]
        herbivores = [Herbivore(random.randint(400, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT - 250), HERBIVORE_ENERGY) for _ in range(int(initial_herbivores))]
        predators = [Predator(random.randint(400, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT - 250), PREDATOR_ENERGY) for _ in range(int(initial_predators))]
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

    pygame.draw.rect(screen, color, input_rect)
    text_surface = base_font.render(initial_plants, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    input_rect.w = max(100, text_surface.get_width()+10)

    pygame.draw.rect(screen, color2, input_rect2)
    text_surface = base_font.render(initial_herbivores, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect2.x+5, input_rect2.y+5))
    input_rect2.w = max(100, text_surface.get_width()+10)

    pygame.draw.rect(screen, color3, input_rect3)
    text_surface = base_font.render(initial_predators, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect3.x+5, input_rect3.y+5))
    input_rect3.w = max(100, text_surface.get_width()+10)
	
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
