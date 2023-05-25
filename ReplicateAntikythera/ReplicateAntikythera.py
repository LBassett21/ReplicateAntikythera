#constants
meters_per_astronomical_unit = 1.4959787**11
meters_per_earth_equatorial_radius = 6378140.0
earth_rad_per_astronomical_unit = meters_per_astronomical_unit / meters_per_earth_equatorial_radius



class Satellite:
    def __init__(self):
        print("Satellite constructor")

class Planet(Satellite):
    def __init__(self):
        print("Planet constructor")

class Moon(Satellite):
    def __init__(self):
        print("Moon constructor")

class Asteroid:
    def __init__(self):
        print("Asteroid constructor")

p = Planet();