import unittest
from src.GeoHashWrapper import GeoHashWrapper


# Diese Klasse soll die Funktionalität des GeoHashWrapper testen.
class TestGeohashWrapper(unittest.TestCase):

    def test_overlap(self):
        bbox_1 = (-84.7230301687, -88.0437195301, 5.0824166086, -0.1530945301)

        self.assertTrue(GeoHashWrapper.overlap(bbox_1, bbox_1))
        self.assertTrue(GeoHashWrapper.overlap(bbox_1, (-87.2784773532, -42.6921570301, -79.0065948826, 45.1984679699)))
        self.assertTrue(GeoHashWrapper.overlap(bbox_1, (-51.7323307799, -25.9929382801, -12.0476934022, 31.3117492199)))
        self.assertTrue(
            GeoHashWrapper.overlap(bbox_1, (-24.0542820566, -117.3991882801, 23.0718554917, -60.0945007801)))
        self.assertTrue(
            GeoHashWrapper.overlap(bbox_1, (-65.7341451731, -75.9148132801, -36.7457445723, -18.6101257801)))

        self.assertFalse(GeoHashWrapper.overlap(bbox_1, (-69.9633727485, 5.6476867199, -45.2190344304, 62.9523742199)))
        self.assertFalse(GeoHashWrapper.overlap(bbox_1, (9.4406166, 0.9894835949, 70.8418632201, 81.6730773449)))
        self.assertFalse(
            GeoHashWrapper.overlap(bbox_1, (-68.3050695526, -116.3005554676, -56.1258325306, -93.5368835926)))
        self.assertFalse(
            GeoHashWrapper.overlap(bbox_1, (80.2221338128, -171.1443054676, 83.8384658562, -148.3806335926)))

        bbox_2 = (5.0824166086, 107.4250304699, 82.0445552426, -138.6687195301)

        self.assertTrue(GeoHashWrapper.overlap(bbox_2, bbox_2))
        self.assertTrue(GeoHashWrapper.overlap(bbox_2, (48.1017141934, 134.1437804699, 69.7151388143, -179.4499695301)))
        self.assertTrue(GeoHashWrapper.overlap(bbox_2, (-4.7492073269, 157.3469054699, 36.1664456641, -156.2468445301)))
        self.assertTrue(GeoHashWrapper.overlap(bbox_2, (33.2774628304, 92.3078429699, 52.584499321, 122.5422179699)))
        self.assertTrue(GeoHashWrapper.overlap(bbox_2, (80.5595384997, 159.8078429699, 84.0698625322, -169.9577820301)))

        self.assertFalse(
            GeoHashWrapper.overlap(bbox_2, (42.1570571961, -112.3015320301, 58.9002238264, -82.0671570301)))
        self.assertFalse(
            GeoHashWrapper.overlap(bbox_2, (-57.0453872502, -168.1999695301, -9.9772825246, 174.3976867199)))
        self.assertFalse(GeoHashWrapper.overlap(bbox_2, (13.0604370531, 14.2609679699, 77.116122992, 41.6828429699)))
        self.assertFalse(GeoHashWrapper.overlap(bbox_2, (83.3075016401, 139.7687804699, 84.745656882, 162.2687804699)))

    def test_overlap_intervalls(self):
        self.assertTrue(GeoHashWrapper.overlap_intervalls((1, 2), (1, 2), 40))
        self.assertTrue(GeoHashWrapper.overlap_intervalls((5, 10), (7, 30), 40))
        self.assertTrue(GeoHashWrapper.overlap_intervalls((1, 5), (2, -3), 10))
        self.assertTrue(GeoHashWrapper.overlap_intervalls((0, 10), (2, 3), 13))
        self.assertTrue(GeoHashWrapper.overlap_intervalls((0, 10), (-2, 0.5), 10))
        self.assertFalse(GeoHashWrapper.overlap_intervalls((3, 9), (9, 10), 10))
        self.assertFalse(GeoHashWrapper.overlap_intervalls((2.5, 7), (-3, 2.5), 9))
        self.assertFalse(GeoHashWrapper.overlap_intervalls((0, 1), (2, 3), 5))
        self.assertFalse(GeoHashWrapper.overlap_intervalls((0, 1), (2, 3), 5))

    def test_number_is_in_intervall(self):
        intervall_1 = (0, 5)
        self.assertTrue(GeoHashWrapper.number_is_in_intervall(3, intervall_1, 7))
        self.assertTrue(GeoHashWrapper.number_is_in_intervall(4.9, intervall_1, 10))
        self.assertFalse(GeoHashWrapper.number_is_in_intervall(0, intervall_1, 40.9))
        self.assertFalse(GeoHashWrapper.number_is_in_intervall(5, intervall_1, 13))
        self.assertFalse(GeoHashWrapper.number_is_in_intervall(-2, intervall_1, 9))

        intervall_2 = (3, -6)
        self.assertTrue(GeoHashWrapper.number_is_in_intervall(4, intervall_2, 8))
        self.assertTrue(GeoHashWrapper.number_is_in_intervall(-7, intervall_2, 10))
        self.assertFalse(GeoHashWrapper.number_is_in_intervall(3, intervall_2, 20))
        self.assertFalse(GeoHashWrapper.number_is_in_intervall(-6, intervall_2, 7))
        self.assertFalse(GeoHashWrapper.number_is_in_intervall(-5, intervall_2, 9.5))

    # TODO: Tests for getGeoHash, getGeoHashes, isFirstBboxLargerThanSecondBbox, getBoundingBox, overlap_axis


if __name__ == '__main__':
    unittest.main()
