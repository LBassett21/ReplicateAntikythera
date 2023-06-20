import pygame
import math
import pygame.font
from datetime import *
import random
from OrbitalDynamics import *
from ReplicateAntikythera import *
import time

#Reference date
ref_date = date(2024, 1, 4)

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600 #size of the display.
screen = pygame.display.set_mode((width, height)) #creating pygame screen with width and height
pygame.display.set_caption("2D Solar System") #title

#background_image = pygame.image.load("C:\Solarsystem\stars_solarsystem.jpg")
#background_image = pygame.transform.scale(background_image, (width, height))

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

db = Database()
db.initDatabase()

earth_orbit = Orbit.fromDb("Earth", db)
earth = Planet(earth_orbit)

# Main game loop
running = True
clock = pygame.time.Clock()

sim_time = 0
curr_time = time.time()
while running:
    prev_time = curr_time
    curr_time = time.time()
    dt = curr_time - prev_time
    sim_time += (dt * (1/4))

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #screen.blit(background_image,(800,600))

    # Clear the screen
    screen.fill(BLACK)

    # Update planet positions
    earth_x = sun_pos[0] + earth.getPos(sim_time)[0] * 100
    earth_y = sun_pos[1] + earth.getPos(sim_time)[1] * 100
    earth_angle += earth_speed

    moon_x = earth_x + math.cos(moon_angle) * moon_distance
    moon_y = earth_y + math.sin(moon_angle) * moon_distance
    moon_angle += moon_speed

    mars_x = sun_pos[0] + math.cos(mars_angle) * mars_distance
    mars_y = sun_pos[1] + math.sin(mars_angle) * mars_distance
    mars_angle += mars_speed

    venus_x = sun_pos[0] + math.cos(venus_angle) * venus_distance
    venus_y = sun_pos[1] + math.sin(venus_angle) * venus_distance
    venus_angle += venus_speed

    mercury_x = sun_pos[0] + math.cos(mercury_angle) * mercury_distance
    mercury_y = sun_pos[1] + math.sin(mercury_angle) * mercury_distance
    mercury_angle += mercury_speed

    jupiter_x = sun_pos[0] + math.cos(jupiter_angle) * jupiter_distance
    jupiter_y = sun_pos[1] + math.sin(jupiter_angle)
    jupiter_angle += jupiter_speed

    #Draw the rotating lines for the planet
    #pygame.draw.line(screen, WHITE, sun_pos, (earth_x, earth_y), 1)
    #pygame.draw.line(screen, WHITE, sun_pos, (mars_x, mars_y), 1)

    # Clear the line positions
    zodiac_line_points.clear()

    # Calculate the zodiac line endpoints
    for i in range(12):  # Assuming there are 12 zodiac signs
        angle = earth_angle + (i * math.pi / 6)  # Angle for each zodiac sign
        line_x = earth_x + math.cos(angle) * 50  # Adjust the length of the lines as needed
        line_y = earth_y + math.sin(angle) * 50
        zodiac_line_points.append((line_x, line_y))

    # Draw the sun
    pygame.draw.circle(screen, YELLOW, sun_pos, sun_radius)

    #Draw the moon
    pygame.draw.circle(screen, WHITE, (int(moon_x), int (moon_y)),moon_radius)

    # Draw the planets
    pygame.draw.circle(screen, BLUE, (int(earth_x), int(earth_y)), earth_radius)
    pygame.draw.circle(screen, RED, (int(mars_x), int(mars_y)), mars_radius)
    pygame.draw.circle(screen, GREEN, (int(venus_x), int(venus_y)), venus_radius)
    pygame.draw.circle(screen, ORANGE, (int(mercury_x), int(mercury_y)),mercury_radius)
    pygame.draw.circle(screen, PURPLE, (int(jupiter_x), int(jupiter_y)),jupiter_radius)

    # Draws the lines around the earth for zodiac signs
    for line_point in zodiac_line_points:
        pygame.draw.line(screen, (128, 128, 128), (int(earth_x), int(earth_y)), line_point, 1)


    #Draw the key
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

    screen.blit(text_box, (key_x, key_y + len(key_text) * key_padding))

    for asteroid in asteroids:
        asteroid_distance, asteroid_speed, asteroid_angle = asteroid
        asteroid_x = sun_pos[0] + math.cos(asteroid_angle) * asteroid_distance
        asteroid_y = sun_pos[1] + math.sin(asteroid_angle) * asteroid_distance
        asteroid_angle += asteroid_speed
        asteroid = (asteroid_distance, asteroid_speed, asteroid_angle)

        pygame.draw.circle(screen, WHITE, (int(asteroid_x), int(asteroid_y)), asteroid_radius)

    # Update the asteroids list
    asteroids = [asteroid for asteroid in asteroids if asteroid[0] >= asteroid_distance_min]

    # Update the display
    pygame.display.flip()
    clock.tick(40)

# Quit the game
pygame.quit()

