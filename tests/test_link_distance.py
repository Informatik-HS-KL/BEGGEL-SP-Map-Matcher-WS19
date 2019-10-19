import unittest

from src.models.link_distance import LinkDistance
from src.map_service import MapService
from src.geo_utils import vector_subtraction, scalar_multiplication, vector_addition, great_circle


class TestLinkDistance(unittest.TestCase):

    def test_link_distance(self):
        """ Test gestaltet sich als schwierig, da mit get_end_node, get_start_node aktuelle Daten abgerufen werden.
        Um dem entgegen zu wirken wird mit relativen Daten getestet.
        Um den Test reibunglos auszuführen, müssen die Tests in test_geo_utils reibungslos gelaufen sein und man benötigt
        eine aktive Internetverbindung.
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
        self.assertAlmostEqual(0, dist.get_fraction(), 10)
        self.assertAlmostEqual(0, dist.get_distance(), 10)

        # Test 2 Point is end node
        link = tile_links[0]
        node = link.get_end_node()
        dist = LinkDistance(node.get_latlon(), link)
        self.assertAlmostEqual(1, dist.get_fraction(), 10)
        self.assertAlmostEqual(0, dist.get_distance(), 10)

        # Test 3 Point above link
        link = tile_links[0]
        # lat lon liegt immer auf der hälfte der Strecke durch Richtungsvector * 0.5
        lat_lon = vector_addition(link.get_start_node().get_latlon(),
                                  scalar_multiplication(0.5,
                                                        vector_subtraction(link.get_end_node().get_latlon(),
                                                                           link.get_start_node().get_latlon())))
        dist = LinkDistance(lat_lon, link)
        self.assertAlmostEqual(0.5, dist.get_fraction(), 10)
        self.assertAlmostEqual(0, dist.get_distance(), 10)


        # Test 4 Abstandsberechnung über Orthogonal proj.
        link = tile_links[0]
        # lat lon liegt immer auf der hälfte der Strecke + 0.5 lat durch Richtungsvector * 0.5 + (1,0)
        richt_vect = scalar_multiplication(0.5,
                                        vector_subtraction(link.get_end_node().get_latlon(),
                                                           link.get_start_node().get_latlon()))

        middle_of_link = vector_addition(link.get_start_node().get_latlon(), richt_vect)
        # Richtungsvector um 90 Grad drehen und zu matched_point addieren
        lat_lon = vector_addition(middle_of_link, (richt_vect[1], richt_vect[0] * (-1)))

        dist = LinkDistance(lat_lon, link)
        self.assertAlmostEqual(0.5, dist.get_fraction(), 10)
        self.assertAlmostEqual(great_circle(middle_of_link,lat_lon), dist.get_distance(), 10)

        # Test 5 Point auserhalb der Strecke ohne Orthogonal proj.
        link = tile_links[0]
        lat_lon = vector_subtraction(scalar_multiplication(2, link.get_end_node().get_latlon()),
                                     link.get_start_node().get_latlon())
        dist = LinkDistance(lat_lon, link)

        self.assertAlmostEqual(1, dist.get_fraction(), 10)
        self.assertEqual(great_circle(lat_lon, link.get_end_node().get_latlon()), dist.get_distance())
