import sqlite3

class Database():
    database = None
    dbcursor = None

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

        self.addObject("Earth", "Sun", 1, 0.0167086, 0.00005, -11.26064, 114.20783, 1, "2023-01-04", "J2000")

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

        return self.dbcursor.fetchall()[0][0]
