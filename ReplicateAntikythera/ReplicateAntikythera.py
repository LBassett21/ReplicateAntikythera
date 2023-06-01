#constants
meters_per_astronomical_unit = 1.4959787**11
meters_per_earth_equatorial_radius = 6378140.0
earth_rad_per_astronomical_unit = meters_per_astronomical_unit / meters_per_earth_equatorial_radius

from OrbitalDynamics import *
from scipy.spatial.transform import Rotation
from datetime import timedelta

import GUI

'''
primary: the satellite or planet around which the satellite orbits
'''
class Satellite:
    def __init__(self, orbit, primary):
        self.orbit = orbit
        self.primary = primary

    '''
    Given sim time (t), compute the position of the satellite.
    The position has the form of a 3d vector (X, Y, Z) with units in AU with reference to the Sun (0, 0, 0).
    '''
    def getPos(self, t):
        orbit = self.orbit
        primary = self.primary

        f = orbit.tToF(t)
        r = orbit.getDistance(t)

        pos = [r, 0, 0]

        rot = Rotation.from_euler('z', -orbit.La, degrees = True)
        pos = rot.apply(pos)

        rot = Rotation.from_euler('x', orbit.i, degrees = True)
        pos = rot.apply(pos)

        rot = Rotation.from_euler('z', 2 * orbit.La + orbit.w + math.degrees(f), degrees = True)
        pos = rot.apply(pos)

        if (primary != None):
            pos += primary.getPos(t)

        return pos

class Planet(Satellite):
    def __init__(self, orbit):
        # Planets have no primary, since they orbit the Sun, which is at the origin.
        super().__init__(orbit, None)

class Moon(Satellite):
    def __init__(self, orbit, primary):
        super().__init__(orbit, primary)

class Asteroid:
    def __init__(self):
        pass

def main():
    #define orbits
    # semimajor axis, eccentricity, longitude of ascending node, argument of perihelion, orbital period, date of periapsis
    earth_orbit = Orbit(1, 0.016710, 0, -11.26064, 114.20783, 1, date(2024, 1, 4))
    earth = Planet(earth_orbit)
    print(earth.getPos(0))

if (__name__ == "__main__"):
    main()
