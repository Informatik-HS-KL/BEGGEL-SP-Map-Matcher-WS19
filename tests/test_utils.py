"""
Description: This is a testfile for geo_utils.py
@date: 11/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
Todo: merge this file with test_geo_utils.py
"""


import unittest
import src.geo_utils as ut


class TestUtils(unittest.TestCase):
    def test_number_is_in_interval(self):
        interval_1 = (0, 5)
        self.assertTrue(ut.number_is_in_interval(3, interval_1, 7, excluding_endpoints=True))
        self.assertTrue(ut.number_is_in_interval(4.9, interval_1, 10, excluding_endpoints=True))
        self.assertTrue(ut.number_is_in_interval(0, interval_1, 40.9, excluding_endpoints=False))
        self.assertTrue(ut.number_is_in_interval(5, interval_1, 13, excluding_endpoints=False))
        self.assertFalse(ut.number_is_in_interval(0, interval_1, 40.9, excluding_endpoints=True))
        self.assertFalse(ut.number_is_in_interval(5, interval_1, 13, excluding_endpoints=True))
        self.assertFalse(ut.number_is_in_interval(-2, interval_1, 9, excluding_endpoints=True))

        interval_2 = (3, -6)
        self.assertTrue(ut.number_is_in_interval(4, interval_2, 8, excluding_endpoints=True))
        self.assertTrue(ut.number_is_in_interval(-7, interval_2, 10, excluding_endpoints=True))
        self.assertTrue(ut.number_is_in_interval(3, interval_2, 20, excluding_endpoints=False))
        self.assertTrue(ut.number_is_in_interval(-6, interval_2, 7, excluding_endpoints=False))
        self.assertFalse(ut.number_is_in_interval(3, interval_2, 20, excluding_endpoints=True))
        self.assertFalse(ut.number_is_in_interval(-6, interval_2, 7, excluding_endpoints=True))
        self.assertFalse(ut.number_is_in_interval(-5, interval_2, 9.5, excluding_endpoints=True))
        
    def test_overlap_intervals(self):
        self.assertTrue(ut.overlap_intervals((1, 2), (1, 2), 40))
        self.assertTrue(ut.overlap_intervals((5, 10), (7, 30), 40))
        self.assertTrue(ut.overlap_intervals((1, 5), (2, -3), 10))
        self.assertTrue(ut.overlap_intervals((0, 10), (2, 3), 13))
        self.assertTrue(ut.overlap_intervals((0, 10), (-2, 0.5), 10))
        self.assertFalse(ut.overlap_intervals((3, 9), (9, 10), 10))
        self.assertFalse(ut.overlap_intervals((2.5, 7), (-3, 2.5), 9))
        self.assertFalse(ut.overlap_intervals((0, 1), (2, 3), 5))
        self.assertFalse(ut.overlap_intervals((0, 1), (2, 3), 5))