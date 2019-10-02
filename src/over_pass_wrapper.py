"""
Läd daten von der OVerpass schnittstelle in eine Kachel
"""
import requests

from src.models import Tile
from src.models import Node
from src.models import Link
from src.models import BoundingBox


class OverpassWrapper:
    OVERPASS_URL = "http://overpass-api.de/api/interpreter"

    def load_tile(self, geo_hash):
        """ Daten von der Overpass api laden
            from geohash to Boundingbox
        """

        bbox_str = "%s" % BoundingBox.from_geohash(geo_hash)
        q_filter = '(if: ' + self.car_filter() + ')'

        query = '[out:json];way%s%s->.ways;node(w.ways)->.nodes;.nodes out body; .ways out body;' % (bbox_str, q_filter)
        url = "%s?data=%s" % (self.OVERPASS_URL, query)
        print(query)

        resp = requests.get(url)
        elements = resp.json().get("elements")

        nodes = {}  # Initalize
        ways = []  # Initalize
        links = []  # Initalize

        for element in elements:
            if element["type"] == "node":
                node = Node(element["id"], (element["lat"], element["lon"]))
                node.set_tags(element.get("tags", {}))
                nodes[node.get_id()] = node

        for element in elements:
            if element["type"] == "way":
                way_nodes = element["nodes"]
                for i in range(0, len(way_nodes) - 1):
                    sn = nodes[way_nodes[i]]
                    en = nodes[way_nodes[i + 1]]
                    link = Link(sn, en)
                    sn.add_link(link)
                    en.add_link(link)
                    links.append(link)

        return Tile(geo_hash, nodes, links)

    def car_filter(self):
        return ('t["highway"] == "motorway" || t["highway"] == "trunk" '
                '|| t["highway"] == "primary" || t["highway"] == "secondary" '
                '|| t["highway"] == "tertiary" || t["highway"] == "unclassified" '
                '|| t["highway"] == "residential" || t["highway"] == "motorway_link" '
                '|| t["highway"] == "trunk_link" || t["highway"] == "primary_link" '
                '|| t["highway"] == "secondary_link" || t["highway"] == "tertiary_link" '
                '|| t["highway"] == "living_street" '
                '|| t["highway"] == "service"' +  # service ways
                '|| t["highway"] == "road"')  # Unknown street type

    def load_links(self):
        pass

    def load_link(self):
        pass

    def load_node(self):
        pass
