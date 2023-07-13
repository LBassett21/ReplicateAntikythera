import pygame
import math
import pygame.font
from datetime import datetime, timedelta
import random
import sys

#Reference date
ref_date = datetime(2023, 1, 4)
current_date = ref_date
TRANSPARENTBLUE = pygame.Color(173, 216, 230, 255)
# Initialize Pygame
pygame.init()

# Set up the display
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h #size of the display.
screen = pygame.display.set_mode((0,0),pygame.RESIZABLE) #creating pygame screen with width and height
pygame.display.set_caption("Replicate Antikythera") #title

# Start window surface definition
start_window = pygame.Surface((width, height))
start_font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 80)
# Imports background image to program
background_image = pygame.image.load("starry_night.jpg")
background_image = pygame.transform.smoothscale(background_image, (width,height))

#List to store zodiac line position
zodiac_line_points = []

#Zodiac signs list !ADD TO DATABASE!
zodiac_signs = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Define colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 150, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)

# Define planet properties
sun_radius = 30
sun_pos = (width // 2, height // 2)
sun_mass = 1000

earth_radius = 10
earth_distance = 200
earth_speed = -0.02
earth_angle = 0
earth_mass = 1

moon_radius = 4
moon_distance = 30
moon_speed = -0.1
moon_angle = 0
moon_mass = 0.2


mars_radius = 7
mars_distance = 300
mars_speed = -0.01
mars_angle = 0
mars_mass = 0.8

venus_radius = 9
venus_distance = 150
venus_speed = -0.03
venus_angle = 0
venus_mass = 0.6

mercury_radius = 6
mercury_distance = 120
mercury_speed = -0.04
mercury_angle = 0
mercury_mass = 0.4

jupiter_radius = 20
jupiter_distance = 400
jupiter_speed = -0.008
jupiter_angle = 0
jupiter_mass = 2.5


#Define the information for the key
key_font = pygame.font.SysFont(None, 16) #font for the key
key_text = {
    "Sun": "Yellow",
    "Earth": "Blue",
    "Moon": "White",
    "Mars": "Red",
    "Venus": "Green",
    "Mercury": "Orange",
    "Jupiter": "Purple"
    }

pause_button_rect = pygame.Rect(width - 100, 10, 90, 30)
pause_button_text = key_font.render("Pause", True, WHITE)

paused = False;

quit_button_rect = pygame.Rect(width - 200, 10, 90, 30)
quit_button_text = key_font.render("Exit", True, WHITE)

showstar_button_rect = pygame.Rect(width - 340, 10, 130, 30)
showstar_button_text = key_font.render("StarSign Wheel", True, BLACK)
# Define asteroid belt properties
asteroid_radius = 2
asteroid_distance_min = 250
asteroid_distance_max = 300
asteroid_speed_min = -0.03
asteroid_speed_max = 0.03
asteroid_count = 200
asteroids = []

for _ in range(asteroid_count):
    asteroid_distance = random.randint(asteroid_distance_min, asteroid_distance_max)
    asteroid_speed = random.uniform(asteroid_speed_min, asteroid_speed_max)
    asteroid_angle = random.uniform(0, 2 * math.pi)
    asteroids.append((asteroid_distance, asteroid_speed, asteroid_angle))

# Main game loop
wheel = True
running = True
clock = pygame.time.Clock()

show_start_window = True
dragging = False

# Define initial constants
zoom_scale = 1.0
offset_x = 0
offset_y = 0

# Define the fixed point for zooming
zoom_center_x = width // 2
zoom_center_y = height // 2

class Option:

    hovered = False
    
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()
    
    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)
        
    def set_rend(self):
        self.rend = start_font.render(self.text, True, self.get_color())
   
        #start_font = pygame.font.SysFont(None, 36)
    def get_color(self):
        if self.hovered:
            return (255, 255, 255)
        else:
            return (100, 100, 100)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.center = self.pos

show_start_window = True

Button_Start = Option("Press START to begin",((width // 2) , height // 2))

#storing hovertexts in array called options
options = [Button_Start]



while running:
    # Scale the screen
    
    scaled_width = int(width * zoom_scale)
    scaled_height = int(height * zoom_scale)
    scaled_screen = pygame.Surface((scaled_width, scaled_height))

    # Scale the background image
    scaled_background_image = pygame.transform.smoothscale(background_image, (scaled_width, scaled_height))
  
    # Calculate the center of the scaled screen
    scaled_center_x = scaled_width // 2
    scaled_center_y = scaled_height // 2

    # Calculate the mouse cursor position relative to the scaled screen
    mouse_x, mouse_y = pygame.mouse.get_pos()
    scaled_mouse_x = (mouse_x - scaled_center_x) / zoom_scale + scaled_center_x
    scaled_mouse_y = (mouse_y - scaled_center_y) / zoom_scale + scaled_center_y

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if quit_button_rect.collidepoint(event.pos):
                running = False
            if pause_button_rect.collidepoint(event.pos):
                paused = not paused
            if showstar_button_rect.collidepoint(event.pos):
                wheel = not wheel
            elif show_start_window and Button_Start.rect.collidepoint(event.pos):
                show_start_window = False
            elif not dragging:
                dragging = True
            
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if dragging:
                dragging = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 and not show_start_window:
            zoom_scale *= 1.05
            offset_x = zoom_center_x - scaled_mouse_x / zoom_scale
            offset_y = zoom_center_y - scaled_mouse_y / zoom_scale
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 and not show_start_window:
            zoom_scale /= 1.05
            offset_x = zoom_center_x - scaled_mouse_x / zoom_scale
            offset_y = zoom_center_y - scaled_mouse_y / zoom_scale

    if show_start_window:
        
        screen.blit(background_image, (0,0))
       
        pygame.event.pump()
        for option in options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()
        

        # Draw the title
        title_font = pygame.font.SysFont("Arial", 80, bold=True)
        title_text = title_font.render("Replicate Antikythera", True, WHITE)
        title_text_rect = title_text.get_rect(center=(width // 2, height // 2 - 50))
        screen.blit(title_text, title_text_rect)

        # Draw the start button
        #button_font = pygame.font.SysFont("Arial", 36)
        #button_text = button_font.render("START", True, WHITE)
        #button_rect = pygame.Rect(width // 2 - 75, height // 2 + 20, 150, 50)
        #pygame.draw.rect(screen, (50, 50, 50), button_rect)
        #screen.blit(button_text, button_rect.move(30, 5))

        pygame.display.flip()
        continue

    # Move/Offset the screen if dragging is true
    if dragging:
        offset_x += mouse_x - prev_mouse_x
        offset_y += mouse_y - prev_mouse_y
    prev_mouse_x = mouse_x
    prev_mouse_y = mouse_y

    if not paused:
    # Update planet positions
        scaled_sun_pos = (scaled_center_x + offset_x, scaled_center_y + offset_y)

        earth_x = scaled_sun_pos[0] + math.cos(earth_angle) * earth_distance // zoom_scale
        earth_y = scaled_sun_pos[1] + math.sin(earth_angle) * earth_distance // zoom_scale
        earth_angle += earth_speed

        moon_x = earth_x + math.cos(moon_angle) * moon_distance // zoom_scale
        moon_y = earth_y + math.sin(moon_angle) * moon_distance // zoom_scale
        moon_angle += moon_speed

        mars_x = scaled_sun_pos[0] + math.cos(mars_angle) * mars_distance // zoom_scale
        mars_y = scaled_sun_pos[1] + math.sin(mars_angle) * mars_distance // zoom_scale
        mars_angle += mars_speed

        venus_x = scaled_sun_pos[0] + math.cos(venus_angle) * venus_distance // zoom_scale
        venus_y = scaled_sun_pos[1] + math.sin(venus_angle) * venus_distance // zoom_scale
        venus_angle += venus_speed

        mercury_x = scaled_sun_pos[0] + math.cos(mercury_angle) * mercury_distance // zoom_scale
        mercury_y = scaled_sun_pos[1] + math.sin(mercury_angle) * mercury_distance // zoom_scale
        mercury_angle += mercury_speed

        jupiter_x = scaled_sun_pos[0] + math.cos(jupiter_angle) * jupiter_distance // zoom_scale
        jupiter_y = scaled_sun_pos[1] + math.sin(jupiter_angle) * jupiter_distance // zoom_scale
        jupiter_angle += jupiter_speed

    

    # Clear the line positions
        zodiac_line_points.clear()

    # Calculate the zodiac line endpoints
    for i in range(12):  # Assuming there are 12 zodiac signs
        angle = (i * math.pi / 6)  # Angle for each zodiac sign
        line_x = earth_x + math.cos(angle) * 400  # Adjust the length of the lines as needed
        line_y = earth_y + math.sin(angle) * 400
        zodiac_line_points.append((line_x, line_y))

    scaled_screen.blit(scaled_background_image, (0, 0))

    # Draw the sun
    pygame.draw.circle(scaled_screen, YELLOW, (int(scaled_sun_pos[0]),int(scaled_sun_pos[1])), int(sun_radius//zoom_scale))

    #Draw the moon
    pygame.draw.circle(scaled_screen, WHITE, (int(moon_x), int (moon_y)),int(moon_radius//zoom_scale))

    # Draw the planets
    pygame.draw.circle(scaled_screen, BLUE, (int(earth_x), int(earth_y)), int(earth_radius//zoom_scale))
    pygame.draw.circle(scaled_screen, RED, (int(mars_x), int(mars_y)), int(mars_radius//zoom_scale))
    pygame.draw.circle(scaled_screen, GREEN, (int(venus_x), int(venus_y)), int(venus_radius//zoom_scale))
    pygame.draw.circle(scaled_screen, ORANGE, (int(mercury_x), int(mercury_y)),int(mercury_radius//zoom_scale))
    pygame.draw.circle(scaled_screen, PURPLE, (int(jupiter_x), int(jupiter_y)),int(jupiter_radius//zoom_scale))


    key_x =10
    key_y = 10
    key_padding = 20

    for i, (planet, color) in enumerate(key_text.items()):
        key_surface = key_font.render(f"{planet}: {color}", True, WHITE)
        screen.blit(key_surface, (key_x, key_y + i * key_padding))

     # Calculates the current sign
    current_sign_index = int((earth_angle / (2 * math.pi)) * len(zodiac_signs)) % len(zodiac_signs)
    current_sign = zodiac_signs[current_sign_index]

    text_box = pygame.Surface((200, 30))
    text_box.fill(BLACK)
    text_surface = key_font.render(f"Current Sign: {current_sign}", True, WHITE)
    text_box.blit(text_surface, (10, 5))
    # Draws the lines around the earth for zodiac signs
    #for line_point in zodiac_line_points:
     #   pygame.draw.line(scaled_screen, (128, 128, 128), (int(earth_x), int(earth_y)), line_point, 1)
  
    
    screen.blit(text_box, (key_x, key_y + len(key_text) * key_padding))
    for asteroid in asteroids:
        asteroid_distance, asteroid_speed, asteroid_angle = asteroid
        asteroid_x = scaled_sun_pos[0] + math.cos(asteroid_angle) * asteroid_distance // zoom_scale
        asteroid_y = scaled_sun_pos[1] + math.sin(asteroid_angle) * asteroid_distance // zoom_scale
        asteroid_angle += asteroid_speed
        asteroid = (asteroid_distance, asteroid_speed, asteroid_angle)

        pygame.draw.circle(scaled_screen, WHITE, (int(asteroid_x), int(asteroid_y)), asteroid_radius)

    # Update the asteroids list
    asteroids = [asteroid for asteroid in asteroids if asteroid[0] >= asteroid_distance_min]

    # Update the display with the scaled screen
    screen.blit(pygame.transform.scale(scaled_screen, (width, height)), (0, 0))

    pygame.draw.rect(screen, RED, showstar_button_rect)
    screen.blit(showstar_button_text, showstar_button_rect.move(30,10))
    # Add a pause button on top of the scaled screen
    pygame.draw.rect(screen, RED, pause_button_rect, 1)
    screen.blit(pause_button_text, (pause_button_rect.x, pause_button_rect.y))

    # Add a exit button on top of the scaled screen
    pygame.draw.rect(screen, RED, quit_button_rect, 1)
    screen.blit(quit_button_text, (quit_button_rect.x, quit_button_rect.y))

    #Draw the key
    
   
   
    if wheel: 
        if current_sign_index > 0:
            triangle = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[current_sign_index]), (zodiac_line_points[current_sign_index - 1]))
            pygame.draw.polygon(screen, TRANSPARENTBLUE, triangle, 2)
            #pygame.draw.line(screen, TRANSPARENTBLUE, ( (int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[current_sign_index])))
        else: 
            triangle = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[current_sign_index]), (zodiac_line_points[current_sign_index - 1]))
            pygame.draw.polygon(screen, TRANSPARENTBLUE, triangle, 2)
    

    for i, (planet, color) in enumerate(key_text.items()):
        if planet == "Earth":
            planet_text = f"{planet}: {color} ({current_sign})"
        else:
            planet_text = f"{planet}: {color}"
        key_surface = key_font.render(planet_text, True, WHITE)
        screen.blit(key_surface, (key_x, key_y + i * key_padding))
   
    pygame.display.flip()
    clock.tick(40)

# Quit the game
pygame.quit()
