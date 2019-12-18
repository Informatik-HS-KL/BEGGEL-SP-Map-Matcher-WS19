"""
Description:  A Node is basically representing an osm-node. But the class Node also contains useful observer functions,
for example to convert the geometry of a Node-Object into several geo-formats, and mutator functions.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""
from .node_id import NodeId
from shapely.geometry import Point


class Node:

    def __init__(self, node_id: NodeId, lat_lon: tuple):
        """
        :param node_id: NodeId-Object
        :param lat_lon: tuple(lat, lon)
        """
        self._id = node_id
        self._latLon = lat_lon
        self._tags = {}
        self._links = []
        self._parent_links = []

    def add_parent_link(self, link):
        """
        :param link: Link Object
        :return: None
        """
        self._parent_links.append(link)

    def get_parent_links(self):
        """
        :return: list(Link-Object)
        """
        return self._parent_links

    def get_links(self):
        """
        :return: list(link)
        """
        return self._links

    def get_id(self):
        """
        :return: NodeId Object
        """
        return self._id

    def get_latlon(self):
        """
        :return: tuple (lat, lon)
        """
        return self._latLon

    def get_lat(self):
        """
        :return: float
        """
        return self._latLon[0]

    def get_lon(self):
        """
        :return: float
        """
        return self._latLon[1]

    def set_tags(self, tags: dict):
        """
        :param tags: dict
        :return: None
        """
        if tags is None:
            self._tags = {}
        else:
            self._tags = tags

    def get_tags(self):
        """
        :return: dict
        """
        return self._tags

    def add_link(self, link):
        """
        :param link: Link Model related to that Node
        :return: None
        """
        self._links.append(link)

    def to_geojson(self):
        """
        :return: dict
        """

        data = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.get_lat(), self.get_lon()]
            },
            "properties": {
                "osm_node_id": self.get_osm_id(),
                "geohash": self.get_geohash(),
                "tags": self.get_tags()
            }
        }
        return data

    def to_wkt(self):
        """
        :return: str
        """
        lat, lon = self.get_latlon()
        return Point(lon, lat).wkt

    def __repr__(self):
        return "Node: <id: %s> <latLon: %s>" % (self._id, self._latLon)

    def get_osm_id(self):
        """
        :return: int
        """
        return self.get_id().get_osm_id()

    def get_geohash(self):
        """
        :return: str
        """
        return self.get_id().get_geohash()
