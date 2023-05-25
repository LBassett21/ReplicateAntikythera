print("Live, love, laugh, Python :)")

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

#This is a test of the github bot for discord