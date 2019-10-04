"""
Part of street where there is no intersection and that has a fixed set of properties.
A link might have a non-linear geometry. Geometry of a link is a LINESTRING!
for WKT see:
https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry

"""
from .node import NodeId


class LinkId:

    def __init__(self, osm_way_id, start_node_id: NodeId):
        self.osm_way_id = osm_way_id
        self.geohash = start_node_id.geohash
        self.start_node_id = start_node_id

    def __eq__(self, other):
        if type(other) is not LinkId:
            return False
        assert (isinstance(other, LinkId))

        return other.osm_way_id == self.osm_way_id and self.start_node_id == other.start_node_id and \
            other.geohash == self.geohash

    def __ne__(self, other):
        return not (self is other)

    def __hash__(self):
        return hash("%s%s" % (self.osm_way_id, self.geohash))


class Link:
    # Links sollen nur noch Referenzen auf die Knoten (also die nodeIds) enthalten.
    # In get_start_node bzw. get_end_node wird dann über mapService der entsprechende Knoten geladen.
    _map_service = None

    def __init__(self, osm_way_id, start_node_id: NodeId, end_node_id: NodeId):
        """
        :param startNode: Node Start of this Link
        :param endNode: Node End of this Link
        """
        self.__start_node_id = start_node_id
        self.__end_node_id = end_node_id
        self.__outs = []
        self.__link_id = LinkId(osm_way_id, start_node_id)

    def get_start_node(self):
        """
        :return Gibt den Startknoten (als Node) zurück.
        """

        # return self.__startNode
        return self._map_service.load_node(self.__start_node_id)

    def get_end_node(self):
        """ :return Gibt den Endknoten (als Node) zurück.
        """
        return self._map_service.load_node(self.__end_node_id)

    # def get_links(self):
    #     return self.__startNode.get_links().extend(self.__endNode.get_links())

    def get_links_at_start_node(self):
        """
        Gibt alle vom Startknoten ausgehende Links zurück (exclusive self).
        :return: Liste von Link-Objekten
        """
        pass

    def get_links_at_end_node(self):
        """
        Gibt alle vom Endknoten ausgehende Links zurück (exclusive self).
        :return: Liste von Link-Objekten
        """
        pass

    def get_tags(self):
        """
        Attributes of this Link
        :return: dict
        """
        # TODO
        return {}

    def get_link_id(self):
        return self.__link_id

    def __repr__(self):
        return "<Link start_node_id:%s end_node_id:%s>" % (self.__start_node_id, self.__end_node_id)

    def to_geojson(self):
        """"""
        data = {"type": "LineString",
                "coordinates": [
                    [self.get_start_node().get_lat(), self.get_start_node().get_lon()],
                    [self.get_end_node().get_lat(), self.get_end_node().get_lon()]
                ]
                }
        return data

    def to_wkt(self):
        pass

    def get_links_at_end_node(self):
        pass

    def get_links_at_start_node(self):
        pass

    def get_length(self):
        pass

    def is_from_start(self):
        pass

    def is_to_start(self):
        pass
