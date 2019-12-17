from src.map_service import MapService

from src.geohash_wrapper import GeoHashWrapper
from src.rest.app import app


def main():
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


def main2():
    ms = MapService()
    ms.get_tile("u0v92")
    links = ms.get_links(236069595)
    for link in links:
        print(link)

def start_server():

    if __name__ == '__main__':
        print("localhost:5000/api")
        app.run(host="localhost", port=5000)


# main()
# start_server()
main2()