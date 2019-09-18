"""
Part of street where there is no intersection and that has a fixed set of properties.
A link might have a non-linear geometry. Geometry of a link is a LINESTRING!
for WKT see:
https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry

"""

class Link:
    """
    """

    def __init__(self, startNode, endNode):
        """
        """
        self.startNode = startNode
        self.endNode = endNode
        self.__outs = []

    def getNodeAtStart (self):
        """
        """
        return self.startNode

    def getNodeAtEnd(self):
        """
        """
        return self.endNode

    def getOutgoingLinks(self):
        return self.__outs
