


#constants
meters_per_astronomical_unit = 1.4959787**11
meters_per_earth_equatorial_radius = 6378140.0
earth_rad_per_astronomical_unit = meters_per_astronomical_unit / meters_per_earth_equatorial_radius

from OrbitalDynamics import *
from scipy.spatial.transform import Rotation

'''
a: semimajor axis (in AU)
e: eccentricity
i: angle of inclination (in degrees, relative to the orbital plane of the Earth (ecliptic))
LA: longitude of the ascending node
w: longitude of perihelion (in degrees relative to the vernal equinox)
T: orbital period (in years)
primary: the satellite or planet around which the satellite orbits
'''
class Satellite:
    def __init__(self, a, e, i, La, w, T, primary):
        self.a = a
        self.e = e
        self.i = i
        self.La = La
        self.w = w
        self.T = T
        self.primary = primary

    '''
    Given time since periapse (t), compute the position of the satellite.
    The position has the form of a 3d vector (X, Y, Z) with units in AU with reference to the Sun (0, 0, 0).
    '''
    def getPos(self, t):
        a = self.a
        e = self.e
        i = self.i
        La = self.La
        w = self.w
        T = self.T

        f = tspToF(t, self.a, self.e, self.i, self.T)
        r = a * (1 - math.pow(e, 2)) / (1 + e * math.cos(f))
        longitude = f + La + w
        pos = [r, 0, 0]
        rot = Rotation.from_euler('z', longitude, degrees = True)
        pos = rot.apply(pos)
        # !! TODO: Implement rotation of orbital plane !!

        return pos

class Planet(Satellite):
    def __init__(self, a, e, i, La, w, T):
        # Planets have no primary, since they orbit the Sun, which is at the origin.
        super().__init__(a, e, i, La, w, T, None)

class Moon(Satellite):
    def __init__(self, a, e, i, La, w, T):
        super().__init__(self, a, e, i, La, w, T)

class Asteroid:
    def __init__(self):
        pass

# I have no idea if this works yet
earth = Planet(1, 0.016710, 0, -11.26064, 114.20783, 1)
print(earth.getPos(0))










import pygame
import math
import pygame.font

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

earth_radius = 10
earth_distance = 200
earth_speed = 0.02
earth_angle = 0
earth_mass = 1

mars_radius = 7
mars_distance = 300
mars_speed = 0.01
mars_angle = 0
mars_mass = 0.8

venus_radius = 9
venus_distance = 150
venus_speed = 0.03
venus_angle = 0
venus_mass = 0.6

mercury_radius = 6
mercury_distance = 120
mercury_speed = 0.04
mercury_angle = 0
mercury_mass = 0.4

jupiter_radius = 20
jupiter_distance = 400
jupiter_speed = 0.008
jupiter_angle = 0
jupiter_mass = 2.5


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

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Update planet positions
    earth_x = sun_pos[0] + math.cos(earth_angle) * earth_distance
    earth_y = sun_pos[1] + math.sin(earth_angle) * earth_distance
    earth_angle += earth_speed

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
    ##pygame.draw.line(screen, WHITE, sun_pos, (earth_x, earth_y), 1)
    ##pygame.draw.line(screen, WHITE, sun_pos, (mars_x, mars_y), 1)

    # Draw the sun
    pygame.draw.circle(screen, YELLOW, sun_pos, sun_radius)

    # Draw the planets
    pygame.draw.circle(screen, BLUE, (int(earth_x), int(earth_y)), earth_radius)
    pygame.draw.circle(screen, RED, (int(mars_x), int(mars_y)), mars_radius)
    pygame.draw.circle(screen, GREEN, (int(venus_x), int(venus_y)), venus_radius)
    pygame.draw.circle(screen, ORANGE, (int(mercury_x), int(mercury_y)), mercury_radius)
    pygame.draw.circle(screen, PURPLE, (int(jupiter_x), int(jupiter_y)), jupiter_radius)

    #Draw the key
    key_x =10
    key_y = 10
    key_padding = 20

    for i, (planet, color) in enumerate(key_text.items()):
        key_surface = key_font.render(f"{planet}: {color}", True, WHITE)
        screen.blit(key_surface, (key_x, key_y + i * key_padding))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()

