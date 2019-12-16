"""
Description: This is a testfile for bounding_box.py
@date: 11/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""


import unittest

from src.models import Node, NodeId
from src.models import BoundingBox


class TestBoundingBox(unittest.TestCase):
    def test_overlap(self):
        bbox_1 = BoundingBox(-84.7230301687, -88.0437195301, 5.0824166086, -0.1530945301)

        self.assertTrue(bbox_1.overlap(bbox_1))
        self.assertTrue(bbox_1.overlap(BoundingBox(-87.2784773532, -42.6921570301, -79.0065948826, 45.1984679699)))
        self.assertTrue(bbox_1.overlap(BoundingBox(-51.7323307799, -25.9929382801, -12.0476934022, 31.3117492199)))
        self.assertTrue(
            bbox_1.overlap(BoundingBox(-24.0542820566, -117.3991882801, 23.0718554917, -60.0945007801)))
        self.assertTrue(
            bbox_1.overlap(BoundingBox(-65.7341451731, -75.9148132801, -36.7457445723, -18.6101257801)))

        self.assertFalse(bbox_1.overlap(BoundingBox(-69.9633727485, 5.6476867199, -45.2190344304, 62.9523742199)))
        self.assertFalse(bbox_1.overlap(BoundingBox(9.4406166, 0.9894835949, 70.8418632201, 81.6730773449)))
        self.assertFalse(
            bbox_1.overlap(BoundingBox(-68.3050695526, -116.3005554676, -56.1258325306, -93.5368835926)))
        self.assertFalse(
            bbox_1.overlap(BoundingBox(80.2221338128, -171.1443054676, 83.8384658562, -148.3806335926)))

        bbox_2 = BoundingBox(5.0824166086, 107.4250304699, 82.0445552426, -138.6687195301)

        self.assertTrue(bbox_2.overlap(bbox_2))
        self.assertTrue(bbox_2.overlap(BoundingBox(48.1017141934, 134.1437804699, 69.7151388143, -179.4499695301)))
        self.assertTrue(bbox_2.overlap(BoundingBox(-4.7492073269, 157.3469054699, 36.1664456641, -156.2468445301)))
        self.assertTrue(bbox_2.overlap(BoundingBox(33.2774628304, 92.3078429699, 52.584499321, 122.5422179699)))
        self.assertTrue(bbox_2.overlap(BoundingBox(80.5595384997, 159.8078429699, 84.0698625322, -169.9577820301)))

        self.assertFalse(
            bbox_2.overlap(BoundingBox(42.1570571961, -112.3015320301, 58.9002238264, -82.0671570301)))
        self.assertFalse(
            bbox_2.overlap(BoundingBox(-57.0453872502, -168.1999695301, -9.9772825246, 174.3976867199)))
        self.assertFalse(bbox_2.overlap(BoundingBox(13.0604370531, 14.2609679699, 77.116122992, 41.6828429699)))
        self.assertFalse(bbox_2.overlap(BoundingBox(83.3075016401, 139.7687804699, 84.745656882, 162.2687804699)))

    def test_contains_bbox(self):
        bbox_1 = BoundingBox(0.513282437, 0.0159996796, 84.0942163677, 89.3608800602)
        self.assertTrue(bbox_1.contains_bbox(bbox_1))
        self.assertTrue(bbox_1.contains_bbox(BoundingBox(
            21.6647872488, 15.5327550602, 65.2416229192, 89.3608800602)))
        self.assertTrue(bbox_1.contains_bbox(BoundingBox(
            21.6647872488, 15.5327550602, 65.2416229192, 67.5640050602)))
        self.assertTrue(bbox_1.contains_bbox(BoundingBox(
            60.4394489351, 1.4702550602, 73.7411216463, 53.5015050602)))

        self.assertFalse(bbox_1.contains_bbox(BoundingBox(
            64.0372106287, 111.1577550602, 75.7716930825, -160.2484949398)))
        self.assertFalse(bbox_1.contains_bbox(BoundingBox(
            -63.6817377051, 4.9858800602, -14.894669805, 93.5796300602)))
        self.assertFalse(bbox_1.contains_bbox(BoundingBox(
            -11.8165911863, -44.2328699398, 48.95656608, 44.3608800602)))

        bbox_2 = BoundingBox(-66.9097288411, 89.3608800602, 0.403422688, -132.8266199398)
        self.assertTrue(bbox_2.contains_bbox(bbox_2))
        self.assertTrue(bbox_2.contains_bbox(BoundingBox(
            -66.9097288411, 89.3608800602, 0.403422688, 162.4858800602)))
        self.assertTrue(bbox_2.contains_bbox(BoundingBox(
            -60.0389493929, 104.1265050602, -18.9299746389, 161.7827550602)))
        self.assertTrue(bbox_2.contains_bbox(BoundingBox(
            -35.1314035932, 162.1343175602, -6.613091808, -169.0375574398)))

        self.assertFalse(bbox_2.contains_bbox(BoundingBox(
            -35.1314035932, 162.1343175602, 16.3488238092, -169.0375574398)))
        self.assertFalse(bbox_2.contains_bbox(BoundingBox(
            -18.5970967976, -33.3344324398, 33.4747130173, 53.5015050602)))
        self.assertFalse(bbox_2.contains_bbox(BoundingBox(
            -69.9426596955, 63.5210363102, -40.807816162, 150.3569738102)))

    def test_contains_node(self):
        """
        :return:
        """
        bbox = BoundingBox(50.0, 10.0, 50.5, 12.0)
        # Liegen in der bbox
        n1 = Node(NodeId(1, ""), (50.0, 10.0))
        n2 = Node(NodeId(2, ""), (50.0, 11.0))
        n3 = Node(NodeId(3, ""), (50.2, 10.0))
        n4 = Node(NodeId(4, ""), (50.5, 11.0))

        # Liegen nicht in der bbox
        n5 = Node(NodeId(5, ""), (49.0, 9.0))
        n6 = Node(NodeId(6, ""), (49.0, 10.0))
        n7 = Node(NodeId(7, ""), (50.0, 9.0))

        self.assertTrue(bbox.contains_node(n1))
        self.assertTrue(bbox.contains_node(n2))
        self.assertTrue(bbox.contains_node(n3))
        self.assertTrue(bbox.contains_node(n4))
        self.assertTrue(bbox.contains_node(Node(NodeId(8, ""), (bbox.south, bbox.west))))

        self.assertFalse(bbox.contains_node(n5), False)
        self.assertFalse(bbox.contains_node(n6), False)
        self.assertFalse(bbox.contains_node(n7), False)
