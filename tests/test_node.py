"""
Description: This is a testfile for node.py
@date: 11/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""


import unittest
from src.models import Node, NodeId
from src.models import Link, LinkId


class TestNode(unittest.TestCase):

    def test_node(self):
        n1 = Node(NodeId(1, ""), (2.4, 2.5))
        n2 = Node(NodeId(2, ""), (10, 12))
        n3 = Node(NodeId(3, ""), (-5, 4))

        link = Link(LinkId(233, n1.get_id()), [n1.get_latlon(), n2.get_latlon(), n3.get_latlon()], [n1.get_id(), n2.get_id(), n3.get_id()])

        self.assertEqual(n1.get_id(), NodeId(1, ""))
        self.assertEqual(n1.get_lat(), 2.4)
        self.assertEqual(n1.get_lon(), 2.5)
        self.assertEqual(n1.get_latlon(), (2.4, 2.5))

        n1.add_link(link)
        self.assertTrue(link in n1.get_links())
