"""
Description: This is a testfile for link_distance.py
@date: 11/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

import unittest
from src.models.link_distance import LinkDistance
from src.map_service import MapService


class TestLinkDistance(unittest.TestCase):

    def test_link_distance(self):
        ms = MapService()
        tile = ms.get_tile("u0v3h")

        tile_links = list(tile.get_links())
        if not len(tile_links) > 0:
            raise Exception("Neuer Geohash nötig um zu testen")

        # Test 1 Point is start node
        link = tile_links[0]
        node = link.get_start_node()
        dist = LinkDistance(node.get_latlon(), link)
        self.assertAlmostEqual(0, dist.get_fraction(), 10)
        self.assertAlmostEqual(0, dist.get_distance(), 10)

        # Test 2 Point is end node
        link = tile_links[0]
        node = link.get_end_node()
        dist = LinkDistance(node.get_latlon(), link)
        self.assertAlmostEqual(1, dist.get_fraction(), 10)
        self.assertAlmostEqual(0, dist.get_distance(), 10)
