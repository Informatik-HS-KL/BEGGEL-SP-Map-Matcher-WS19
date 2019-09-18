"""
Läd daten von der OVerpass schnittstelle in eine Kachel
"""
import  requests
import geohash2 as Geohash
from Tile import Tile

OVERPASS_URL = "http://overpass-api.de/api/interpreter"

class OverPassWrapper:

    def loadTile (self, geoHash):
        """ Daten von der Overpass api laden
            from geohash to Boundingbox
        """

        bbox = Geohash.decode_exactly(geoHash)
        bboxstr = "(%s,%s,%s,%s)" % (bbox[0] - bbox[2], bbox[1] - bbox[3], bbox[0] + bbox[2], bbox[1] + bbox[3])
        query = '[out:json];way%s;out;' % bboxstr
        url = "%s?data=%s" % (OVERPASS_URL, query)
        print(query)

        resp = requests.get(url)
        json_ways = resp.json().get("elements")

        tile = Tile(geoHash)

        for way in json_ways:
            for node in way["nodes"]:

                tile.addNode(node)
                print(node)
        return None


OverPassWrapper().loadTile("u0v921")