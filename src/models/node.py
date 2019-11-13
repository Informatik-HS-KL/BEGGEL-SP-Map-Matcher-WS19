"""
Description:  A Node is basically representing an osm-node. But the class Node also contains useful observer functions,
for example to convert the geometry of a Node-Object into several geo-formats, and mutator functions.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""


class NodeId:
    def __init__(self, osm_node_id, geohash):
        """:param geohash: geohash wird in voller Länge (als String) angegeben."""
        self.osm_node_id = osm_node_id
        self.geohash = geohash

    def __eq__(self, other):
        if type(other) is not NodeId:
            return False
        assert (isinstance(other, NodeId))

        return other.osm_node_id == self.osm_node_id and other.geohash == self.geohash

    def __ne__(self, other):
        return not (self is other)

    def __repr__(self):
        return "NodeId: <osm_node_id: %s> <geohash: %s>" % (self.osm_node_id, self.geohash)

    def __hash__(self):
        # ToDo: Muss überarbeitet werden. Hashes sind derzeit noch eindeutig. Vielleicht einfach self.osm_node_id % p
        #  (wobei p eine ausreichend große Primzahl ist).
        return self.osm_node_id


class Node:

    def __init__(self, node_id: NodeId, lat_lon: tuple):
        """
        :param id: id from OSM Overpass API
        :param lat_lon: tuple with the float position values lat and lon
        """

        self.__id = node_id
        self.__latLon = lat_lon
        self.__tags = {}
        self.__links = []
        self.__parent_link = None

    def set_parent_link(self, link):
        self.__parent_link = link

    def get_parent_link(self):
        return self.__parent_link

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

    def to_geo_json(self):
        """
        :return: Gibt den Knoten im GeoJson-Format (als String) zurück.
        """
        # TODO KP: Macht das Sinn hier sowas zu erstellen oder lieber an einer anderen Stelle?

    def to_wkt(self):
        """:return: Gibt den Knoten im WKT-Format (als String) zurück."""
        return "POINT(%s %s)" % (self.get_lat(), self.get_lon())

    def __repr__(self):
        return "Node: <id: %s> <latLon: %s>" % (self.__id, self.__latLon)
