from cgi import test
from OrbitalDynamics import *
from scipy.spatial.transform import Rotation
from datetime import timedelta

import GUI
from Database import Database

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
    db = Database()
    db.initDatabase()

    earth_orbit = Orbit.fromDb("Earth", db)
    earth = Planet(earth_orbit)

    db.closeDatabase()

if (__name__ == "__main__"):
    main()
