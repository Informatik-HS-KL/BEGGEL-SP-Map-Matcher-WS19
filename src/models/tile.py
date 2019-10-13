from src.models.link_id import LinkId

class Tile:
    ## maps nodeId --> Node object

    def __init__(self, geohash, nodes: dict, links: dict):
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
        self.__links.update(link, link)

    def get_node(self, nodeid):
        """
        :param osm_id: int
        :return: Node
        """

        return self.__nodes.get(nodeid, None)

    def get_nodes(self):
        """
        :return:
        """
        return self.__nodes.values()

    def get_nodes_with_keys(self):
        """
        :return:
        """
        return self.__nodes

    def get_links(self):
        """"""
        return self.__links

    def get_link(self, link_id: LinkId):
        """
        :return:
        """
        return self.__links[link_id]


    def get_geohash(self):
        return self.__geohash

    def get_nachbar(self):
        nachbar = Tile[8]
        nachbar[0] = get_right(get_top(self))
        nachbar[1] = get_top(self)
        nachbar[2] = get_left(get_top(self))
        nachbar[3] = get_right(self)
        nachbar[4] = get_left(self)
        nachbar[5] = get_right(get_below(self))
        nachbar[6] = get_below(self)
        nachbar[7] = get_left(get_below(self))


def get_top(other):
    return other.get_geohash()


def get_below(other):
    return other.get_geohash()


def get_left(other):
    return other.get_geohash()


def get_right(other):
    return other.get_geohash()
