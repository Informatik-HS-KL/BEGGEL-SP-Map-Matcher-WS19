"""
Description: This is a testfile for geo_hash_wrapper.py
@date: 11/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""


import unittest
from src.geo_hash_wrapper import GeoHashWrapper


# Diese Klasse soll die Funktionalität des GeoHashWrapper testen.
class TestGeohashWrapper(unittest.TestCase):
    pass

    # TODO: Tests for getGeoHash, getGeoHashes, isFirstBboxLargerThanSecondBbox, getBoundingBox, overlap_axis,
    #  firstintervalContainsSecondinterval


if __name__ == '__main__':
    unittest.main()
