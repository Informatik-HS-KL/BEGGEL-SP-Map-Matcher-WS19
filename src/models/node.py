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
        :param node_id: id from OSM Overpass API
        :param lat_lon: tuple with the float position values lat and lon
        """
        self.__id = node_id
        self.__latLon = lat_lon
        self.__tags = {}
        self.__links = []
        self.__parent_links = []

    def add_parent_link(self, link):
        """
        Adds Parent Link of this Node
        :param link: Link Object
        :return: None
        """
        self.__parent_links.append(link)

    def get_parent_links(self):
        """
        getter for all parent Links from this Node Object
        :return: list(linkobject, ..)
        """
        return self.__parent_links

    def get_links(self):
        """
        street sections relate to this Node
        :return: list of Links
        """
        return self.__links

    def get_id(self):
        """
        :return: NodeId Object
        """
        return self.__id

    def get_latlon(self):
        """
        :return: tuple (lat, lon)
        """
        return self.__latLon

    def get_lat(self):
        """
        :return: float
        """
        return self.__latLon[0]

    def get_lon(self):
        """
        :return: float
        """
        return self.__latLon[1]

    def set_tags(self, tags: dict):
        """ set Tags to that Point"""
        self.__tags = tags

    def get_tags(self):
        """
        :return: dict of saved Tags to this Node
        """
        return self.__tags

    def add_link(self, link):
        """
        :param link: Link Model related to that Node
        :return: None
        """
        self.__links.append(link)

    def to_geojson(self):
        """
        returns Node as geojson feature
        """

        data = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.get_lat(), self.get_lon()]
            },
            "properties": {
                "osm_node_id": self.get_osm_node_id(),
                "geohash": self.get_geohash(),
                "tags": self.get_tags()
            }
        }
        return data

    def to_wkt(self):
        """:return: Gibt den Knoten im WKT-Format (als String) zurück."""
        lat, lon = self.get_latlon()
        return Point(lon, lat).wkt

    def __repr__(self):
        return "Node: <id: %s> <latLon: %s>" % (self.__id, self.__latLon)

    def get_osm_node_id(self):
        """
        Returns the OSM Id of the Node
        :return:
        """
        return self.get_id().get_osm_node_id()

    def get_geohash(self):
        """
        Returns the Node Geohash
        :return:
        """
        return self.get_id().get_geohash()
