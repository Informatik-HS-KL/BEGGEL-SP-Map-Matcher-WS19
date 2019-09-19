from .models import Tile
import geohash2 as Geohash

def decode2Box(geohash):
    bbox = Geohash.decode_exactly(geohash)
    return (bbox[0] - bbox[2], bbox[1] - bbox[3], bbox[0] + bbox[2], bbox[1] + bbox[3])

def printPretty(tile : Tile):
    """"""

    for n in tile.getNodes():
        print("-"*20)
        print("Node:", n.getId())
        print("Links", [(l.getNodeAtStart(), l.getNodeAtEnd()) for l in n.getLinks()])

