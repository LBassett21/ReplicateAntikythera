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
