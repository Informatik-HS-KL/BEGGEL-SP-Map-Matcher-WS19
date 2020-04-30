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

    nodes = filter(lambda el: "amenity" in el.get_tags(), nodes)
    links = filter(lambda el: "highway" in el.get_tags(), links)

    poi_elements, poi_tags = generate_elements(nodes, type_lut, master_tag="amenity", element_name="POI")
    link_elements, link_tags = generate_elements(links, type_lut, master_tag="highway", add_unique_counter=True, element_name="LINK")
    pd.DataFrame(poi_tags + link_tags).to_csv("out/tags.csv", sep=",", index=False)
    pd.DataFrame(poi_elements + link_elements).to_csv("out/osm_elements.csv", sep=",", index=False)


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


def generate_elements(elements, type_lut, master_tag, element_name, add_unique_counter=False):
    link_arr = []
    tag_arr = []
    for i, element in enumerate(elements):
        if master_tag in element.get_tags():
            osm_id = find_id_method(element)
            if add_unique_counter:
                osm_id = str(osm_id) + ":" + str(i)
            link_arr.append({"osm_id": osm_id,
                             "geom": element.to_wkt(),
                             "osm_type_id": type_lut.get(element.get_tags()[master_tag])["index"],
                             "type": element_name})
            tag_arr += generate_tags(osm_id, element.get_tags().items())
    return link_arr, tag_arr


def find_id_method(element):
    if "get_way_osm_id" in dir(element):
        osm_id = getattr(element, 'get_way_osm_id')()
    else:
        osm_id = getattr(element, 'get_osm_id')()
    return osm_id


def generate_tags(node_id, tag_list):
    tag_arr = []
    for k, v in tag_list:
        tag_arr.append({"osm_id": node_id, "tag_name": k, "tag_value": v})
    return tag_arr


main()
