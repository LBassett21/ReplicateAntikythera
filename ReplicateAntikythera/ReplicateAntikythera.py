from cgi import test
from OrbitalDynamics import *
from scipy.spatial.transform import Rotation
from datetime import timedelta
from math import *

import GUI
from Database import Database
#from Events_Database import Events
import Tests

'''
primary: the satellite or planet around which the satellite orbits
'''
class Satellite:
    f_offset = 0

    def __init__(self, orbit, primary):
        self.orbit = orbit
        self.primary = primary

    '''
    Given sim time (t), compute the position of the satellite.
    The position has the form of a 3d vector (X, Y, Z) with units in AU with reference to the Sun (0, 0, 0).
    '''
    def getPos(self, t, f = None):
        orbit = self.orbit
        primary = self.primary

        if(f==None):
            f = orbit.tToF(t) + self.f_offset
            r = orbit.getDistance(t)
        else:
            t = orbit.fToT(f + self.f_offset)
            r = orbit.getDistance(t)

        pos = [r, 0, 0]

        rot = Rotation.from_euler('ZXZ', [-orbit.La, orbit.i, orbit.La + orbit.w + math.degrees(f)], degrees = True)
        pos = rot.apply(pos)

        if (primary != None):
            pos += primary.getPos(t)

        return pos

    def align(self, t, direction):
        """
        t: the current time (sim time)

        direction: the vector towards the desired position

        f1: the current true anomaly
        f2: the desired true anomaly

        f_offset: f2 - f1
        """

        f1 = self.orbit.tToF(t)
        f2 = atan2(-direction[1], direction[0]) - radians(self.orbit.w)

        self.f_offset = f2 - f1

    def getPrimaryPos(self, t):
        if self.primary == None:
            return (0, 0, 0)
        else:
            return self.primary.getPos(t)

    def getDistance(self, t):
        return self.orbit.getDistance(t)

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

    db_events = Events()
    db_events.initComets()
    db_events.initSolarEclipses()
    db_events.initLunarEclipses()
    db_events.initSpaceLaunches()

    earth_orbit = Orbit.fromDb("Earth", db)
    earth = Planet(earth_orbit)

    db.closeDatabase()
    db_events.closeDatabase()

if (__name__ == "__main__"):
    main()
