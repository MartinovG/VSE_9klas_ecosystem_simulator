import pygame

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
