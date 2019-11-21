from abc import ABC, abstractmethod
from src.utils.routing import point_to_point_dijkstra, link_to_link_dijkstra, ShortestPath, WeightCalculator, \
    dijkstra_routing
from src.models.link_user import LinkUser


class RoutingException(Exception):
    """ IF any stuff in Routing goes wrong"""
    pass



class Router(ABC):
    """
    ABSTRACT BASE CLASS
    """

    def __init__(self):
        """ initialize memebr with none
        """
        self.start_link = None
        self.end_link = None
        self.s_fraction = None
        self.e_fraction = None
        self.s_from_start_to_end = None
        self.e_from_start_to_end = None

    def set_start_link(self, link, fraction=0.0, from_start_to_end: bool = True):
        """
        Setter start link
        :param link the link from which you want to drive
        :param fraction the position on the link to go to
        :param from_start_to_end the direction
        :return:
        """
        self.start_link = link
        self.s_fraction = fraction
        self.s_from_start_to_end = from_start_to_end

    def set_end_link(self, link, fraction=0.0, from_start_to_end: bool = True):
        """
        :param link the link to go to
        :param fraction the position on the link to go to
        :param from_start_to_end the direction
        setter end link
        :return:
        """
        self.end_link = link
        self.e_fraction = fraction
        self.e_from_start_to_end = from_start_to_end

    def get_start_link(self):
        """
        getter
        :return: Link Object
        """
        return self.start_link

    def get_end_link(self):
        """
        getter
        :return: Link Object
        """

        return self.end_link

    @abstractmethod
    def compute(self,  wight_function=ShortestPath):
        """
        Computes Route
        :return: [nodes]
        """

        if not self.start_link or not self.end_link:
            raise RoutingException("Start or End Link not given")


class RouterBaseDijkstra(Router):
    """
    Derived Class with Dijkstra implementation
    """

    def __init__(self, link_user: LinkUser):
        super().__init__()
        self.link_user = link_user

    def compute(self, wight_function=WeightCalculator):
        """
        Computes Route with Dijkstra
        :param: weight_property = 0 are lenth as weight factor
        :return: [nodes]
        """

        super().compute()
        s, n = self.get_start_link(), self.get_end_link()
        return point_to_point_dijkstra(s, n)


class RouterLinkDijkstra(Router):
    """
    Derived Class with Dijkstra implementation
    """

    def __init__(self, link_user: LinkUser):
        super().__init__()
        self.link_user = link_user

    def compute(self, wight_function=ShortestPath()):
        """
        Computes Route with Dijkstra
        :param: weight_property = 0 are lenth as weight factor
        :return: [nodes]
        """

        super().compute()
        s, n = self.get_start_link(), self.get_end_link()
        return link_to_link_dijkstra(s, n, wight_function)


class RouterDijkstra(Router):
    """
    Derived Class with Dijkstra implementation
    """

    def __init__(self, link_user: LinkUser):
        super().__init__()
        self.link_user = link_user

    def compute(self, wight_function=ShortestPath()):
        """
        Computes Route with Dijkstra
        :param: weight_property = 0 are lenth as weight factor
        :return: [nodes]
        """

        super().compute()
        s, n = self.get_start_link(), self.get_end_link()
        nodes = dijkstra_routing(s, self.s_fraction, n, self.e_fraction, wight_function, True, self.link_user)
        for node in nodes:
            print(node.get_id())
            print(",")
        return nodes
