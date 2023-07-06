from OrbitalDynamics import *
from scipy.spatial.transform import Rotation
from datetime import timedelta
from numpy import *
from math import acos

import GUI

'''
primary: the satellite or planet around which the satellite orbits
'''
class Satellite:
    t_offset=0

    def __init__(self, orbit, primary):
        self.orbit = orbit
        self.primary = primary

    '''
    Given sim time (t), compute the position of the satellite.
    The position has the form of a 3d vector (X, Y, Z) with units in AU with reference to the Sun (0, 0, 0).
    '''
    def getPos(self, t=None, f=None):
        orbit = self.orbit
        primary = self.primary

        if(f==None):
            f = orbit.tToF(t+self.t_offset)
            r = orbit.getDistance(t+self.t_offset)
        else:
            t = orbit.fToT(f)
            r = orbit.getDistance(t+self.t_offset)

        pos = [r, 0, 0]

        rot = Rotation.from_euler('ZXZ', [-orbit.La, orbit.i, orbit.w + math.degrees(f)], degrees = True)
        pos = rot.apply(pos)

        if (primary != None):
            pos += primary.getPos(t)

        return pos

    def align(self, t, direction):
        curr_dir = self.getPos(t)

        mag_dir = (direction[0]**2 + direction[1]**2 + direction[2]**2) ** (1/2)
        mag_curr_dir = (curr_dir[0]**2 + direction[1]**2 + direction[2]**2) ** (1/2)

        angle = acos(dot(curr_dir, direction) / (mag_dir * mag_curr_dir))

        f = angle - radians(self.orbit.La + self.orbit.w)

        t_dir = self.orbit.fToT(f)
        t_offset = t_dir - t

        return t_offset

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
    # semimajor axis, eccentricity, angle of inclination, longitude of ascending node, longitude of perihelion, orbital period, date of periapsis
    #earth_orbit = Orbit(1, 0.016710, 0, -11.26064, 114.20783, 1, date(2024, 1, 4))
    earth_orbit = Orbit(1, 0.5, 135, 0, 0, 1, date(2024, 1, 4))
    earth = Planet(earth_orbit)
    print(earth.getPos(0))

if (__name__ == "__main__"):
    main()
