"""

"""
import unittest
from src.models import Node
from src.models import Link

class TestNode(unittest.TestCase):

    def test(self):
        n = Node(1, (2.4, 2.5))
        l = Link(n, Node(2, (47.4, 45.5)))

        self.assertEqual(n.get_id(), 1)
        self.assertEqual(n.get_lat(), 2.4)
        self.assertEqual(n.get_lon(), 2.5)
        self.assertEqual(n.get_lon(), 2.5)

        self.assertEqual(n.get_latlon(), (2.4, 2.5))
        self.assertEqual(n.add_link(l), l in n.get_links())