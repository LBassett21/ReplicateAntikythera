import pygame
import math
import pygame.font
from datetime import datetime, timedelta
import random
import sys
import webbrowser



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
key_font = pygame.font.SysFont(None, 36) #font for the key
button_font = pygame.font.SysFont(None, 16)
key_text = {
    "Sun": "Yellow",
    "Earth": "Blue",
    "Moon": "White",
    "Mars": "Red",
    "Venus": "Green",
    "Mercury": "Orange",
    "Jupiter": "Purple"
    }

fastforward_button_rect = pygame.Rect(width // 2 + 55, height - 100, 70, 30)
fastforward_button_text = button_font.render("--->    ", True, WHITE)

slowdown_button_rect = pygame.Rect(width // 2 - 125, height - 100, 70, 30)
slowdown_button_text = button_font.render("<---    ", True, WHITE)

pause_button_rect = pygame.Rect(width - 100, 10, 90, 30)
pause_button_text = button_font.render("Pause", True, WHITE)


pause_button_rect1 = pygame.Rect(width // 2 - 45, height - 100, 90, 30)
pause_button_text1 = button_font.render("Pause", True, WHITE)

paused = False;

quit_button_rect = pygame.Rect(width - 200, 10, 90, 30)
quit_button_text = button_font.render("Exit", True, WHITE)

showstar_button_rect = pygame.Rect(width - 340, 10, 130, 30)
showstar_button_text = button_font.render("StarSign Wheel", True, WHITE)

github_button_rect = pygame.Rect(width - 440, 10, 90, 30)
github_button_text = button_font.render("Github", True, WHITE)

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
time = 0
wheel = False
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
            if github_button_rect.collidepoint(event.pos):
                webbrowser.open('https://github.com/LBassett21/ReplicateAntikythera/tree/master')
            if fastforward_button_rect.collidepoint(event.pos):
                print("fastforward")
            if pause_button_rect.collidepoint(event.pos):
                paused = not paused
            if pause_button_rect1.collidepoint(event.pos): #other pause button
                paused = not paused
            if showstar_button_rect.collidepoint(event.pos):
                wheel = not wheel
            if fastforward_button_rect.collidepoint(event.pos):
                if time < 5:
                    time = time + 1
            if slowdown_button_rect.collidepoint(event.pos):
                if time > -5:
                    time = time - 1
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

    
        
        clock = pygame.time.Clock()

        #create the locations of the stars for when we animate the background
        star_field_slow = []
        star_field_medium = []
        star_field_fast = []

        for slow_stars in range(50): 
            star_loc_x = random.randrange(0, width)
            star_loc_y = random.randrange(0, height)
            star_field_slow.append([star_loc_x, star_loc_y]) 

        for medium_stars in range(35):
            star_loc_x = random.randrange(0, width)
            star_loc_y = random.randrange(0, height)
            star_field_medium.append([star_loc_x, star_loc_y])

        for fast_stars in range(15):
            star_loc_x = random.randrange(0, width)
            star_loc_y = random.randrange(0, height)
            star_field_fast.append([star_loc_x, star_loc_y])

        #define some commonly used colours
        WHITE = (255, 255, 255)
        LIGHTGREY = (192, 192, 192)
        DARKGREY = (128, 128, 128)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        YELLOW = (255, 255, 0)
        MAGENTA = (255, 0, 255)
        CYAN = (0, 255, 255)
                                        
        #create the window
        while show_start_window:
            #need to move the button click event to under while loop as it refreshes with each iteration
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if show_start_window and Button_Start.rect.collidepoint(event.pos):
                        show_start_window = False
            
            
            screen.fill(BLACK)

            #draw starts
            for star in star_field_slow:
                star[1] += 1
                if star[1] > height:
                    star[0] = random.randrange(0, width)
                    star[1] = random.randrange(-20, -5)
                pygame.draw.circle(screen, DARKGREY, star, 3)

            for star in star_field_medium:
                star[1] += 4
                if star[1] > height:
                    star[0] = random.randrange(0, width)
                    star[1] = random.randrange(-20, -5)
                pygame.draw.circle(screen, LIGHTGREY, star, 2)

            for star in star_field_fast:
                star[1] += 8
                if star[1] > height:
                    star[0] = random.randrange(0, width)
                    star[1] = random.randrange(-20, -5)
                pygame.draw.circle(screen, YELLOW, star, 1)
            
            
            pygame.event.pump()
            
            #hover effect for start button
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
            #redraw everything we've asked pygame to draw
               #set frames per second
            clock.tick(30)
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
        line_x = earth_x + math.cos(angle) * 300  # Adjust the length of the lines as needed
        line_y = earth_y + math.sin(angle) * 300
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

    
#changing buttons based on if they are clicked or not    
    if showstar_button_rect == False:
        pygame.draw.rect(screen, BLUE, showstar_button_rect)
        screen.blit(showstar_button_text, showstar_button_rect.move(30,10))
    else:
        pygame.draw.rect(screen, BLUE, showstar_button_rect, 1)
        screen.blit(showstar_button_text, showstar_button_rect.move(30,10))
    
    if paused:
        pygame.draw.rect(screen, BLUE, pause_button_rect)
        screen.blit(pause_button_text, pause_button_rect.move(30,10))

        pygame.draw.rect(screen, BLUE, pause_button_rect1)
        screen.blit(pause_button_text1, pause_button_rect1.move(30,10))
    else: #drawing both pause buttons here 
        pygame.draw.rect(screen, BLUE, pause_button_rect, 1)
        screen.blit(pause_button_text, pause_button_rect.move(30,10))

        pygame.draw.rect(screen, BLUE, pause_button_rect1, 1)
        screen.blit(pause_button_text1, pause_button_rect1.move(30,10))
    
   
    pygame.draw.rect(screen, BLUE, fastforward_button_rect, 1)
    screen.blit(fastforward_button_text, fastforward_button_rect.move(30,10))
    pygame.draw.rect(screen, BLUE, slowdown_button_rect, 1)
    screen.blit(slowdown_button_text, slowdown_button_rect.move(30,10))
    
    
    # Add a exit button on top of the scaled screen
    # Add a exit button on top of the scaled screen
    pygame.draw.rect(screen, BLUE, quit_button_rect, 1)
    screen.blit(quit_button_text, quit_button_rect.move(30,10))

    pygame.draw.rect(screen, BLUE, github_button_rect, 1)
    screen.blit(github_button_text, github_button_rect.move(30,10))
    #Draw the key
    text_surface_time = key_font.render(f"{time}x", True, BLUE)
    screen.blit(text_surface_time, (width // 2 - 10, height - 130))
    
   
    
    if wheel: 
        pygame.draw.rect(screen, BLUE, showstar_button_rect)
        screen.blit(showstar_button_text, showstar_button_rect.move(30,10))

        triangle0 = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[0]), (zodiac_line_points[1]))
        pygame.draw.polygon(screen, WHITE, triangle0, 1)
        triangle1 = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[1]), (zodiac_line_points[2]))
        pygame.draw.polygon(screen, WHITE, triangle1, 1)
        triangle2 = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[2]), (zodiac_line_points[3]))
        pygame.draw.polygon(screen, WHITE, triangle2, 1)
        triangle3 = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[3]), (zodiac_line_points[4]))
        pygame.draw.polygon(screen, WHITE, triangle3, 1)
        triangle4 = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[4]), (zodiac_line_points[5]))
        pygame.draw.polygon(screen, WHITE, triangle4, 1)
        triangle5 = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[5]), (zodiac_line_points[6]))
        pygame.draw.polygon(screen, WHITE, triangle5, 1)
        triangle6 = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[6]), (zodiac_line_points[7]))
        pygame.draw.polygon(screen, WHITE, triangle6, 1)
        triangle7 = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[7]), (zodiac_line_points[8]))
        pygame.draw.polygon(screen, WHITE, triangle7, 1)
        triangle8 = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[8]), (zodiac_line_points[9]))
        pygame.draw.polygon(screen, WHITE, triangle8, 1)
        triangle9 = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[9]), (zodiac_line_points[10]))
        pygame.draw.polygon(screen, WHITE, triangle9, 1)
        triangle10 = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[10]), (zodiac_line_points[11]))
        pygame.draw.polygon(screen, WHITE, triangle10, 1)
        triangle11 = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[11]), (zodiac_line_points[0]))
        pygame.draw.polygon(screen, WHITE, triangle11, 1)
        
        
        special_font = pygame.font.SysFont(None, 60)
        text1_surface = special_font.render(f"{current_sign}", True, RED)
        
    
       # screen.blit(text1_surface, (width // 2 - 100, height // 2 ))
        screen.blit(text1_surface, ((zodiac_line_points[current_sign_index])))
        
        if current_sign_index > 0:
            triangle = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[current_sign_index]), (zodiac_line_points[current_sign_index - 1]))
            pygame.draw.polygon(screen, RED, triangle, 2)
            #pygame.draw.line(screen, TRANSPARENTBLUE, ( (int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[current_sign_index])))
        else: 
            triangle = ((int(sun_pos[0]), int(sun_pos[1])), (zodiac_line_points[current_sign_index]), (zodiac_line_points[current_sign_index - 1]))
            pygame.draw.polygon(screen, RED, triangle, 2)
    

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
