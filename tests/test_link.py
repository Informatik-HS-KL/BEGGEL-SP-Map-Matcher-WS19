import unittest

from src.models.link_distance import LinkDistance
from src.map_service import MapService
from src.geo_utils import vector_subtraction, scalar_multiplication, vector_addition, great_circle


class TestLinkDistance(unittest.TestCase):

    def test_get_start_node(self):
        """"""

    def test_get_end_node(self):
        """"""

    def test_get_links_at_start_node(self):
        """
        """
        service = MapService()
        tile = service.get_tile("u0v3h")

        tile_links = list(tile.get_links())
        if not len(tile_links) > 0:
            raise Exception("Neuer Geohash nötig um zu testen")


        self.assertAlmostEqual(0, dist.get_fraction(), 10)
        self.assertAlmostEqual(0, dist.get_distance(), 10)

    def test_get_links_at_end_node(self):
        """
        """
        service = MapService()
        tile = service.get_tile("u0v3h")

        tile_links = list(tile.get_links())
        if not len(tile_links) > 0:
            raise Exception("Neuer Geohash nötig um zu testen")

        self.assertAlmostEqual(0, dist.get_fraction(), 10)
        self.assertAlmostEqual(0, dist.get_distance(), 10)
