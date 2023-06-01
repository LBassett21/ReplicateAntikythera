import math
from scipy.optimize import newton

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
compute true anomaly (f) from time since periapsis (t)
a: semimajor axis
e: eccentricity
i: angle of inclination
T: orbital period
'''
def tspToF(t, a, e, i, T):
    if (T <= 0):
        raise Exception("T cannot be <= 0")

    # 1: find mean anomaly (M)
    M = meanAnomaly(t, T)

    # 2: find eccentric anomaly (E)
    # here, we have to find the roots of Kepler's Equation
    E = newton(kepEqn, 0, kepEqnDeriv, (e, M))

    # 3: use E to solve for f
    f = 2 * math.atan(math.tan(E/2) / (math.sqrt((1 - e) / (1 + e))))

    return f
