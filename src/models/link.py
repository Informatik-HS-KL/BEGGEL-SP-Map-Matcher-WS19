"""
Description: A Link is a part of a street which if at all has only intersections at the beginning and/or the end. A Link might
have a non-linear geometry. The geometry of a link is a LINESTRING.
For WKT see: (https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz

# Part of street where there is no intersection and that has a fixed set of properties.
# A link might have a non-linear geometry. Geometry of a link is a LINESTRING!
# for WKT see:
# https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
#
"""

import src.map_service

from shapely.geometry import LineString

from .bounding_box import BoundingBox
from .link_user import LinkUser
from src.geo_utils import great_circle


class Link:

    def __init__(self, link_id, geometry: list, node_ids: list):
        """
        :param link_id: LinkId-Object
        :param geometry: list(tuple)
        :param node_ids: list(NodeId-Objects)
        """
        self._start_node_id = node_ids[0]
        self._end_node_id = node_ids[len(node_ids) - 1]
        self._link_id = link_id
        self._geometry = geometry  # contains the (lat, lon)-tupel of all nodes of the link
        self._node_ids = node_ids
        self._tags = {}
        self._length = None

        self._map_service = src.map_service.MapService()

    def get_bbox(self):
        """
        bounding box of link resulted from geometry
        :return: BoundingBox-Object
        """
        s, w, n, e = LineString(self.get_geometry()).bounds

        return BoundingBox(s, w, n, e)

    def get_start_node(self):
        """
        :return Gibt den Startknoten (als Node) zurück.
        """

        return self._map_service.get_node(self._start_node_id)

    def get_end_node(self):
        """ :return Gibt den Endknoten (als Node) zurück.
        """
        return self._map_service.get_node(self._end_node_id)

    # def get_links(self):
    #     return self.__startNode.get_links().extend(self.__endNode.get_links())

    def get_links_at_start_node(self, link_user: LinkUser = None):
        """
        Gibt alle vom Startknoten ausgehende Links zurück (exclusive self).
        :param link_user: LinkUser-Object
        :return: Liste von Link-Objects

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
        :param link_user: LinkUser-Object
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
        return self._tags

    def set_tags(self, tags: dict):
        """
        :param tags: dict
        :return: None
        """
        if tags is None:
            self._tags = {}
        else:
            self._tags = tags

    def get_id(self):
        """
        :return: LinkId-Object
        """
        return self._link_id

    def get_way_osm_id(self):
        """
        :return: Osm Way id of self
        """
        return self.get_id().get_osm_way_id()

    def __repr__(self):
        return "Link: <link_id: %s> <geometry: %s> <node_ids: %s>" % (self._link_id, self._geometry, self._node_ids)

    def __str__(self):
        return "Link: <start_node_id: %s> <end_node_id: %s>" % (self._start_node_id, self._end_node_id)

    def to_geojson(self):
        """
        returns link as geojson feature
        """

        line_string_coordinates = []
        for p in self._geometry:
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
                    "geohash": self.get_id().get_start_node_id().get_geohash(),
                    "id": self.get_id().get_start_node_id().get_osm_id()
                },
                "tags": self.get_tags()
            }
        }

        return data

    def to_wkt(self):
        """
        return WKT String from self
        :return: WKT-String
        """
        return LineString(self.get_geometry()).wkt

    def get_length(self):
        """
        Returns the length of the link.
        The calculation of the length is done on demand and then saved in the corresponding attribute.
        :return: int length in meter
        """
        if self._length is None:
            self._length = 0
            for i in range(len(self._geometry) - 1):
                self._length += great_circle(self._geometry[i], self._geometry[i + 1])

        return self._length

    def is_navigatable_from_start(self, link_user: LinkUser) -> bool:
        """
        Indicates, whether the specified user is permitted to use the link from the start-node to the end-node.
        :param link_user: LinkUser-Object
        :return: bool
        """
        return link_user.can_navigate_from_start(self)

    def is_navigatable_to_start(self, link_user: LinkUser) -> bool:
        """
        Indicates, whether the specified user is permitted to use the link from the end-node to the start-node.
        :param link_user: LinkUser-Object
        :return: bool
        """
        return link_user.can_navigate_to_start(self)

    def get_link_segments(self) -> list:
        """
        Splits a link into segments, each consisting of two positions/coordinates.
        :return: list, containing the segments
        """
        segments = list()

        for i in range(len(self._geometry) - 1):
            segment = (self._geometry[i], self._geometry[i + 1])
            segments.append(segment)

        return segments

    def get_geometry(self):
        """
        :return: list(tuple)
        """
        return self._geometry

    def get_node_ids(self):
        """
        :return: list(NodeIds)
        """
        return self._node_ids

    def get_geohash(self):
        """
        :return: str
        """
        return self.get_id().get_geohash()
