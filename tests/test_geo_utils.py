"""
Description: This is a testfile for geo_utils.py
@date: 11/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""


import unittest
from src.geo_utils import great_circle, number_is_in_interval, overlap_intervals


class TestGeoUtils(unittest.TestCase):

    def test_great_circle(self):
        a = (50.1, 90.1)
        b = (60.2, 110.45)

        self.assertEqual(round(great_circle(a, b), 2), 1700095.67)

    def test_number_is_in_interval(self):
        interval_1 = (0, 5)
        self.assertTrue(number_is_in_interval(3, interval_1, 7, excluding_endpoints=True))
        self.assertTrue(number_is_in_interval(4.9, interval_1, 10, excluding_endpoints=True))
        self.assertTrue(number_is_in_interval(0, interval_1, 40.9, excluding_endpoints=False))
        self.assertTrue(number_is_in_interval(5, interval_1, 13, excluding_endpoints=False))
        self.assertFalse(number_is_in_interval(0, interval_1, 40.9, excluding_endpoints=True))
        self.assertFalse(number_is_in_interval(5, interval_1, 13, excluding_endpoints=True))
        self.assertFalse(number_is_in_interval(-2, interval_1, 9, excluding_endpoints=True))

        interval_2 = (3, -6)
        self.assertTrue(number_is_in_interval(4, interval_2, 8, excluding_endpoints=True))
        self.assertTrue(number_is_in_interval(-7, interval_2, 10, excluding_endpoints=True))
        self.assertTrue(number_is_in_interval(3, interval_2, 20, excluding_endpoints=False))
        self.assertTrue(number_is_in_interval(-6, interval_2, 7, excluding_endpoints=False))
        self.assertFalse(number_is_in_interval(3, interval_2, 20, excluding_endpoints=True))
        self.assertFalse(number_is_in_interval(-6, interval_2, 7, excluding_endpoints=True))
        self.assertFalse(number_is_in_interval(-5, interval_2, 9.5, excluding_endpoints=True))

    def test_overlap_intervals(self):
        self.assertTrue(overlap_intervals((1, 2), (1, 2), 40))
        self.assertTrue(overlap_intervals((5, 10), (7, 30), 40))
        self.assertTrue(overlap_intervals((1, 5), (2, -3), 10))
        self.assertTrue(overlap_intervals((0, 10), (2, 3), 13))
        self.assertTrue(overlap_intervals((0, 10), (-2, 0.5), 10))
        self.assertFalse(overlap_intervals((3, 9), (9, 10), 10))
        self.assertFalse(overlap_intervals((2.5, 7), (-3, 2.5), 9))
        self.assertFalse(overlap_intervals((0, 1), (2, 3), 5))
        self.assertFalse(overlap_intervals((0, 1), (2, 3), 5))
