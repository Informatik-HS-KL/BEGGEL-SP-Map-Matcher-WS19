"""
Part of street where there is no intersection and that has a fixed set of properties.
A link might have a non-linear geometry. Geometry of a link is a LINESTRING!
for WKT see:
https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry

"""
from . import Node


class Link_id:

    def __init__(self, way_id, geohash, start_node):
        self.way_id = way_id
        self.geohash = geohash
        self.start_node = start_node

class Link:

    # Links sollen nur noch Referenzen auf die Knoten (also die nodeIds) enthalten.
    # In get_start_node bzw. get_end_node wird dann über mapService der entsprechende Knoten geladen.
    _map_service = None

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
        return _map_service.loadNode(startNodeId)

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

    def to_wkt(self):
        pass

    def get_links_at_endnode(self):
        pass

    def get_links_at_startnode(self):
        pass

    def get_length(self):
        pass

    def is_from_start(self):
        pass

    def is_to_start(self):
        pass