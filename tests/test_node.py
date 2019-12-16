"""
Description: This is a testfile for node.py
@date: 11/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""


import unittest
from src.models import Node, NodeId
from src.models import Link


class TestNode(unittest.TestCase):

    def test(self):
        n = Node(1, (2.4, 2.5))
        link = Link(NodeId(1, ""), Node(NodeId(2, ""), (47.4, 45.5)))

        self.assertEqual(n.get_id(), 1)
        self.assertEqual(n.get_lat(), 2.4)
        self.assertEqual(n.get_lon(), 2.5)
        self.assertEqual(n.get_lon(), 2.5)

        self.assertEqual(n.get_latlon(), (2.4, 2.5))
        n.add_link(link)
        self.assertTrue(link in n.get_links())
