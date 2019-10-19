import unittest

from src.models.link_distance import LinkDistance
from src.map_service import MapService
from src.models.link import LinkId
from src.models.node import Node
from src.geo_utils import vector_subtraction, scalar_multiplication, vector_addition, great_circle


class TestLinkDistance(unittest.TestCase):

    def test_link_distance(self):
        """ Test gestaltet sich als schwierig, da mit get_end_node, get_start_node aktuelle daten abgerufen werden
        um dem entgegen zu wirken wird mit relativen Daten getestet.
        Um den Test reibunglos auszuführen mussen die Tests in der Geo Utils reibungslos gelaufen sein und es benötigt
        eine aktive I net verbindung
        """
        service = MapService()
        tile = service.get_tile("u0v3h")

        tile_links = list(tile.get_links())
        if not len(tile_links) > 0:
            raise Exception("Neuer Geohash nötig um zu testen")

        # Test 1 Point is start node
        link = tile_links[0]
        node = link.get_start_node()
        dist = LinkDistance(node.get_latlon(), link)
        self.assertEqual(0, dist.get_fraction())
        self.assertEqual(0, dist.get_distance())

        # Test 2 Point is end node
        link = tile_links[0]
        node = link.get_end_node()
        dist = LinkDistance(node.get_latlon(), link)
        self.assertEqual(1, dist.get_fraction())
        self.assertEqual(0, dist.get_distance())

        # Test 3 Point above link
        link = tile_links[0]
        # lat lon liegt immer auf der hälfte der Strecke durch Richtungsvector * 0.5
        lat_lon = scalar_multiplication(
            0.5, vector_subtraction(link.get_end_node().get_latlon(), link.get_start_node().get_latlon()))
        dist = LinkDistance(lat_lon, link)
        self.assertEqual(0.5, dist.get_fraction())
        self.assertEqual(0, dist.get_distance())


        # # Test 3 Abstandsberechnung über Orthogonal proj.
        # link = tile_links[0]
        # # lat lon liegt immer auf der hälfte der Strecke + 0.5 lat durch Richtungsvector * 0.5 + (1,0)
        # lat_lon = scalar_multiplication(
        #     0.5,
        #     vector_addition(
        #         (1, 0),
        #         vector_subtraction(link.get_end_node().get_latlon(), link.get_start_node().get_latlon())
        #     )
        # )
        # dist = LinkDistance(lat_lon, link)
        # self.assertEqual(x, dist.get_fraction())
        # self.assertEqual(x, dist.get_distance())
        # print(dist.get_fraction())
        # print(dist.get_distance())

        # Test 3 Point auserhalb der Strecke ohne Orthogonal proj.
        link = tile_links[0]
        lat_lon = vector_addition(link.get_end_node().get_latlon(), link.get_start_node().get_latlon())
        dist = LinkDistance(lat_lon, link)

        self.assertEqual(1, dist.get_fraction())
        self.assertEqual(link.get_length(), dist.get_distance())
        print(dist.get_fraction())
        print(dist.get_distance())