import unittest

from src.models.node import Node, NodeId
from src.link_distance import distance_between_nodes


class TestLinkDistance(unittest.TestCase):
    def test__get_nearest_point_on_link_to_point(self):
        pass

    def test_distance_between_nodes(self):
        a = Node(NodeId("", ""), (49.186697, 7.629492))
        b = Node(NodeId("", ""), (49.187240, 7.629905))

        self.assertEqual(round(distance_between_nodes(a, b), 5), 0.06743)

    def test_distance_node_link(self):
        pass