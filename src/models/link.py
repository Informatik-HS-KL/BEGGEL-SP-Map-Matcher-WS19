"""
Description: A Link is a part of a street which if at all has only intersections at the beginning and/or the end. A Link might
have a non-linear geometry. The geometry of a link is a LINESTRING.
For WKT see: (https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

# """
# Part of street where there is no intersection and that has a fixed set of properties.
# A link might have a non-linear geometry. Geometry of a link is a LINESTRING!
# for WKT see:
# https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
#
# """

from .node import NodeId
from .link_id import LinkId
import src.map_service
from src.geo_utils import great_circle
import src.models.bounding_box
from shapely.geometry import LineString
from src.models.link_user import LinkUser


class Link:
    # Links sollen nur noch Referenzen auf die Knoten (also die nodeIds) enthalten.
    # In get_start_node bzw. get_end_node wird dann über mapService der entsprechende Knoten geladen.

    def __init__(self, link_id, geometry: list, node_ids: list):
        """
        :param startNode: Node Start of this Link
        :param endNode: Node End of this Link
        """
        self.__start_node_id = node_ids[0]
        self.__end_node_id = node_ids[len(node_ids) - 1]
        self.__outs = []
        self.__link_id = link_id
        self.__geometry = geometry  # contains the (lat, lon)-tupel of all nodes of the link
        self.__node_ids = node_ids
        self.__tags = None

        self._map_service = src.map_service.MapService()

    def get_bbox(self):
        """
        bounding box of link resulted from geometry
        :return: BoundingBox Object
        """
        s, w, n, e = LineString(self.get_geometry()).bounds

        return src.models.bounding_box.BoundingBox(s, w, n, e)

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

    def get_links_at_start_node(self, link_user: LinkUser = None):
        """
        Gibt alle vom Startknoten ausgehende Links zurück (exclusive self).
        :return: Liste von Link-Objekten

        """

        node_links = self.get_start_node().get_links()
        links = list(filter(lambda i: i != self, node_links))

        if link_user is None:
            return links
        else:
            for link in links:
                if self.get_start_node() == link.get_start_node():
                    if not link.is_navigatable_from_start(link_user):
                        links.remove(link)
                elif self.get_start_node() == link.get_end_node():
                    if not link.is_navigatable_to_start(link_user):
                        links.remove(link)
            return links

    def get_links_at_end_node(self, link_user: LinkUser = None):
        """
        Gibt alle vom Endknoten ausgehende Links zurück (exclusive self).
        :return: Liste von Link-Objekten
        """

        nodelinks = self.get_end_node().get_links()
        links = list(filter(lambda l: l != self, nodelinks))

        if link_user is None:
            return links
        else:
            for link in links:
                if self.get_end_node() == link.get_start_node():
                    if not link.is_navigatable_from_start(link_user):
                        links.remove(link)
                elif self.get_end_node() == link.get_end_node():
                    if not link.is_navigatable_to_start(link_user):
                        links.remove(link)
            return links

    def get_tags(self):
        """
        Attributes of this Link
        :return: dict
        """
        # TODO
        return self.__tags

    def set_tags(self, tags: dict):
        self.__tags = tags

    def get_link_id(self):
        """
        :return: LinKId Object
        """
        return self.__link_id

    def get_way_osm_id(self):
        """
        :return: Osm Way id of self
        """
        return self.__link_id.osm_way_id

    def __repr__(self):
        return "Link: <link_id: %s> <geometry: %s> <node_ids: %s>" % (self.__link_id, self.__geometry, self.__node_ids)

    def __str__(self):
        return "Link: <start_node_id: %s> <end_node_id: %s>" % (self.__start_node_id, self.__end_node_id)

    def to_geojson(self):
        """
        Todo: Wenn wir shapely verwenden, dann geht das hier komfortabler!!!
        returns link as geojson feature
        """

        line_string_coordinates = []
        for p in self.__geometry:
            line_string_coordinates.append([p[0], p[1]])

        data = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": line_string_coordinates
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
        Todo: An neue Linkstruktur anpassen (verwenden wir hier shapely oder nicht?)!!!
        return WKT String from self
        :return:
        """
        return "LINESTRING (%s %s, %s %s)" % (self.get_start_node().get_lat(), self.get_start_node().get_lon(), \
                                              self.get_end_node().get_lat(), self.get_end_node().get_lon())

    def get_length(self):
        """
        Todo: An neue Linkstruktur anpassen (verwenden wir hier shapely oder nicht?)!!!
        """
        return great_circle(self.get_start_node().get_latlon(), self.get_end_node().get_latlon())

    def is_navigatable_from_start(self, link_user: LinkUser) -> bool:
        """
        Indicates, whether the specified user is permitted to use the link from the start-node to the end-node.
        :param link_user:
        :return: bool
        """
        return link_user.can_navigate_from_start(self)

    def is_navigatable_to_start(self, link_user: LinkUser) -> bool:
        """
        Indicates, whether the specified user is permitted to use the link from the end-node to the start-node.
        :param link_user:
        :return: bool
        """
        return link_user.can_navigate_to_start(self)

    def get_link_segments(self) -> list:
        """
        Splits a link into segments, each consisting of two positions/coordinates.

        :return: list, containing the segments
        """
        segments = list()

        for i in range(len(self.__geometry) - 1):
            segment = (self.__geometry[i], self.__geometry[i + 1])
            segments.append(segment)

        return segments

    def get_geometry(self):
        return self.__geometry

    def get_node_ids(self):
        return self.__node_ids
