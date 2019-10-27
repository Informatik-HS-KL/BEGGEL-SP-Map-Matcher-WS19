"""
Description: The OverpassWrapper is not only used to obtain OpenStreetMap-Data via the Overpass-API, but also to parse
the obtained data into the convenient model-objects.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

# """
# Läd daten von der OVerpass schnittstelle in eine Kachel
# """
import requests
from .geo_hash_wrapper import GeoHashWrapper

from src.models.tile import Tile
from src.models.node import Node, NodeId
from src.models.link_id import LinkId
from src.models.link import Link
from src.models.bounding_box import BoundingBox

from . import CONFIG


class OverpassWrapper:
    OVERPASS_URL = CONFIG.get("DEFAULT", "overpass_url")
    full_geohash_level = CONFIG.getint("DEFAULT", "full_geohash_level")
    counter = 0

    @staticmethod
    def load_tile(geo_hash):
        """ Daten von der Overpass api laden
            from geohash to Boundingbox
        """
        # ---------------------
        OverpassWrapper.counter += 1
        print(OverpassWrapper.counter, __name__, geo_hash)
        # ---------------------------
        ghw = GeoHashWrapper()

        q_filter = OverpassWrapper._filterQuery(CONFIG)
        url = OverpassWrapper._buildQuery(geo_hash, q_filter)
        print(url)
        resp = requests.get(url)
        elements = resp.json().get("elements")

        nodes = {}  # Initalize
        intersections = set()
        links = {}  # Initalize

        number_of_intersections = int(elements[0]["tags"]["nodes"])
        for k in range(1, number_of_intersections + 1):
            intersections.add(elements[k]["id"])

        for k in range(number_of_intersections + 1, len(elements)):
            element = elements[k]
            if element["type"] == "node":

                node = OverpassWrapper.__create_node(element["id"], (element["lat"], element["lon"]),
                                                     element.get("tags"))
                nodes[node.get_id()] = node

            elif element["type"] == "way":
                way_nodes_ids = element["nodes"]
                way_nodes_positions = element["geometry"]

                link_geometry = []
                link_node_ids = []

                for i in range(0, len(way_nodes_ids) - 1):  # Building the links that put together the way.

                    if (way_nodes_ids[i] in intersections and i != 0) or i == len(way_nodes_ids) - 1:  # reached end of link

                        end_node_pos = (way_nodes_positions[i]["lat"], way_nodes_positions[i]["lon"])
                        end_node_id = NodeId(way_nodes_ids[i], ghw.get_geohash(end_node_pos,
                                                                               level=OverpassWrapper.full_geohash_level))

                        link_geometry.append(end_node_pos)
                        link_node_ids.append(end_node_id)
                        link_id = LinkId(element["id"], link_node_ids[0])
                        link = Link(link_id, link_geometry, link_node_ids)
                        links.update({link_id: link})

                        #  Re-Initialization for the next link
                        link_geometry = [end_node_pos]
                        link_node_ids = [end_node_id]

                    else:
                        node_pos = (way_nodes_positions[i]["lat"], way_nodes_positions[i]["lon"])
                        node_id = NodeId(way_nodes_ids[i], ghw.get_geohash(node_pos,
                                                                           level=OverpassWrapper.full_geohash_level))
                        link_geometry.append(node_pos)
                        link_node_ids.append(node_id)

        return Tile(geo_hash, nodes, links)

    @staticmethod
    def _buildQuery(geohash, q_filter: str):
        """Return Url to Download Tile"""

        bbox_str = "%s" % BoundingBox.from_geohash(geohash)
        query = '[out:json];way%s%s->.ways;node(w.ways)->.nodes;relation.nodes->.intersections;foreach.ways->.w((' \
                '.ways; - .w;)->.otherWays;node(w.w)->.currentWayNodes;node(' \
                'w.otherWays)->.otherWayNodes;node.currentWayNodes.otherWayNodes->.currentIntersections;(' \
                '.intersections; .currentIntersections;)->.intersections;);.intersections out count;.intersections ' \
                'out ids;.nodes out body; .ways out geom;' % (bbox_str, q_filter)
        url = "%s?data=%s" % (OverpassWrapper.OVERPASS_URL, query)
        return url

    @staticmethod
    def _filterQuery(config, conf_section="HIGHWAY_CARS"):
        """Erstellt Query aus gegebenen Highways aus der Config
           conf_section: Section in der config.ini die zur Erstellung der Query herangezogen werden soll
        """

        query = "(if: "
        options = config.options(conf_section, no_defaults=True)
        for option in options:
            if config.getboolean(conf_section, option):
                query += 't["highway"] == "%s" ||' % option

        return query[:-2] + ")"

    @staticmethod
    def __create_node(osm_id, pos: tuple, tags=None):
        node_id = NodeId(osm_id, GeoHashWrapper().get_geohash(pos, level=OverpassWrapper.full_geohash_level))
        node = Node(node_id, pos)
        node.set_tags(tags)
        return node

    # KP 20.10.2019: Ersetzt durch buildQuery
    # @staticmethod
    # def car_filter():
    #     return ('   t["highway"] == "motorway" || t["highway"] == "trunk" '
    #             '|| t["highway"] == "primary" || t["highway"] == "secondary" '
    #             '|| t["highway"] == "tertiary" || t["highway"] == "unclassified" '
    #             '|| t["highway"] == "residential" || t["highway"] == "motorway_link" '
    #             '|| t["highway"] == "trunk_link" || t["highway"] == "primary_link" '
    #             '|| t["highway"] == "secondary_link" || t["highway"] == "tertiary_link" '
    #             '|| t["highway"] == "living_street" '
    #             '|| t["highway"] == "service"'  # service ways
    #             '|| t["highway"] == "road"')  # Unknown street type
