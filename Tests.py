import unittest
import sqlite3
import GUI
import OrbitalDynamics
#import ReplicateAntikythera

class TestGUI(unittest.TestCase):

    def test_date(self):
        date = GUI.curr_date
        self.assertEqual(date, '2024-01-04', 'The start date is wrong')

class TestOrbitalDynamics(unittest.TestCase):

    def test_orbit(self):
        days = OrbitalDynamics.solar_years_to_days
        self.assertEqual(days, 365.242, 'Value from OrbitalDynamics is grabbed incorrectly')

class TestDatabase(unittest.TestCase):

    def test_database(self):
        db_connection = sqlite3.connect("assignment5.db")
        cursor = db_connection.cursor()
        data = cursor.execute("SELECT name FROM OBJECTS WHERE name = Mars")
        self.assertEqual(data, 'Mars', 'The data selected from the database is incorrect')


if (__name__ == "__main__"):
    unittest.main()