from src.map_service import MapService
import argparse
import pandas as pd
# from src.map_service import MapService

from src.geohash_wrapper import GeoHashWrapper
from src.models import BoundingBox, Car
from src.models import Link
from src.models import Node
from src.rest.app import app

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
    parser.add_argument('elements', type=int, help='height of the search area', default=100)
    args = parser.parse_args()

    pos = (args.lat, args.lng)
    dim = (args.width, args.height)
    nodes, links = get_bbox(pos, dim)
    type_lut = generate_types(links, nodes)
    generate_poi(nodes, type_lut)
    generate_link(links, type_lut)


def get_bbox(pos, dim):
    map_service = MapService()
    nodes = map_service.get_nodes_in_bounding_box(
        BoundingBox(pos[0] - dim[0] / 2, pos[1] - dim[1] / 2, pos[0] + dim[0] / 2, pos[1] + dim[1] / 2))
    links = map_service.get_links_in_bounding_box(
        BoundingBox(pos[0] - dim[0] / 2, pos[1] - dim[1] / 2, pos[0] + dim[0] / 2, pos[1] + dim[1] / 2))

    return nodes, links


def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))


def generate_types(links, nodes):
    osm_poi_set = set()
    for node in nodes:
        if "amenity" in node.get_tags():
            osm_poi_set.add(node.get_tags()["amenity"])

    osm_link_set = set()
    for link in links:
        if "highway" in link.get_tags():
            osm_link_set.add(link.get_tags()["highway"])

    osm_type_arr = []
    for i, poi in enumerate(osm_poi_set):
        osm_type_arr.append({"osm_type_name": poi, "source": "POI"})
    for i, link in enumerate(osm_link_set):
        osm_type_arr.append({"osm_type_name": link, "source": "LINK"})

    pd.DataFrame(osm_type_arr).to_csv("out/osm_types.csv", sep=",", index_label="osm_type_id")
    type_lut = build_dict(osm_type_arr, key="osm_type_name")
    return type_lut


def generate_poi(nodes, type_lut):
    poi_arr = []
    for node in nodes:
        if "amenity" in node.get_tags():
            poi_arr.append({"osm_id": node.get_osm_id(), "geom": node.to_wkt(), "osm_type": type_lut.get(node.get_tags()["amenity"])["index"]})
    pd.DataFrame(poi_arr).to_csv("out/poi.csv", sep=",", index=False)


def generate_link(links, type_lut):
    link_arr = []
    for link in links:
        if "highway" in link.get_tags():
            link_arr.append({"osm_id": link.get_way_osm_id(),
                             "geom": link.to_wkt(),
                             "osm_type": type_lut.get(link.get_tags()["highway"])["index"]})
    pd.DataFrame(link_arr).to_csv("out/link.csv", sep=",", index=False)

main()
