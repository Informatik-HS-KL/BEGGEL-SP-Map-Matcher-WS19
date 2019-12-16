"""
Description: This is a testfile for link.py
@date: 11/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

import unittest

from src.map_service import MapService
from src.models.node import NodeId


class TestLinkDistance(unittest.TestCase):

    def test_get_start_node(self):
        """"""

    def test_get_end_node(self):
        """"""

    def test_get_links_at_start_node(self):
        """
        Geohash:

        Link1:
        263081703 SN - Id: u0v978d9vsmj
        --> Abgehende Links:
            240764576 SN-Id:u0v978d9vsmj
            240764576 SN-Id:u0v978eeuc0x
            263081704 SN-Id:u0v978d9vsmj
        """

        service = MapService()
        tile = service.get_tile("u0v97")

        nid = NodeId(290512608, "u0v978d9vsmj")
        link = service.get_link(263081703, nid)

        sn_links_test = {
            service.get_link(240764576, NodeId(290512634, "u0v978eeuc0x")),
            service.get_link(263081704, NodeId(290512608, "u0v978d9vsmj")),
            service.get_link(240764576, NodeId(290512608, "u0v978d9vsmj")),
        }

        sn_links = set(link.get_links_at_start_node())
        self.assertSetEqual(sn_links, sn_links_test)

    def test_get_links_at_end_node(self):
        """
        Die Straßen sind real existierende Strasen in dem angegebenen Geohash
        Die Endlink wurden manuell in der Karte ermittels

        --> Abgehende Links andere Seite
            263081708 SN-Id:u0v9786ytguz
            240764572 SN-Id:u0v9786vztrm

        :return:
        """

        service = MapService()
        tile = service.get_tile("u0v97")

        nid = NodeId(290512608, "u0v978d9vsmj")
        link = service.get_link(263081703, nid)

        en_links_test = {
            service.get_link(263081708, NodeId(2687039625, "u0v9786ytguz")),
            service.get_link(240764572, NodeId(290512604, "u0v9786vztrm")),
        }
        en_links = set(link.get_links_at_end_node())

        self.assertSetEqual(en_links, en_links_test)

