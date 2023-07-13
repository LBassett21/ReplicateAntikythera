import pygame
import math
import pygame.font

from ReplicateAntikythera import *

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600 #size of the display.
screen = pygame.display.set_mode((width, height)) #creating pygame screen with width and height
pygame.display.set_caption("2D Solar System") #title

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

p1_radius = 10
p1_distance = 200
p1_speed = 0.02
p1_angle = 0
p1_mass = 1

#Define the information for the key
key_font = pygame.font.SysFont(None, 16) #font for the key
key_text = {
    "Sun": "Yellow",
    "Earth": "Blue",
    "Mars": "Red",
    "Venus": "Green",
    "Mercury": "Orange",
    "Jupiter": "Purple"
    }


# semimajor axis, eccentricity, angle of inclination, longitude of ascending node, longitude of perihelion, orbital period, date of periapsis
p1_orbit = Orbit(1, 0, 0, 0, 0, 1, date(2024, 1, 4))
p2_orbit = Orbit(2, 0, 0, 0, -45, 1, date(2024, 1, 4))
p3_orbit = Orbit(3, 0.4, math.pi/3, 0, -90, 3, date(2024, 1, 4))
#p1_orbit = Orbit(1, 0.016710, 0, -11.26064, 114.20783, 1, date(2024, 1, 4))
p1 = Planet(p1_orbit)
p2 = Planet(p2_orbit)
p3 = Planet(p3_orbit)

# Main game loop
running = True
clock = pygame.time.Clock()

sim_time = 0
dt = 0

angle = math.pi

p1.align(sim_time, [1, 1, 0])
p2.align(sim_time, [-1, 1, 0])

while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1 second of real time = 0.25 years of sim time
    sim_time = (sim_time + (dt / 1000)/4)

    # Clear the screen
    screen.fill(BLACK)

    # Update planet positions
    '''
    p1_x = sun_pos[0] + math.cos(earth_angle) * earth_distance
    p1_y = sun_pos[1] + math.sin(earth_angle) * earth_distance
    p1_angle += earth_speed
    '''


    p1_x = sun_pos[0] + p1.getPos(sim_time)[0] * 100
    p1_y = sun_pos[1] + p1.getPos(sim_time)[1] * 100
    p2_x = sun_pos[0] + p2.getPos(sim_time)[0] * 100
    p2_y = sun_pos[1] + p2.getPos(sim_time)[1] * 100
    p3_x = sun_pos[0] + p3.getPos(sim_time)[0] * 100
    p3_y = sun_pos[1] + p3.getPos(sim_time)[1] * 100

    # Draw the sun
    pygame.draw.circle(screen, YELLOW, sun_pos, sun_radius)

    # Draw the planets
    pygame.draw.circle(screen, BLUE, (int(p1_x), int(p1_y)), p1_radius)
    pygame.draw.circle(screen, RED, (int(p2_x), int(p2_y)), p1_radius)
    pygame.draw.circle(screen, GREEN, (int(p3_x), int(p3_y)), p1_radius)

    #Draw the key
    key_x =10
    key_y = 10
    key_padding = 20

    for i, (planet, color) in enumerate(key_text.items()):
        key_surface = key_font.render(f"{planet}: {color}", True, WHITE)
        screen.blit(key_surface, (key_x, key_y + i * key_padding))

    # Update the display
    pygame.display.flip()
    dt = clock.tick(60)

# Quit the game
pygame.quit()
