import pygame
import pygame.gfxdraw
import random
import math
import sys
from variables import *

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BORDER_COLOR = (0, 0, 0) # Black
BACKGROUND_COLOR = ('#FFFFFF') # White
PLANT_COLOR = (0, 255, 0) # Green
HERBIVORE_COLOR = (0, 0, 255) # Red
PREDATOR_COLOR = (255, 0, 0) # Blue
PLANT_COLOR2 = (128, 0, 128) # Purple
HERBIVORE_SPEED = 1.0
HERBIVORE_ENERGY = 100
HERBIVORE_SIGHT_RANGE = 100
HERBIVORE_FOOD_THRESHOLD = 50
PREDATOR_SPEED = 0.5
PREDATOR_ENERGY = 150
PREDATOR_SIGHT_RANGE = 50
PREDATOR_FOOD_THRESHOLD = 50
PLANT_ENERGY = 100
PLANT_GROWTH_RATE = 0.01
HERBIVORE_ENERGY_COST = 0.005
PREDATOR_ENERGY_COST = 0.007 
ENERGY_DEPLETION_FACTOR = 1
REPRODUCTION_ENERGY_COST = 200
base_font = pygame.font.Font(None, 32)
initial_plants = '250'
initial_herbivores = '50'
initial_predators = '10'
temperature = '0'
PLANT_REPRODUCTION_RATE = 0.01
MATING_ENERGY_THRESHOLD = 15000  
OFFSPRING_ENERGY_FACTOR = 0.2  
MATING_DISTANCE = 2  
#DARK_GREEN = (0, 100, 0)
#BLUE = (0, 0, 255)  
start_x1 = SCREEN_WIDTH - 500
start_y1 = SCREEN_HEIGHT - 500 
start_x2 = SCREEN_WIDTH - 500 
start_y2 = SCREEN_HEIGHT - 400
image1_x, image1_y = start_x1, start_y1
image2_x, image2_y = start_x2, start_y2
area_x, area_y, area_w, area_h = 390, SCREEN_HEIGHT - 590, SCREEN_WIDTH - 390, 590
pygame.font.init()
font = pygame.font.Font(None, 36)
text = font.render("Drop here", True, (0, 0, 0))
radius = 200  
speed = 0.012  
attraction_speed = 0.05 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Ecosystem Simulator")
clock = pygame.time.Clock()
image1 = pygame.image.load("tornado.png")
image2 = pygame.image.load("fire.png")

angles = [random.uniform(0, 2 * math.pi) for _ in range(int(initial_plants))]

'''def generate_perlin_noise(width, height, scale):
    noise_array = []
    for y in range(height):
        row = []
        for x in range(width):
            value = noise.pnoise2(x/scale, y/scale, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0)
            row.append(value)
        noise_array.append(row)
    return noise_array'''

'''def draw_pond(noise_array, scale, threshold):
    for y in range(len(noise_array)):
        for x in range(len(noise_array[y])):
            if noise_array[y][x] < threshold:
                pond_x = x * scale + 390  # Adjust x-coordinate based on the starting boundary
                pond_y = y * scale + (SCREEN_HEIGHT - 590)  # Adjust y-coordinate based on the starting and ending boundaries
                if pond_y < 590:  # Check if the y-coordinate is within the ending boundary
                    pygame.draw.rect(screen, DARK_GREEN, (pond_x, pond_y, scale, scale))
            else:
                pond_x = x * scale + 390  # Adjust x-coordinate based on the starting boundary
                pond_y = y * scale + (SCREEN_HEIGHT - 590)  # Adjust y-coordinate based on the starting and ending boundaries
                if pond_y < 590:  # Check if the y-coordinate is within the ending boundary
                    pygame.draw.rect(screen, BLUE, (pond_x, pond_y, scale, scale))'''

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

def tornado(plants, mouse_x, mouse_y, radius, speed, attraction_speed):
    for i, plant in enumerate(plants):
        dx = (mouse_x - plant.x)
        dy = (mouse_y - plant.y)
        distance = math.sqrt(dx**2 + dy**2)
        angle = angles[i]

        if distance <= radius:
            new_angle = angle + speed
            new_distance = distance - attraction_speed
            new_x = mouse_x + math.cos(new_angle) * new_distance
            new_y = mouse_y + math.sin(new_angle) * new_distance
            plant.x, plant.y= new_x, new_y
            angles[i] = new_angle

class Plant:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy

    def draw(self, screen):
        radius = max(2, min(4, int(self.energy / 20)))
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), radius, PLANT_COLOR)
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), radius, PLANT_COLOR)
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), radius - 2 , PLANT_COLOR2)
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), radius - 2, PLANT_COLOR2)

    def generate_new_plant(plant):
        new_x = plant.x + random.randint(-200, 200)
        new_y = plant.y + random.randint(-200, 200)
        if 390 <= new_x <= SCREEN_WIDTH and SCREEN_HEIGHT - 590 <= new_y <= SCREEN_HEIGHT - 10:
            return Plant(new_x, new_y, plant.energy / 200)
        else:
            return None

    def grow(self):
        self.energy = min(self.energy + PLANT_GROWTH_RATE * self.energy, 100)
            
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

    def move(self):
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
        if self.energy >= HERBIVORE_FOOD_THRESHOLD + REPRODUCTION_ENERGY_COST:
            self.energy -= REPRODUCTION_ENERGY_COST
            return Herbivore(self.x, self.y, self.energy / 2)
        else:
            return None

    def mate(self, other):
        if (self.gender != other.gender) and (self.energy > MATING_ENERGY_THRESHOLD) and (other.energy > MATING_ENERGY_THRESHOLD):
            offspring_energy = self.energy * OFFSPRING_ENERGY_FACTOR + other.energy * OFFSPRING_ENERGY_FACTOR
            offspring_color = tuple((c1 + c2) // 2 for c1, c2 in zip(self.color, other.color))
            offspring = Herbivore(self.x, self.y, offspring_energy, color=offspring_color)
            self.energy *= (1 - OFFSPRING_ENERGY_FACTOR)
            other.energy *= (1 - OFFSPRING_ENERGY_FACTOR)
            return offspring
        return None
    
    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)

class Predator:
    def __init__(self, x, y, energy, color=PREDATOR_COLOR):
        self.x = x
        self.y = y
        self.energy = energy
        self.angle = random.uniform(0, 2 * math.pi)
        self.gender = random.choice(["male", "female"])
        self.color = self.adjust_color_by_gender(color)

    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)

    def adjust_color_by_gender(self, color):
        if self.gender == "male":
            return (128, 0, 0)  # Darker shade
        else:
            return (250, 128, 114)  # Lighter shade

    def draw(self, screen):
        MALE_SIZE = 10
        FEMALE_SIZE = 7

        size = MALE_SIZE if self.gender == 'male' else FEMALE_SIZE

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

    def move(self):
        dx = PREDATOR_SPEED * math.cos(self.angle)
        dy = PREDATOR_SPEED * math.sin(self.angle)
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
        elif new_y < 0:
            new_y = 0
        self.x = new_x
        self.y = new_y
        self.energy *= ENERGY_DEPLETION_FACTOR  
    
    def turn(self):
        self.angle += random.uniform(-math.pi / 16, math.pi / 16)

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
            self.angle = math.atan2(nearest_herbivore.y - self.y, nearest_herbivore.x - self.x)
        else:
            self.turn()

    def reproduce(self):
        if self.energy >= PREDATOR_FOOD_THRESHOLD + REPRODUCTION_ENERGY_COST:
            self.energy -= REPRODUCTION_ENERGY_COST
            return Predator(self.x, self.y, self.energy / 2)
        else:
            return None
        
    def mate(self, other):
        if (self.gender != other.gender) and (self.energy > MATING_ENERGY_THRESHOLD) and (other.energy > MATING_ENERGY_THRESHOLD):
            offspring_energy = self.energy * OFFSPRING_ENERGY_FACTOR + other.energy * OFFSPRING_ENERGY_FACTOR
            offspring_color = tuple((c1 + c2) // 2 for c1, c2 in zip(self.color, other.color))
            offspring = Predator(self.x, self.y, offspring_energy, color=offspring_color)
            self.energy *= (1 - OFFSPRING_ENERGY_FACTOR)
            other.energy *= (1 - OFFSPRING_ENERGY_FACTOR)
            return offspring
        return None    
    
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

    tornado(plants, image1_x, image1_y, radius, speed, attraction_speed)

    screen.fill(BACKGROUND_COLOR)
    screen.blit(image1, (image1_x, image1_y))
    screen.blit(image2, (image2_x, image2_y))
    #noise_array = generate_perlin_noise(SCREEN_WIDTH // 7, SCREEN_HEIGHT // 5, scale=15)
    #draw_pond(noise_array, scale=5, threshold=0.15)   
    draw_button(screen, button_rect, button_text)
    draw_button(screen, button_rect2, button_text2)
    pygame.gfxdraw.rectangle(screen, pygame.Rect(389, SCREEN_HEIGHT - 591, SCREEN_WIDTH, 583), BORDER_COLOR) #simulation border

    if not simulation_running:

        if -20 <= int(temperature) <= 20:
            HERBIVORE_SPEED = 0.1 + (int(temperature) + 20) * (1 - 0.1) / (20 - (-20))
            PREDATOR_SPEED = 0.1 + (int(temperature) + 20) * (0.5 - 0.1) / (20 - (-20))
        elif 20 < int(temperature) <= 50:
            HERBIVORE_SPEED = 1 - (int(temperature) - 20) * (1 - 0.1) / (50 - 20)
            PREDATOR_SPEED = 0.5 - (int(temperature) - 20) * (0.5 - 0.1) / (50 - 20)
        else:
            HERBIVORE_SPEED = 0.1
            PREDATOR_SPEED = 0.1
        if int(temperature) <= -25 or int(temperature) >= 55:
            ENERGY_DEPLETION_FACTOR = 0.001

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

            if herbivore.energy <= 50:
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

            if predator.energy <= 50:
                predators.remove(predator)

        new_herbivores = []
        new_predators = []

        for h1 in herbivores:
            for h2 in herbivores:
                if h1 != h2 and h1.distance_to(h2) < MATING_DISTANCE:
                    offspring = h1.mate(h2)
                    if offspring:
                        new_herbivores.append(offspring)

        for p1 in predators:
            for p2 in predators:
                if p1 != p2 and p1.distance_to(p2) < MATING_DISTANCE:
                    offspring = p1.mate(p2)
                    if offspring:
                        new_predators.append(offspring)

    if not simulation_started:
        if button_text2 == "Begin":
            for plant in plants:
                plant.draw(screen)

            for herbivore in herbivores:
                herbivore.draw(screen)

            for predator in predators:
                predator.draw(screen)
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

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
