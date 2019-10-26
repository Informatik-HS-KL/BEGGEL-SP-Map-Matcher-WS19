"""
Description: This class represents the geometry of a bounding box. It also offers some methods especially for
determining the (geometric) relation of  a BoundingBox to a node/link/other BoundingBox.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz"""


from src.models.node import Node
from src.models.link import Link
import src.geo_utils as ut
import geohash2 as Geohash


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
        elif isinstance(item, Link):
            return self.contains_link(item)

        else:
            raise TypeError("{} is not supported by this method.".format(type(item)))

    def contains_link(self, link: Link):
        """
        :param link:
        :return:
        """

        return link.get_start_node() in self or link.get_end_node() in self

    def contains_node(self, node: Node):
        return (ut.number_is_in_interval(node.get_lat(), (self.south, self.north), 90) and
                ut.number_is_in_interval(node.get_lon(), (self.west, self.east),  180))

    def contains_bbox(self, other):
        """Diese Methode überprüft, ob other eine Teilmenge von self ist.
                Die Rückgabe erfolgt als boolean. Beachte: self == other liefert ebenfalls True."""

        if self == other:
            return True

        lat_interval_1 = (self.south, self.north)
        lat_interval_2 = (other.south, other.north)

        if not ut.first_interval_contains_second_interval(lat_interval_1, lat_interval_2, 90):
            return False

        lon_interval_1 = (self.west, self.east)
        lon_interval_2 = (other.west, other.east)

        if not ut.first_interval_contains_second_interval(lon_interval_1, lon_interval_2, 180):
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
        """Diese Methode überprüft, ob sich zwei Bounding-Boxen überlappen.
           Rückgabe erfolgt als boolean.
           Beachte: Wenn die beiden Bounding-Boxen sich lediglich an ihren Rändern berühren, so zählt dies NICHT als Überlappung"""
        if self == other_bbox:
            return True

        lat_interval_1 = (self.south, self.north)
        lat_interval_2 = (other_bbox.south, other_bbox.north)

        if not ut.overlap_intervals(lat_interval_1, lat_interval_2, 90):
            # Hier wird wird nie ein overflow passieren
            return False

        lon_interval_1 = (self.west, self.east)
        lon_interval_2 = (other_bbox.west, other_bbox.east)

        if not ut.overlap_intervals(lon_interval_1, lon_interval_2, 180):
            return False

        return True

    @staticmethod
    def get_bbox_from_point(pos, radius=1):
        """
        nimmt den punkt als mitte einer Bounding Box mit dem gegebenen "radius" in meter
        :param pos:
        :param radius:
        :return:
        """

        lat, lon = pos
        radius_as_lat = ut.convert_meter_2_lat(radius)
        radius_as_lon = ut.convert_meter_2_lon(radius)

        return BoundingBox(lat - radius_as_lat, lon - radius_as_lon, lat + radius_as_lat, lon + radius_as_lon)

    def get_bbox_from_points(self, min):
        pass

    @staticmethod
    def from_geohash(geohash):
        bbox = Geohash.decode_exactly(geohash)
        return BoundingBox(bbox[0] - bbox[2], bbox[1] - bbox[3], bbox[0] + bbox[2], bbox[1] + bbox[3])
