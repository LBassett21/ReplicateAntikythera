import sqlite3

solar_years_to_days = 365.242

class Database():
    database = None
    dbcursor = None

    #def initEvents(self):
    #    self.openDatabase()
    #
    #    self.dbcursor.execute("DROP TABLE IF EXISTS EVENTS")
    #    self.dbcursor.execute(
    #        "CREATE TABLE IF NOT EXISTS EVENTS (
    #         name TEXT PRIMARY KEY NOT NULL,
    #         )")

    def initDatabase(self):
        self.openDatabase()

        # create the tables

        self.dbcursor.execute("DROP TABLE IF EXISTS OBJECTS")
        self.dbcursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS OBJECTS (
        name TEXT PRIMARY KEY NOT NULL,
        orbital_primary TEXT NOT NULL,
        semi_major_axis FLOAT NOT NULL,
        eccentricity FLOAT NOT NULL,
        angle_of_inclination FLOAT NOT NULL,
        longitude_of_ascending_node FLOAT NOT NULL,
        argument_of_periapsis FLOAT NOT NULL,
        orbital_period FLOAT NOT NULL,
        time_of_periapsis DATETIME NOT NULL,
        epoch TEXT NOT NULL
        )
        '''
        )
        # a  e  i  omega
        self.addObject("Mercury", "Sun", 0.387098, 0.205630, 7.005, 48.331, 29.124, 88 / solar_years_to_days, "2026-08-13", "J2000")
        self.addObject("Venus", "Sun", 0.723332, 0.006772, 3.39458, 76.680, 54.884, 583.92 / solar_years_to_days, "2026-12-25", "J2000")
        self.addObject("Earth", "Sun", 1, 0.0167086, 0.00005, -11.26064, 114.20783, 1, "2023-01-04", "J2000")
        self.addObject("Mars", "Sun", 1.52368055, 0.0934, 1.850, 49.57845, 286.5, 779.94 / solar_years_to_days, "2022-06-21", "J2000")
        self.addObject("Jupiter", "Sun", 5.2038, 0.0489, 1.303, 100.464, 273.867, 398.88 / solar_years_to_days, "2023-01-21", "J2000") 
        self.addObject("Neptune", "Sun", 30.07, 0.008678, 1.770, 131.783, 273.187, 367.49 / solar_years_to_days, "2042-09-04", "J2000")
        self.addObject("Saturn", "Sun", 9.5826, 0.0565, 2.485, 113.665, 339.392, 10759 / solar_years_to_days, "2032-11-29", "J2000")
        self.addObject("Uranus", "Sun", 19.19126, 0.04717, 0.773, 74.006, 96.998857, 30688.5 / solar_years_to_days, "2050-08-17", "J2000")
        self.addObject("Moon", "Earth", 0.00257, 0.0549, 5.145, 0, 0, 29.530 / solar_years_to_days, "2023-01-04", "J2000") 

        self.database.commit()

    def openDatabase(self):
        self.database = sqlite3.connect("antikythera_database.db")
        self.dbcursor = self.database.cursor()

    def getCursor(self):
        return self.database.cursor()

    def closeDatabase(self):
        self.database.commit()
        self.database.close()

    def addObject(self, name, orbital_primary, a, e, i, La, w, T, dop, epoch):
        self.dbcursor.execute(
           f"""
            INSERT INTO OBJECTS VALUES(
            "{name}",
            "{orbital_primary}",
            {a},
            {e},
            {i},
            {La},
            {w},
            {T},
            "{dop}",
            "{epoch}"
            )
           """
        )

    def removeObject(self, name):
        self.dbcursor.execute(f"DELETE FROM OBJECTS WHERE name = {name}")

    def fetchValue(self, object, column):
        self.dbcursor.execute(
            f"""
            SELECT {column}
            FROM OBJECTS
            WHERE name = "{object}"
            """
        )

        result = self.dbcursor.fetchone()[0]
        return result
