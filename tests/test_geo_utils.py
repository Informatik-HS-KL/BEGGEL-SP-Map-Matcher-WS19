"""
Description: This is a testfile for geo_utils.py
@date: 11/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""


import unittest

from src.geo_utils import great_circle

from math import sqrt


class TestLinkDistance(unittest.TestCase):

    def test_great_circle(self):
        a = (49.186697, 7.629492)
        b = (49.187240, 7.629905)

        self.assertEqual(round(great_circle(a, b), 5), 0.06743)
