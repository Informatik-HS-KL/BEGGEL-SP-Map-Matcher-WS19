from .Node import Node
import src.utils as ut


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
        else:
            raise TypeError("{} is not supported by this method.".format(type(item)))

    def contains_node(self, node):
        pass

    def contains_bbox(self, other):
        """Diese Methode überprüft, ob other eine Teilmenge von self ist.
                Die Rückgabe erfolgt als boolean. Beachte: self == other liefert ebenfalls True."""

        if self == other:
            return True

        lat_interval_1 = (self.south, self.north)
        lat_interval_2 = (other.south, other.north)

        if not ut.firstIntervalContainsSecondInterval(lat_interval_1, lat_interval_2, 90):
            return False

        lon_interval_1 = (self.west, self.east)
        lon_interval_2 = (other.west, other.east)

        if not ut.firstIntervalContainsSecondInterval(lon_interval_1, lon_interval_2, 180):
            return False

        return True

    def __eq__(self, other):
        if not isinstance(other, BoundingBox):
            raise TypeError("{} is not supported by this method.".format(type(other)))

        return self.south == other.south and self.west == other.west and \
               self.north == other.north and self.east == other.east

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








