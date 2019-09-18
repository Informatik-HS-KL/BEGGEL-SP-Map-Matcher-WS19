"""
Läd daten von der OVerpass schnittstelle in eine Kachel
"""
import  requests
import geohash2 as Geohash
from src.models import Tile
from src.models import Node
from src.models import Link

OVERPASS_URL = "http://overpass-api.de/api/interpreter"

class OverPassWrapper:

    def loadTile (self, geoHash):
        """ Daten von der Overpass api laden
            from geohash to Boundingbox
        """

        bbox = Geohash.decode_exactly(geoHash)
        bboxstr = "(%s,%s,%s,%s)" % (bbox[0] - bbox[2], bbox[1] - bbox[3], bbox[0] + bbox[2], bbox[1] + bbox[3])
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
                nodes[node.getId()] = node

        for element in elements:
            if element["type"] == "way":
                way_nodes = element["nodes"]
                for i in range(0, len(way_nodes)-1):
                    sn = nodes[way_nodes[i]]
                    en = nodes[way_nodes[i + 1]]
                    link = Link(sn, en)
                    sn.addLink(link)
                    en.addLink(link)
                    links.append(link)

        return Tile(geoHash, nodes.values(), links)

tile = OverPassWrapper().loadTile("u0v92u1")

print(tile)
print("NODES:", tile.getNodes())
print("LINKS:", tile.getLinks())

from src.utils import printPretty
printPretty(tile)

