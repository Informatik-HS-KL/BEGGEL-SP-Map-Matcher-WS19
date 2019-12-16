"""
Description: This is a testfile for map_service.py
@date: 11/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

import unittest
from src.map_service import MapService
from src.utils.overpass_wrapper import OverpassWrapperClientSide, OverpassWrapperServerSide
from src.models import BoundingBox


class TestMapService(unittest.TestCase):

    def test_map_service(self):
        ms = MapService()
        ms.set_overpass_wrapper(OverpassWrapperServerSide(ms.get_config()))

        nodes = ms.get_nodes_in_bounding_box(BoundingBox(49.4790812638, 7.7679723593, 49.482845546, 7.7734850962))
        for node in nodes[:5]:
            ms.get_node(node.get_id())
            node.to_geojson()
            node.get_tags()
            node.to_wkt()

        ms.set_overpass_wrapper(OverpassWrapperClientSide(ms.get_config()))
        links = ms.get_links_in_bounding_box(BoundingBox(49.4796172829,  8.4784880064, 49.5097706833, 8.5317118292))

        for link in links[:5]:
            self.assertEqual(ms.get_link_by_id(link.get_id()), link)
            ms.get_links(link.get_way_osm_id())
            link.to_geojson()
            link.to_wkt()
            link.get_tags()

        link_distances = ms.get_linkdistances_in_radius((49.4298243272, 7.7204445597), 500)

        for ld in link_distances:
            ld.get_link().to_geojson()
            ld.get_distance()
            ld.get_fraction()
            ld.get_point()
