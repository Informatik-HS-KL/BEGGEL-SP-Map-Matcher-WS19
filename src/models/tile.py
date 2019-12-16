"""
Description: One way to encode a geographic coordinate, rather an area, is to use a geohash
(https://en.wikipedia.org/wiki/Geohash). In doing so, the earth is split into tiles and each tile can be split into
further tiles, depending on how accurate the encoding should be. Now a Tile-Object represents not only the geographic
dimensions of such a tile, but also the Node- and Link-Objects which are located within this tile.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

from .link_id import LinkId


class Tile:

    def __init__(self, geohash, nodes: dict, links: dict):
        """

        :param geohash: str
        :param nodes: dict {nodeid: node}
        :param links: dict {linkid:link}
        """

        self.__nodes = nodes
        self.__links = links
        self.__geohash = geohash

    def get_geohash(self):
        return self.__geohash

    def add_node(self, node):
        self.__nodes.update({node.get_id(): node})

    def add_link(self, link):
        """
        :param link:
        :return:
        """
        self.__links.update({link.get_id(), link})

    def get_node(self, nodeid):
        """
        :param nodeid: NodeId Object
        :return: Node
        """

        return self.__nodes.get(nodeid, None)

    def get_node_from_osm_id(self, osmid):
        """
        :param osmid: int
        :return: Node Object
        """
        res = list(filter(lambda n: n.osm_node_id == osmid, self.__nodes))
        if len(res) == 1:
            return self.__nodes.get(res[0])
        return None

    def get_nodes(self):
        """
        :return: list [node,..]
        """
        return self.__nodes.values()

    def get_nodes_with_keys(self):
        """
        :return: dict {nodeid: node}
        """
        return self.__nodes

    def get_links(self):
        """
        :return: list [link, ..]
        """
        return self.__links.values()

    def get_links_with_keys(self):
        """
        :return: dict {linkid: link}
        """
        return self.__links

    def get_link(self, link_id: LinkId):
        """
        :return: Link
        """
        return self.__links[link_id]

    def get_geohash(self):
        """
        Geohash from self
        :return: str
        """
        return self.__geohash
