from src.map_service import MapService

from src.geohash_wrapper import GeoHashWrapper
from src.rest.app import app


def main():
    """
    This methods runs all tests from the directory tests. If any test fails the corresponding assertion will print an
    error. Otherwise nothing happens.
    :return: None
    """
    from tests.test_map_service import TestMapService
    t = TestMapService()
    t.test_map_service()

    from tests.test_bounding_box import TestBoundingBox
    t = TestBoundingBox()
    t.test_contains_bbox()
    t.test_contains_node()
    t.test_overlap()

    from tests.test_node import TestNode
    t = TestNode()
    t.test_node()

    from tests.test_geo_utils import TestGeoUtils
    t = TestGeoUtils()
    t.test_great_circle()
    t.test_number_is_in_interval()
    t.test_overlap_intervals()

    from tests.test_link_distance import TestLinkDistance
    t = TestLinkDistance()
    t.test_link_distance()


def start_server():

    if __name__ == '__main__':
        print("localhost:5000/api")
        app.run(host="localhost", port=5000)


# main()
start_server()
