from src.map_service import MapService
import argparse
import pandas as pd
# from src.map_service import MapService

from src.geohash_wrapper import GeoHashWrapper
from src.models import BoundingBox, Car
from src.models import Link
from src.models import Node
from src.rest.app import app


def sanitize(string):
    return string.replace(";", ",")


def main():
    """
    This methods runs all tests from the directory tests. If any test fails the corresponding assertion will print an
    error. Otherwise nothing happens.
    :return: None
    """

    parser = argparse.ArgumentParser(description='Export Map Data to CSV')
    parser.add_argument('lat', type=float, help='center of search area as latitude')
    parser.add_argument('lng', type=float, help='center of search area as longitude')
    parser.add_argument('width', type=float, help='width of the search area', default=0.2)
    parser.add_argument('height', type=float, help='height of the search area', default=0.2)
    args = parser.parse_args()

    map_service = MapService()

    pos = (args.lat, args.lng)
    dim = (args.width, args.height)

    nodes = map_service.get_nodes_in_bounding_box(
        BoundingBox(pos[0] - dim[0] / 2, pos[1] - dim[1] / 2, pos[0] + dim[0] / 2, pos[1] + dim[1] / 2))

    counter = 0
    poi_arr = []
    poi_tags = []
    for node in nodes:
        if "amenity" in node.get_tags():
            print("{:-^50}".format(node.to_wkt()))
            counter += 1
            tmp_obj = {"id": counter,
                       "lat": node.get_lat(),
                       "lng": node.get_lon(),
                       "type": sanitize(node.get_tags()["amenity"])}
            for k, v in node.get_tags().items():
                print("  " + k + " --> " + v)
                if k != "amenity":
                    poi_tags.append({"poi_id": counter, "name": sanitize(k), "value": sanitize(v)})
            poi_arr.append(tmp_obj)

    pd.DataFrame(poi_arr).to_csv("out/exported_poi.csv", sep=";", index=False)
    pd.DataFrame(poi_tags).to_csv("out/exported_poi_tags.csv", sep=";", index_label="id")

    # parse links
    links = map_service.get_links_in_bounding_box(
        BoundingBox(pos[0] - dim[0] / 2, pos[1] - dim[1] / 2, pos[0] + dim[0] / 2, pos[1] + dim[1] / 2))

    for link in links[:1]:
        print(link.to_wkt())
        print(link.to_geojson())
        print(link.get_geometry())
        for k, v in link.get_tags().items():
            print(k + " --> " + v)
        print("Car from Start: ", link.is_navigatable_from_start(Car()))
        print("Car to Start: ", link.is_navigatable_to_start(Car()))
        print("Start Note: ", link.get_start_node().get_id())
        print("End Note: ", link.get_end_node().get_id().get_osm_id())
        print("Length Meter:", link.get_length())


main()
