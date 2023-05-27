import pygame

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
initial_plants = '0'
initial_herbivores = '0'
initial_predators = '0'
temperature = '0'
PLANT_REPRODUCTION_RATE = 0.01
MATING_ENERGY_THRESHOLD = 15000  
OFFSPRING_ENERGY_FACTOR = 0.2  
MATING_DISTANCE = 2  
start_x1 = SCREEN_WIDTH - 500
start_y1 = SCREEN_HEIGHT - 500 
start_x2 = SCREEN_WIDTH - 500 
start_y2 = SCREEN_HEIGHT - 400
image1_x, image1_y = start_x1, start_y1
image2_x, image2_y = start_x2, start_y2
area_x, area_y, area_w, area_h = 390, SCREEN_HEIGHT - 590, SCREEN_WIDTH - 390, 590
pygame.font.init()
font = pygame.font.Font(None, 36)
text = font.render("Hold here", True, (0, 0, 0))
radius = 100  
speed = 0.05 
attraction_speed = 0.5 

button_width, button_height = 100, 40
button_x, button_y = 110, 10
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
simulation_running = True
button_text = "Start"
button_x2, button_y2 = 10, 10
button_rect2 = pygame.Rect(button_x2, button_y2, button_width, button_height)
simulation_started = True
button_text2 = "Finish"

input_rect = pygame.Rect(10, 200, 140, 32) #plants
color_active = pygame.Color(144, 238, 144)
color_passive = pygame.Color(69,139,0)
color = color_passive
active = False

input_rect2 = pygame.Rect(10, 250, 140, 32) #herbivores
color_active2 = pygame.Color(173, 216, 230)
color_passive2 = pygame.Color(30,144,255)
color2 = color_passive2
active2 = False

input_rect3 = pygame.Rect(10, 300, 140, 32) #predators
color_active3 = pygame.Color(250, 128, 114)
color_passive3 = pygame.Color(128, 0, 0)
color3 = color_passive3
active3 = False

input_rect4 = pygame.Rect(10, 350, 140, 32) #temperature
color_active4 = pygame.Color(192, 192, 192)
color_passive4 = pygame.Color(105,105,105)
color4 = color_passive4
active4 = False
