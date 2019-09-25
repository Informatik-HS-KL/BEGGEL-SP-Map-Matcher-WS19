from src.models.links import Link


class Tile:
    ## maps nodeId --> Node object

    def __init__(self, geohash, nodes: dict, links: list):
        """"""

        self.__nodes = nodes
        self.__links = links
        self.__geohash = geohash

    def add_node(self, node):
        self.__nodes.update({node.get_id(): node})

    def add_link(self, link):
        """
        :param link:
        :return:
        """
        self.__links.append(link)

    def get_node(self, osm_id: int):
        """
        :param osm_id: int
        :return: Node
        """
        return self.__nodes[osm_id]

    def get_nodes(self):
        """
        :return:
        """
        return self.__nodes.values()

    def get_links(self):
        """"""
        return self.__links
