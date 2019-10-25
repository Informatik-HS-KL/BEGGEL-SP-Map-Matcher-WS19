"""
Part of street where there is no intersection and that has a fixed set of properties.
A link might have a non-linear geometry. Geometry of a link is a LINESTRING!
for WKT see:
https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry

"""

from .node import NodeId
from .link_id import LinkId
import src.map_service
from src.geo_utils import great_circle

class Link:
    # Links sollen nur noch Referenzen auf die Knoten (also die nodeIds) enthalten.
    # In get_start_node bzw. get_end_node wird dann über mapService der entsprechende Knoten geladen.

    def __init__(self, link_id, start_node_id: NodeId, end_node_id: NodeId):
        """
        :param startNode: Node Start of this Link
        :param endNode: Node End of this Link
        """
        self.__start_node_id = start_node_id
        self.__end_node_id = end_node_id
        self.__outs = []
        self.__link_id = link_id

        self._map_service = src.map_service.MapService()

    def get_start_node(self):
        """
        :return Gibt den Startknoten (als Node) zurück.
        """

        # return self.__startNode

        return self._map_service.get_node(self.__start_node_id)

    def get_end_node(self):
        """ :return Gibt den Endknoten (als Node) zurück.
        """
        return self._map_service.get_node(self.__end_node_id)

    # def get_links(self):
    #     return self.__startNode.get_links().extend(self.__endNode.get_links())

    def get_links_at_start_node(self):
        """
        Gibt alle vom Startknoten ausgehende Links zurück (exclusive self).
        :return: Liste von Link-Objekten
        """
        nodelinks = self.get_start_node().get_links()
        links = filter(lambda l: l!=self, nodelinks)
        return list(links)

    def get_links_at_end_node(self):
        """
        Gibt alle vom Endknoten ausgehende Links zurück (exclusive self).
        :return: Liste von Link-Objekten
        """

        nodelinks = self.get_end_node().get_links()
        links = filter(lambda l: l != self, nodelinks)
        return list(links)

    def get_tags(self):
        """
        Attributes of this Link
        :return: dict
        """
        # TODO
        return {}

    def get_link_id(self):
        return self.__link_id

    def get_way_osm_id(self):
        return self.__link_id.osm_way_id


    def __repr__(self):
        return "<Link start_node_id:%s end_node_id:%s>" % (self.__start_node_id, self.__end_node_id)

    def to_geojson(self):
        """returns link as geojson feature"""

        data = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [self.get_start_node().get_lat(), self.get_start_node().get_lon()],
                    [self.get_end_node().get_lat(), self.get_end_node().get_lon()]
                ]
            },
            "properties": {
                "osm_way_id": self.get_way_osm_id(),
                "start_node": {
                    "geohash": self.get_link_id().get_start_node_id().geohash,
                    "id": self.get_link_id().get_start_node_id().osm_node_id
                }
            }
        }
        return data

    def to_wkt(self):
        """
        return WKT String from self
        :return:
        """
        return "LINESTRING (%s %s, %s %s)" % (self.get_start_node().get_lat(), self.get_start_node().get_lon(), \
                                                     self.get_end_node().get_lat(), self.get_end_node().get_lon())

    def get_length(self):
        return great_circle(self.get_start_node().get_latlon(), self.get_end_node().get_latlon())

    def is_from_start(self):
        pass

    def is_to_start(self):
        pass

    # beggel-changes
    # def isNavFromStart(self, vehicleType):
    #     """
    #     Kann der Link vom Startknoten zum Endknoten befahren werden.
    #
    #     :param _self:
    #     :return:
    #     """
    #     return 0
    #
    # def isNavToStart(self):
    #     """
    #     Kann der Link vom Endknoten zum StartKnoten befahren werden.
    #
    #     :param _self:
    #     :return:
    #     """
    #     return 0
