from enum import Enum
from abc import ABC, abstractmethod
from src.geo_utils import dijsktra

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

    def set_start_link(self, link):
        """
        Setter start link
        :return:
        """
        self.start_link = link

    def set_end_link(self, link):
        """
        setter end link
        :return:
        """

        self.end_link = link

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
    def compute(self):
        """
        Computes Route
        :return: [nodes]
        """

        if not self.start_link or not self.end_link:
            raise RoutingException("Start or End Link not given")


class RouterDijkstra(Router):
    """
    Derived Class with Dijkstra implementation
    """

    def __init__(self):
        super().__init__()

    def compute(self, weight_property=0):
        """
        Computes Route with Dijkstra
        :param: weight_property = 0 are lenth as weight factor
        :return: [nodes]
        """

        super().compute()
        s, n = self.get_start_link(), self.get_end_link()
        return dijsktra(s, n, "length")

