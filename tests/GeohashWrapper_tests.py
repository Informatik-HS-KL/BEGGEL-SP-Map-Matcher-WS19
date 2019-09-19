# from src.GeoHashWrapper import GeoHashWrapper
#
# bbox_1 = (31.27, -110.19, 37.64, -102.1)
#
# # Test 1
# if not GeoHashWrapper.overlapse(bbox_1, (30.85, -106.76, 33.31, -103.77)):
#     print("Test 1: ", end="")
#     print(False)
#
# # Test 2
# if not GeoHashWrapper.overlapse(bbox_1, (33.46, -110.45, 35.84, -107.46)):
#     print("Test 2: ", end="")
#     print(False)
#
# # Test 3
# if not GeoHashWrapper.overlapse(bbox_1, (33.49, -107.11, 34.37, -105.88)):
#     print("Test 3: ", end="")
#     print(False)
#
# # Test 4
# if not GeoHashWrapper.overlapse(bbox_1, (36.16, -106.06, 37.01, -104.83)):
#     print("Test 3: ", end="")
#     print(False)
#
# # Test 5
# if GeoHashWrapper.overlapse(bbox_1, (41.76, -105.18, 45.7, -90.59)):
#     print("Test 5: ", end="")
#     print(False)
#
# # Test 6
# if GeoHashWrapper.overlapse(bbox_1, (-5.8, 46.3, 6.3, 60.9)):
#     print("Test 6: ", end="")
#     print(False)


import unittest
from src.GeoHashWrapper import GeoHashWrapper


class TestGeohashWrapper(unittest.TestCase):

    def test_overlaps(self):
        self.assertEqual(GeoHashWrapper.overlap((31.27, -110.19, 37.64, -102.1), (30.85, -106.76, 33.31, -103.77)), True)
        self.assertEqual(GeoHashWrapper.overlap((31.27, -110.19, 37.64, -102.1), (33.46, -110.45, 35.84, -107.46)),
                         True)
        self.assertEqual(GeoHashWrapper.overlap((31.27, -110.19, 37.64, -102.1), (33.49, -107.11, 34.37, -105.88)),
                         True)
        self.assertEqual(GeoHashWrapper.overlap((31.27, -110.19, 37.64, -102.1), (36.16, -106.06, 37.01, -104.83)),
                         True)
        self.assertEqual(GeoHashWrapper.overlap((31.27, -110.19, 37.64, -102.1), (41.76, -105.18, 45.7, -90.59)),
                         False)
        self.assertEqual(GeoHashWrapper.overlap((31.27, -110.19, 37.64, -102.1), (-5.8, 46.3, 6.3, 60.9)),
                         False)


if __name__ == '__main__':
    unittest.main()
