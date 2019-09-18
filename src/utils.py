from .models import Tile




def printPretty(tile : Tile):
    """"""

    for n in tile.getNodes():
        print("-"*20)
        print("Node:", n.getId())
        print("Links", [(l.getNodeAtStart(), l.getNodeAtEnd()) for l in n.getLinks()])

