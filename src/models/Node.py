"""
Node is a Point on the Map with a geo Position lat/lon
"""


class Node:

    def __init__(self, osmid: int, latlon: tuple):
        """
        :param id: id from OSM Overpass API
        :param latlon: tuple with the float position values lat and lon
        """

        self.__id = osmid
        self.__latLon = latlon
        self.__tags = {}
        self.__links = []

    def get_links(self):
        """
        street sections relate to this Node
        :return: list of Links
        """
        return self.__links

    def get_id(self):
        """
        :return: int of OSM Node ID
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

    def get_distance(self, other):
        """

        :param other: Node
        :return:
        """

        # TODO Berechne Distanz zu anderem Knoten


    def to_geo_json(self):
        """
        :return:
        """
        # TODO KP: MAcht das Sinn hier sowas zu erstellen oder lieber an einer anderen Stelle?

    def __repr__(self):
        return "<Node: %s>" % self.__id