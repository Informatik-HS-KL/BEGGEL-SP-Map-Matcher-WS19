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

    def test_overlap_intervals(self):
        self.assertTrue(GeoHashWrapper.overlap_intervals((1, 2), (1, 2), 40))
        self.assertTrue(GeoHashWrapper.overlap_intervals((5, 10), (7, 30), 40))
        self.assertTrue(GeoHashWrapper.overlap_intervals((1, 5), (2, -3), 10))
        self.assertTrue(GeoHashWrapper.overlap_intervals((0, 10), (2, 3), 13))
        self.assertTrue(GeoHashWrapper.overlap_intervals((0, 10), (-2, 0.5), 10))
        self.assertFalse(GeoHashWrapper.overlap_intervals((3, 9), (9, 10), 10))
        self.assertFalse(GeoHashWrapper.overlap_intervals((2.5, 7), (-3, 2.5), 9))
        self.assertFalse(GeoHashWrapper.overlap_intervals((0, 1), (2, 3), 5))
        self.assertFalse(GeoHashWrapper.overlap_intervals((0, 1), (2, 3), 5))

    def test_number_is_in_interval(self):
        interval_1 = (0, 5)
        self.assertTrue(GeoHashWrapper.number_is_in_interval(3, interval_1, 7, excluding_endpoints=True))
        self.assertTrue(GeoHashWrapper.number_is_in_interval(4.9, interval_1, 10, excluding_endpoints=True))
        self.assertTrue(GeoHashWrapper.number_is_in_interval(0, interval_1, 40.9, excluding_endpoints=False))
        self.assertTrue(GeoHashWrapper.number_is_in_interval(5, interval_1, 13, excluding_endpoints=False))
        self.assertFalse(GeoHashWrapper.number_is_in_interval(0, interval_1, 40.9, excluding_endpoints=True))
        self.assertFalse(GeoHashWrapper.number_is_in_interval(5, interval_1, 13, excluding_endpoints=True))
        self.assertFalse(GeoHashWrapper.number_is_in_interval(-2, interval_1, 9, excluding_endpoints=True))

        interval_2 = (3, -6)
        self.assertTrue(GeoHashWrapper.number_is_in_interval(4, interval_2, 8, excluding_endpoints=True))
        self.assertTrue(GeoHashWrapper.number_is_in_interval(-7, interval_2, 10, excluding_endpoints=True))
        self.assertTrue(GeoHashWrapper.number_is_in_interval(3, interval_2, 20, excluding_endpoints=False))
        self.assertTrue(GeoHashWrapper.number_is_in_interval(-6, interval_2, 7, excluding_endpoints=False))
        self.assertFalse(GeoHashWrapper.number_is_in_interval(3, interval_2, 20, excluding_endpoints=True))
        self.assertFalse(GeoHashWrapper.number_is_in_interval(-6, interval_2, 7, excluding_endpoints=True))
        self.assertFalse(GeoHashWrapper.number_is_in_interval(-5, interval_2, 9.5, excluding_endpoints=True))

    def test_firstBboxContainsSecondBbox(self):
        bbox_1 = (0.513282437, 0.0159996796, 84.0942163677, 89.3608800602)
        self.assertTrue(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_1, bbox_1))
        self.assertTrue(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_1, (21.6647872488, 15.5327550602, 65.2416229192, 89.3608800602)))
        self.assertTrue(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_1, (21.6647872488, 15.5327550602, 65.2416229192, 67.5640050602)))
        self.assertTrue(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_1, (60.4394489351, 1.4702550602, 73.7411216463, 53.5015050602)))

        self.assertFalse(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_1, (64.0372106287, 111.1577550602, 75.7716930825, -160.2484949398)))
        self.assertFalse(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_1, (-63.6817377051, 4.9858800602, -14.894669805, 93.5796300602)))
        self.assertFalse(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_1, (-11.8165911863, -44.2328699398, 48.95656608, 44.3608800602)))

        bbox_2 = (-66.9097288411, 89.3608800602, 0.403422688, -132.8266199398)
        self.assertTrue(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_2, bbox_2))
        self.assertTrue(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_2, (-66.9097288411, 89.3608800602, 0.403422688, 162.4858800602)))
        self.assertTrue(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_2, (-60.0389493929, 104.1265050602, -18.9299746389, 161.7827550602)))
        self.assertTrue(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_2, (-35.1314035932, 162.1343175602, -6.613091808, -169.0375574398)))

        self.assertFalse(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_2, (-35.1314035932, 162.1343175602, 16.3488238092, -169.0375574398)))
        self.assertFalse(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_2, (-18.5970967976, -33.3344324398, 33.4747130173, 53.5015050602)))
        self.assertFalse(GeoHashWrapper.firstBboxContainsSecondBbox(bbox_2, (-69.9426596955, 63.5210363102, -40.807816162, 150.3569738102)))


    # TODO: Tests for getGeoHash, getGeoHashes, isFirstBboxLargerThanSecondBbox, getBoundingBox, overlap_axis, firstintervalContainsSecondinterval


if __name__ == '__main__':
    unittest.main()
