"""
Description: This class represents the geometry of a bounding box. It also offers some methods especially for
determining the (geometric) relation of  a BoundingBox to a node/link/other BoundingBox.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz"""

import geohash2 as geohash
import src.models.link as link

from .node import Node

from ..geo_utils import number_is_in_interval, first_interval_contains_second_interval
from ..geo_utils import convert_meter_2_lon, convert_meter_2_lat, overlap_intervals


class BoundingBox:

    def __init__(self, south: float, west: float, north: float, east: float):
        self.south = south
        self.west = west
        self.north = north
        self.east = east

    def __contains__(self, item):
        if isinstance(item, Node):
            return self.contains_node(item)
        elif isinstance(item, BoundingBox):
            return self.contains_bbox(item)
        elif isinstance(item, link.Link):
            return self.contains_link(item)

        else:
            raise TypeError("{} is not supported by this method.".format(type(item)))

    def contains_link(self, link):
        """
        Returns True if self and the bounding box of link overlap.
        :param link: Link-Object
        :return: bool
        """

        return link.get_bbox().overlap(self)

    def contains_node(self, node: Node):
        """
        Returns True if node is located in self.
        :param node: Node-Object
        :return: bool
        """
        return (number_is_in_interval(node.get_lat(), (self.south, self.north), 90) and
                number_is_in_interval(node.get_lon(), (self.west, self.east), 180))

    def contains_bbox(self, other):
        """
        Returns True if self contains other. Remark: In case of self == other, True is returned.
       :param other: BoundingBox-Object
       :return: bool
        """

        if self == other:
            return True

        lat_interval_1 = (self.south, self.north)
        lat_interval_2 = (other.south, other.north)

        if not first_interval_contains_second_interval(lat_interval_1, lat_interval_2, 90):
            return False

        lon_interval_1 = (self.west, self.east)
        lon_interval_2 = (other.west, other.east)

        if not first_interval_contains_second_interval(lon_interval_1, lon_interval_2, 180):
            return False

        return True

    def __eq__(self, other):
        if not isinstance(other, BoundingBox):
            raise TypeError("{} is not supported by this method.".format(type(other)))

        return self.south == other.south and self.west == other.west and \
               self.north == other.north and self.east == other.east

    def __str__(self):
        return "(%s,%s,%s,%s)" % (self.south, self.west, self.north, self.east)

    def overlap(self, other_bbox):
        """
        Returns true if the self and other_bbox overlap. Remark: If self and other_bbox are only touching at their edges
        False is returned.
        :param other_bbox: BoundingBox-Object
        :return bool
        """
        if self == other_bbox:
            return True

        lat_interval_1 = (self.south, self.north)
        lat_interval_2 = (other_bbox.south, other_bbox.north)

        if not overlap_intervals(lat_interval_1, lat_interval_2, 90):
            # Hier wird wird nie ein overflow passieren
            return False

        lon_interval_1 = (self.west, self.east)
        lon_interval_2 = (other_bbox.west, other_bbox.east)

        if not overlap_intervals(lon_interval_1, lon_interval_2, 180):
            return False

        return True

    @staticmethod
    def get_bbox_from_point(pos, radius=1):
        """
        Returns a Bounding Box with pos as center. Radius is the distance (in meter) from center to the south/west/
        north/east-border of the Bounding Box.
        :param pos: tuple
        :param radius: int
        :return: BoundingBox-Object
        """

        lat, lon = pos
        radius_as_lat = convert_meter_2_lat(radius)
        radius_as_lon = convert_meter_2_lon(radius, lat)

        return BoundingBox(lat - radius_as_lat, lon - radius_as_lon, lat + radius_as_lat, lon + radius_as_lon)

    @staticmethod
    def from_geohash(geo_hash: str):
        """
        Returns a Bounding Box which covers the Tile with the specified geohash.
        :param geo_hash: str
        :return: BoundingBox-Object
        """
        bbox = geohash.decode_exactly(geo_hash)
        return BoundingBox(bbox[0] - bbox[2], bbox[1] - bbox[3], bbox[0] + bbox[2], bbox[1] + bbox[3])
