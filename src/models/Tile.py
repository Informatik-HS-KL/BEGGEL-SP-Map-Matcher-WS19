from src.models.Links import Link


class Tile:
       ## maps nodeId --> Node object

    def __init__(self, geohash, nodes: dict, links: list):
        """"""

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
        self.__links.append(link)

    def get_node(self, osmid: int):
        """
        :param osmid: int
        :return: Node
        """
<<<<<<< Updated upstream:src/models/Tile.py
        return self.__nodes[osmid]

=======
        return self.__nodes.get(osm_id, None)
>>>>>>> Stashed changes:src/models/tile.py

    def get_nodes(self):
        """
        :return:
        """
        return self.__nodes.values()

    def get_links(self):
        """"""
        return self.__links

    def get_neigbors(self):
        """

        :return:
        """
        # TODO