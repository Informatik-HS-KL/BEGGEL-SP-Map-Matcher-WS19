"""
Description: Sometimes you want to find links within a certain radius around a certain position. In this context it
is usually interesting to get further information about a link that was found. A LinkDistance-Object encapsulates all
these information, e.g. the shortest distance between the point and the link or the nearest position on the link.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

import math
from ..geo_utils import great_circle


class LinkDistance:

    def __init__(self, pos: tuple, link):
        """
        :param pos: tuple
        :param link: Link-Object
        """

        self._lat_lon = pos
        self._matched_point = None
        self._fraction = None
        self._link = link
        self._initialize_matched_point_and_fraction()
        self._distance = great_circle(self._matched_point, self._lat_lon)

    def get_distance(self):
        """
        Returns the calculated distance between self_link and self_lat_lon.
        :return: float
        """
        return self._distance

    def get_fraction(self):
        """
        :return: float
        """
        return self._fraction

    def _calc_fraction(self, link_segments, involved_segment):
        """
        Take note, that this function, should only be invoked if self._matched_point is already initialized.
        :param link_segments: the segments of the link
        :param involved_segment: the link segment, which contains self._matched_point.
        :return: None
        """
        distance = 0
        for seg in link_segments:
            if seg == involved_segment:
                distance += great_circle(seg[0], self._matched_point)
                if not self._link.get_length() == 0.0:
                    # Links, die aus einem einzigen Punkt bestehen. (Falsche Daten Overpass)
                    return distance / self._link.get_length()
                return 0
            else:
                distance += great_circle(seg[0], seg[1])

    @staticmethod
    def _calc_shrink_factor(a_lat_deg, b_lat_deg):
        """Taken from:
        https://github.com/graphhopper/graphhopper/blob/master/api/src/main/java/com/graphhopper/util
        /DistanceCalcEarth.java
        :param a_lat_deg: float
        :param b_lat_deg: float
        """
        return math.cos(math.radians((a_lat_deg + b_lat_deg) / 2))

    def _calc_matched_point_of_link_segment(self, a: tuple, b: tuple) -> tuple:
        """
        Calculates the matched point of a link_segment like the method calcCrossingPointToEdge in:
        https://github.com/graphhopper/graphhopper/blob/master/api/src/main/java/com/graphhopper/util
        /DistanceCalcEarth.java
        Take note, that here is essentially performed a orthogonal projection.

        :param a: beginning of the link-segment
        :param b: end of the link-segment
        :return: matched point of the link-segment
        """

        a_lat_deg, a_lon_deg = a
        b_lat_deg, b_lon_deg = b
        r_lat_deg, r_lon_deg = self._lat_lon

        shrink_factor = self._calc_shrink_factor(a_lat_deg, b_lat_deg)

        # _lat, _lon are cartesian coordinates
        a_lat = a_lat_deg
        a_lon = a_lon_deg * shrink_factor

        b_lat = b_lat_deg
        b_lon = b_lon_deg * shrink_factor

        r_lat = r_lat_deg
        r_lon = r_lon_deg * shrink_factor

        delta_lon = b_lon - a_lon
        delta_lat = b_lat - a_lat

        matched_point = None

        norm = delta_lon * delta_lon + delta_lat * delta_lat
        factor = ((r_lon - a_lon) * delta_lon + (r_lat - a_lat) * delta_lat) / norm

        if factor >= 1:
            matched_point = b
        elif factor <= 0:
            matched_point = a
        else:
            c_lat = a_lat + factor * delta_lat
            c_lon = a_lon + factor * delta_lon
            matched_point = (c_lat, c_lon / shrink_factor)

        return matched_point

    def _initialize_matched_point_and_fraction(self):
        """
        Performs the initialization of the attributes _matched_point and _fraction.
        :return: None
        """

        link_segments = self._link.get_link_segments()
        min_distance = 20037000  # biggest range of earth: 40074000 Meter
        matched_point = None
        involved_segment = None
        for seg in link_segments:
            candidate = self._calc_matched_point_of_link_segment(seg[0], seg[1])
            distance = great_circle(candidate, self._lat_lon)

            if distance < min_distance:
                min_distance = distance
                matched_point = candidate
                involved_segment = seg

        self._matched_point = matched_point
        self._fraction = self._calc_fraction(link_segments, involved_segment)

    def get_link(self):
        """
        :return: Link-Object
        """
        return self._link

    def get_point(self):
        """
        :return: tuple(lat, lon)
        """
        return self._lat_lon
