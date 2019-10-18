import unittest

from src.models.node import Node, NodeId
from src.geo_utils import great_circle


class TestLinkDistance(unittest.TestCase):

    def test_great_circle(self):
        a = Node(NodeId("", ""), (49.186697, 7.629492))
        b = Node(NodeId("", ""), (49.187240, 7.629905))

        self.assertEqual(round(great_circle(a, b), 5), 0.06743)
