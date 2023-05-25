# based on: http://cosinekitty.com/astronomy.js
import math
from math import pi

class SphericalCoordinates:
    def __init__(self, long, lat, rad):
        self.longitude = long
        self.latitude = lat
        self.radius = rad

rad_to_deg = 180.0 / math.pi
deg_to_rad = math.pi / 180.0
rad_to_hours = 12.0 / math.pi
hours_to_rad = math.pi / 12.0

def CosDeg(deg):
    return math.cos(rad_to_deg * deg)

def SinDeg(deg):
    return math.sin(rad_to_deg * deg)

def TanDeg(deg):
    return math.tan(rad_to_deg * deg)

def CosHour(hr):
    return math.cos(rad_to_hours * hr)

def SinHour(hr):
    return math.sin(rad_to_hours * hr)

def ArctanDeg(x, y):
    return rad_to_deg * math.atan2(x, y)

def fixCycle(ang, cycle):
    fraction = ang / cycle
    return cycle * (fraction - math.floor(fraction))

def fixHour(hr):
    return fixCycle(hr, 24.0)

def fixDeg(deg):
    return fixCycle(deg, 360)

def Polar(x, y, z):
    rho = (x * x) + (y * y)
    rad = math.sqrt(rho + (z * z))
    phi = ArctanDeg(y, z)
    if (phi < 0):
        phi = phi + 360.0
    rho = math.sqrt(rho)
    theta = ArctanDeg(z, rho)
    return SphericalCoordinates(phi, theta, rad)

def DMS(x):
    a = type('', (), {})()
    a.negative = (x < 0)
    if (a.negative):
        x = -x
    a.degrees = math.floor(x)
    x = 60.0 * (x - a.degrees)
    a.minutes = math.floor(x)
    x = 60.0 * (x - a.minutes)
    a.seconds = round(10.0 * x, 1)
    if (a.seconds == 60):
        a.seconds = 0
        if ((a.minutes +=1) == 60):
            a.minutes = 0
            a.degrees += 1
    
    return a

def DMM(x):
    a = type('', (), {})()
    a.negative = (x < 0)
    if (a.negative):
        x = -x
    a.degrees = math.floor(x)
    x = 60.0 * (x - a.degrees)
    a.minutes = round(100.0 * x, 2)
    a.seconds = 0.0
    if (a.minutes >= 60.0):
        a.minutes -= 60.0
        a.degrees += 1

    return a

def SafeArcSinInDeg(z):
    absval = abs(z);
    if (absval > 1.0):
        if (absval > 1.00000001):
            print('invalid argument to SafeArcSinInDeg')
        elif (z < -1.0):
            return -90.0
        else:
            return 90.0
    else:
        return rad_to_deg * math.asin(z)

