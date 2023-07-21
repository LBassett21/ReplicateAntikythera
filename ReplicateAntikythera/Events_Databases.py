import sqlite3

solar_years_to_days = 365.242
saros_to_days = 6585.3211

class Events():
    database = None
    dbcursor = None

    def initComets(self):
        self.openDatabase()
    
        self.dbcursor.execute("DROP TABLE IF EXISTS COMETS")
        self.dbcursor.execute("""CREATE TABLE IF NOT EXISTS COMETS (
             ID INTEGER PRIMARY KEY NOT NULL,
             name TEXT NOT NULL,
             orbital_primary TEXT NOT NULL,
             semi_major_axis FLOAT NOT NULL,
             eccentricity FLOAT NOT NULL,
             angle_of_inclination FLOAT NOT NULL,
             longitude_of_ascending_node FLOAT NOT NULL,
             argument_of_periapsis FLOAT NOT NULL,
             orbital_period FLOAT NOT NULL,
             time_of_periapsis DATETIME NOT NULL,
             epoch TEXT NOT NULL
             )"""
        )

        self.addComet(1, "Halley's Comet", "Sun", 17.737, 0.96658, 161.96, 59.396, 112.05, 74.7 / solar_years_to_days, "2061-07-28", "2474040.5")
        self.addComet(2, "Hyakutake", "Sun", 1700, 0.9998946, 124.92246, 188.05766, 130.17218, 17000 / solar_years_to_days, "1996-05-01", "2450400.5")
        self.addComet(3, "Hale-Bopp", "Sun", 177, 0.99498, 89.3, 282.47, 130.41, 2520 * solar_years_to_days, "4385-04-01", "JD 2459837.5")
        self.addComet(4, "Comet Borrelly", "Sun", 3.61, 0.6377, 29.3, 74.31, 351.86, 6.85 * solar_years_to_days, "2028-12-11", "JD 2459800.5")
        self.addComet(5, "Comet Encke", "Sun", 2.2195, 0.8471, 11.35, 334.03, 187.2, 3.31 * solar_years_to_days, "2023-10-22", "2023-02-25")

        self.database.commit()

    def initAlignment(self):
        self.openDatabase()

        self.dbcursor.execute("DROP TABLE IF EXISTS ALIGNMENT")
        self.dbcursor.execute("""CREATE TABLE IF NOT EXISTS ALIGNMENT (
             ID INTEGER PRIMARY KEY NOT NULL,
             date_aligned DATETIME NOT NULL,
             mercury BOOLEAN NOT NULL,
             venus BOOLEAN NOT NULL,
             earth BOOLEAN NOT NULL,
             mars BOOLEAN NOT NULL,
             jupiter BOOLEAN NOT NULL,
             neptune BOOLEAN NOT NULL,
             saturn BOOLEAN NOT NULL,
             uranus BOOLEAN NOT NULL,
             moon BOOLEAN NOT NULL
             )"""
        )


        self.database.commit()

    def initSolarEclipses(self):
        self.openDatabase()

        self.dbcursor.execute("DROP TABLE IF EXISTS SOLAR_ECLIPSES")
        self.dbcursor.execute("""CREATE TABLE IF NOT EXISTS SOLAR_ECLIPSES (
             ID INTEGER PRIMARY KEY NOT NULL,
             date_observed DATETIME NOT NULL,
             type TEXT NOT NULL,
             saros FLOAT NOT NULL,
             duration TEXT NOT NULL
             )"""
        )
        
        self.addSolarEclipse(1, "2001-06-21", "Total", 127 * saros_to_days, "4.57")
        self.addSolarEclipse(2, "2001-12-14", "Annular", 132 * saros_to_days, "3.53")
        self.addSolarEclipse(3, "2002-06-10", "Annular", 137 * saros_to_days, "0.23")
        self.addSolarEclipse(4, "2002-12-04", "Total", 142 * saros_to_days, "2.04")
        self.addSolarEclipse(5, "2003-05-31", "Annular", 147 * saros_to_days, "3.37")

        self.database.commit()

    def initLunarEclipses(self):
        self.openDatabase()

        self.dbcursor.execute("DROP TABLE IF EXISTS LUNAR_ECLIPSES")
        self.dbcursor.execute("""CREATE TABLE IF NOT EXISTS LUNAR_ECLIPSES (
             ID INTEGER PRIMARY KEY NOT NULL,
             date_observed DATETIME NOT NULL,
             type TEXT NOT NULL,
             saros FLOAT NOT NULL,
             duration TEXT NOT NULL
             )"""
        )

        self.addLunarEclipse(1, "1999-07-28", "Partial", 119 * saros_to_days, "144.00")
        self.addLunarEclipse(2, "2000-01-21", "Total", 124 * saros_to_days, "78.00")
        self.addLunarEclipse(3, "2000-07-16", "Total", 129 * saros_to_days, "106.00")
        self.addLunarEclipse(4, "2001-01-09", "Total", 134 * saros_to_days, "62.00")
        self.addLunarEclipse(5, "2001-07-05", "Partial", 139 * saros_to_days, "160.00")

        self.database.commit()

    # Only includes major NASA space launches
    def initSpaceLaunches(self):
        self.openDatabase()

        self.dbcursor.execute("DROP TABLE IF EXISTS SPACE_LAUNCHES")
        self.dbcursor.execute("""CREATE TABLE IF NOT EXISTS SPACE_LAUNCHES (
             ID INTEGER PRIMARY KEY NOT NULL,
             name TEXT NOT NULL,
             start_date TEXT NOT NULL,
             end_date TEXT NOT NULL,
             special_note TEXT NOT NULL
             )"""
        )

        self.addSpaceLaunch(1, "Project Mercury", "1958", "1963", "First U.S. crewed program")
        self.addSpaceLaunch(2, "Project Gemini", "1961", "1966", "Program used to practice space rendevous and EVAs")
        self.addSpaceLaunch(3, "Apollo Program", "1960", "1972", "Landed first humans on the moon")
        self.addSpaceLaunch(4, "Skylab", "1964", "1974", "First American space station")
        self.addSpaceLaunch(5, "Apollo-Soyuz", "1971", "1975", "Joint with Soviet Union")
        self.addSpaceLaunch(6, "Space Shuttle Program", "1972", "2011", "First missions in which a spacecraft was reused")
        self.addSpaceLaunch(7, "Shuttle-Mir Program", "1993", "1998", "Russian partnership")
        self.addSpaceLaunch(8, "International Space Station", "1993", "(Present)", "Joint with Roscosmos, CSA, ESA, and JAXA")
        self.addSpaceLaunch(9, "Commercial Crew Program", "2011", "(Present)", "Current program (as of 2023) to shuttle Americans to the ISS")
        self.addSpaceLaunch(10, "Artemis Program", "2017", "(Present)", "Current program (as of 2023) to bring humans to the Moon again")

        self.database.commit()


    def openDatabase(self):
        self.database = sqlite3.connect("antikythera_database.db")
        self.dbcursor = self.database.cursor()

    def getCursor(self):
        return self.database.cursor()

    def closeDatabase(self):
        self.database.commit()
        self.database.close()

    def addComet(self, ID, name, orbital_primary, a, e, i, La, w, T, dop, epoch):
        self.dbcursor.execute(
           f"""
            INSERT INTO COMETS VALUES(
            {ID},
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

    def addSolarEclipse(self, ID, date_observed, type, saros, duration):
        self.dbcursor.execute(
           f"""
            INSERT INTO SOLAR_ECLIPSES VALUES(
            {ID},
            "{date_observed}",
            "{type}",
            {saros},
            "{duration}"
            )
           """
        )

    def addLunarEclipse(self, ID, date_observed, type, saros, duration):
        self.dbcursor.execute(
           f"""
            INSERT INTO LUNAR_ECLIPSES VALUES(
            "{ID}",
            "{date_observed}",
            "{type}",
            {saros},
            "{duration}"
            )
           """
        )

    def addAlignment(self, ID, date, mercury, venus, earth, mars, jupiter, saturn, neptune, uranus, moon):
        self.dbcursor.execute(
           f"""
            INSERT INTO LUNAR_ECLIPSES VALUES(
            "{ID}",
            "{date}",
            "{mercury}",
            {venus},
            "{earth}",
            "{mars}",
            "{jupiter}",
            "{saturn}",
            "{neptune}",
            "{uranus}",
            "{moon}"
            )
           """
        )

    def addSpaceLaunch(self, ID, name, start, end, note):
        self.dbcursor.execute(
           f"""
            INSERT INTO SPACE_LAUNCHES VALUES(
            "{ID}",
            "{name}",
            "{start}",
            "{end}",
            "{note}"
            )
           """
        )

    def fetchComet(self, object, column):
        self.dbcursor.execute(
            f"""
            SELECT {column}
            FROM COMETS
            WHERE name = "{object}"
            """
        )

    def fetchAlignment(self, object, column):
        self.dbcursor.execute(
            f"""
            SELECT {column}
            FROM ALIGNMENT
            WHERE name = "{object}"
            """
        )

    def fetchSolarEclipse(self, object, column):
        self.dbcursor.execute(
            f"""
            SELECT {column}
            FROM SOLAR_ECLIPSES
            WHERE name = "{object}"
            """
        )

    def fetchLunarEclipse(self, object, column):
        self.dbcursor.execute(
            f"""
            SELECT {column}
            FROM LUNAR_ECLIPSES
            WHERE name = "{object}"
            """
        )

    def fetchSpaceLaunch(self, object, column):
        self.dbcursor.execute(
            f"""
            SELECT {column}
            FROM SPACE_LAUNCHES
            WHERE name = "{object}"
            """
        )

        result = self.dbcursor.fetchone()[0]
        return result
