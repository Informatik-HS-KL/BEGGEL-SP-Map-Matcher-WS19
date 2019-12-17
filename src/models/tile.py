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
        :param nodes: dict {NodeId-Object: Node-Object}
        :param links: dict {LinkId-Object: Link-Object}
        """
        self._nodes = nodes
        self._links = links
        self._geohash = geohash

    def get_geohash(self):
        """
        :return: str
        """
        return self._geohash

    def add_node(self, node):
        """
        :param node: Node-Object
        :return: None
        """
        self._nodes.update({node.get_id(): node})

    def add_link(self, link):
        """
        :param link: Link-Object
        :return:
        """
        self._links.update({link.get_id(), link})

    def get_node(self, nodeid):
        """
        :param nodeid: NodeId-Object
        :return: Node-Object
        """

        return self._nodes.get(nodeid, None)

    def get_node_from_osm_id(self, osmid):
        """
        :param osmid: int
        :return: Node Object
        """
        res = list(filter(lambda n: n.get_osm_id() == osmid, self._nodes))
        if len(res) == 1:
            return self._nodes.get(res[0])
        return None

    def get_nodes(self):
        """
        :return: list(Node-Object)
        """
        return self._nodes.values()

    def get_nodes_with_keys(self):
        """
        :return: dict {NodeId-Object: Node-Object}
        """
        return self._nodes

    def get_links(self):
        """
        :return: list(Link-Object)
        """
        return self._links.values()

    def get_links_with_keys(self):
        """
        :return: dict {LinkId-Object: Link-Object}
        """
        return self._links

    def get_link(self, link_id: LinkId):
        """
        :return: Link-Object
        """
        return self._links[link_id]

