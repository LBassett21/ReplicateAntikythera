from cmath import e
import math
from re import I
from tkinter import Label
from scipy.optimize import newton
from datetime import *
from math import *

ref_date = date(2024, 1, 4)

'''
Kepler's Equation, used in finding true anomaly in tsoToF
E: eccentric anomaly
e: eccentricity
M: mean anomaly
'''
def kepEqn(E, e, M):
    return E - e * math.sin(E) - M

# Derivative of Kepler's Equation, used in finding roots
# (it needs 3 arguments for the scipy implemenation of Newton's Method to work)
def kepEqnDeriv(E, e, M):
    return 1 - e * math.cos(E)

'''
Compute the mean anomaly
t: time since periapsis
T: orbital period
'''
def meanAnomaly(t, T):
    return 2 * math.pi * t / T

'''
a: semimajor axis (in AU)
e: eccentricity
i: angle of inclination (in degrees, relative to the orbital plane of the Earth (ecliptic))
LA: longitude of the ascending node
w: longitude of perihelion (in degrees relative to the vernal equinox)
T: orbital period (in years)
dop: a date of periapsis
'''
class Orbit():
    def __init__(self, a, e, i, La, w, T, dop):
        self.a = a
        self.e = e
        self.i = i
        self.La = La
        self.w = w
        self.T = T
        self.dop = dop

    '''
    Given sim time (t), find time since periapsis
    '''
    def getTsp(self, t):
        curr_date = ref_date + timedelta(days = t * 365)
        tsp = (curr_date - self.dop).days / 365

        return tsp
    
    '''
    compute true anomaly (f) from sim time (t)
    '''
    def tToF(self, t):
        T = self.T
        e = self.e

        if (T <= 0):
            raise Exception("T cannot be <= 0")

        tsp = self.getTsp(t)

        # 1: find mean anomaly (M)
        M = meanAnomaly(tsp, T)

        # 2: find eccentric anomaly (E)
        # here, we have to find the roots of Kepler's Equation
        E = newton(kepEqn, 0, kepEqnDeriv, (e, M))

        # 3: use E to solve for f
        f = -2 * math.atan(math.tan(E/2) / (math.sqrt((1 - e) / (1 + e))))

        return f

    # True anomaly to time
    def fToT(self, f):
        T = self.T
        e = self.e

        # use f to solve for E
        E = 2*atan(((1-e)/(1+e))**(1/2)*tan(f/2))

        # use E to solve for M
        M = E - e*sin(E)

        # use E and M to solve for t
        t = M/(2*math.pi)*T

        return t
    
    # Get distance from primary at sim time t
    def getDistance(self, t):
        a = self.a
        e = self.e
        tsp = self.getTsp(t)
        f = self.tToF(tsp)

        return a * (1 - math.pow(e, 2)) / (1 + e * math.cos(f))

