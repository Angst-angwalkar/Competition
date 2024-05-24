import unittest
from runner import Runner
from custom_errors import *

class TestRunner(unittest.TestCase):
    def test_runner_initialization(self):
        runner = Runner('Elijah', 18, 'Australia', 5.8, 4.4)
        
        # Check the initialization of attributes
        self.assertEqual(runner.name, 'Elijah')
        self.assertEqual(runner.age, 18)
        self.assertEqual(runner.country, 'Australia')
        self.assertEqual(runner.sprint_speed, 5.8)
        self.assertEqual(runner.endurance_speed, 4.4)
        self.assertEqual(runner.energy, 1000)

# if __name__ == '__main__':
#     unittest.main()



import unittest

class TestRunner(unittest.TestCase):
    def setUp(self):
        self.runner = Runner('Elijah', 18, 'Australia', 5.8, 4.4)

    def test_drain_energy(self):
        self.runner.drain_energy(100)
        self.assertEqual(self.runner.energy, 900)
        with self.assertRaises(CustomValueError):
            self.runner.drain_energy(-10)
        with self.assertRaises(CustomValueError):
            self.runner.drain_energy(1500)

    def test_recover_energy(self):
        self.runner.drain_energy(100)
        self.runner.recover_energy(50)
        self.assertEqual(self.runner.energy, 950)
        with self.assertRaises(CustomValueError):
            self.runner.recover_energy(-10)
        with self.assertRaises(CustomValueError):
            self.runner.recover_energy(1500)
        self.runner.recover_energy(1000)
        self.assertEqual(self.runner.energy, 1000)

    def test_run_race(self):
        self.assertAlmostEqual(self.runner.run_race('short', 2), 344.83, places=2)
        self.assertAlmostEqual(self.runner.run_race('long', 2), 454.55, places=2)
        with self.assertRaises(ValueError):
            self.runner.run_race('medium', 2)
        with self.assertRaises(ValueError):
            self.runner.run_race('short', -1)

if __name__ == '__main__':
    unittest.main()