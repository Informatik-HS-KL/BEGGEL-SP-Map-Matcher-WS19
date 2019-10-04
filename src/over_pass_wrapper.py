"""
Läd daten von der OVerpass schnittstelle in eine Kachel
"""
import requests
from .geo_hash_wrapper import GeoHashWrapper

from src.models import Tile
from src.models import Node, NodeId
from src.models import Link, LinkId
from src.models import BoundingBox


class OverpassWrapper:
    OVERPASS_URL = "http://lz4.overpass-api.de/api/interpreter"
    full_geohash_level = 12
    counter = 0

    def load_tile(self, geo_hash):
        """ Daten von der Overpass api laden
            from geohash to Boundingbox
        """
        # ---------------------
        OverpassWrapper.counter += 1
        print(OverpassWrapper.counter)
        # ---------------------------

        bbox_str = "%s" % BoundingBox.from_geohash(geo_hash)
        q_filter = '(if: ' + self.car_filter() + ')'

        query = '[out:json];way%s%s->.ways;node(w.ways)->.nodes;.nodes out body; .ways out geom;' % (bbox_str, q_filter)
        url = "%s?data=%s" % (self.OVERPASS_URL, query)
        print(query)

        resp = requests.get(url)
        print(resp.content)
        elements = resp.json().get("elements")

        nodes = {}  # Initalize
        ways = []  # Initalize
        links = {}  # Initalize

        for element in elements:
            if element["type"] == "node":
                # kapl: TODO: wir müssen über die erstellung von NodeId reden
                # NodeId direkt über Node Klasse erstellen?
                node = self.__create_node(element["id"], (element["lat"], element["lon"]), element.get("tags"))
                nodes[node.get_id()] = node

            elif element["type"] == "way":
                way_nodes_ids = element["nodes"]
                way_nodes_positions = element["geometry"]
                for i in range(0, len(way_nodes_ids) - 1):

                    # kapl TODO: Schaut ich die folgende recherche in unserem Dictonary nodes an:
                    # Wir müssen bevor wir in einem nodes oder link dict recherieren erst mal die geohashes des Nodes
                    # rausfinden.
                    # Dann ein Objekt NodeId erstellen und mit diesem als Key suchen
                    # Vielleicht in NodeId eine Funktion get_node_id schreiben, die zu einer osm_node_id die NodeId
                    # liefert.
                    ghw = GeoHashWrapper()
                    start_node_pos = (way_nodes_positions[i]["lat"], way_nodes_positions[i]["lon"])
                    end_node_pos = (way_nodes_positions[i+1]["lat"], way_nodes_positions[i+1]["lon"])

                    start_node_id = NodeId(way_nodes_ids[i], ghw.get_geohash(start_node_pos,
                                                                             level=self.full_geohash_level))
                    end_node_id = NodeId(way_nodes_ids[i+1], ghw.get_geohash(end_node_pos,
                                                                             level=self.full_geohash_level))

                    link_id = LinkId(element["id"], start_node_id)
                    link = Link(link_id, start_node_id, end_node_id)
                    nodes[start_node_id].add_link(link)
                    nodes[end_node_id].add_link(link)

                    links.update({link_id:link})

        return Tile(geo_hash, nodes, links)

    def car_filter(self):
        return ('   t["highway"] == "motorway" || t["highway"] == "trunk" '
                '|| t["highway"] == "primary" || t["highway"] == "secondary" '
                '|| t["highway"] == "tertiary" || t["highway"] == "unclassified" '
                '|| t["highway"] == "residential" || t["highway"] == "motorway_link" '
                '|| t["highway"] == "trunk_link" || t["highway"] == "primary_link" '
                '|| t["highway"] == "secondary_link" || t["highway"] == "tertiary_link" '
                '|| t["highway"] == "living_street" '
                '|| t["highway"] == "service"'  # service ways
                '|| t["highway"] == "road"')  # Unknown street type

    def footway_filter(self):
        return ('t["highway"] == "footway" || t["highway"] == "steps"'
                '|| t["highway"] == "path" || t["sidewalk"]')

    def load_links(self):
        pass

    def load_link(self):
        pass

    def load_node(self):
        pass

    def __create_node(self, osm_id, pos: tuple, tags=None):
        node_id = NodeId(osm_id, GeoHashWrapper().get_geohash(pos, level=self.full_geohash_level))
        node = Node(node_id, pos)
        node.set_tags(tags)
        return node
