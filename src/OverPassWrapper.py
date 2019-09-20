"""
Läd daten von der OVerpass schnittstelle in eine Kachel
"""
import  requests
import geohash2 as Geohash
from src.models import Tile
from src.models import Node
from src.models import Link
from src.utils import decode2Box

OVERPASS_URL = "http://overpass-api.de/api/interpreter"

class OverPassWrapper:

    def loadTile (self, geoHash):
        """ Daten von der Overpass api laden
            from geohash to Boundingbox
        """

        bboxstr = "(%s,%s,%s,%s)" % decode2Box(geoHash)
        query = '[out:json];way[highway]%s->.ways;node(w.ways)->.nodes;.nodes out body; .ways out body;' % bboxstr
        url = "%s?data=%s" % (OVERPASS_URL, query)
        print(query)

        resp = requests.get(url)
        elements = resp.json().get("elements")
        nodes = {}
        ways = []
        links = []

        for element in elements:
            if element["type"] == "node":
                node = Node(element["id"], (element["lat"], element["lon"]))
                nodes[node.get_id()] = node

        for element in elements:
            if element["type"] == "way":
                way_nodes = element["nodes"]
                for i in range(0, len(way_nodes)-1):
                    sn = nodes[way_nodes[i]]
                    en = nodes[way_nodes[i + 1]]
                    link = Link(sn, en)
                    sn.add_link(link)
                    en.add_link(link)
                    links.append(link)

        return Tile(geoHash, nodes, links)
