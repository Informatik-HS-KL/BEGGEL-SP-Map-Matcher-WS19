"""
Part of street where there is no intersection and that has a fixed set of properties.
A link might have a non-linear geometry. Geometry of a link is a LINESTRING!
for WKT see:
https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry

"""
from . import Node


class Link:
    _mapService =null

    def __init__(self, start_node: Node, end_node: Node):
        """
        :param startNode: Node Start of this Link
        :param endNode: Node End of this Link
        """
        self.__startNode = start_node
        self.__endNode = end_node
        self.__outs = []

    def get_start_node(self):
        """ :return Node
        """

        #return self.__startNode
        return mapService.loadNode(startNodeRef)

    def get_end_node(self):
        """ :return Node
        """
        return self.__endNode

    def get_links(self):
        return self.__startNode.get_links().extend(self.__endNode.get_links())

    def get_tags(self):
        """
        Attributes of this Link
        :return: dict
        """
        # TODO
        return {}

    def __repr__(self):
        return "<Link Start:%s End:%s>" % (self.__startNode.get_id(), self.__endNode.get_id())

    def to_geojson(self):
        """"""
        data = {"type": "LineString",
                "coordinates": [
                    [self.__startNode.get_lat(), self.__endNode.get_lon()],
                    [self.__endNode.get_lat(), self.__endNode.get_lon()]
                ]
                }
        return data

    def getLinksAsStartNode(self):
        startNode = get_start_node()

        return startNode.getLinks () ## entferne mich selber

