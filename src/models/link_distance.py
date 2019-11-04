"""
Description: Sometimes you want to find links within a certain radius around a certain position. In this context it is usually
interesting to get further information about a link that was found. A LinkDistance-Object encapsulates all these
information, e.g. the shortest distance between the point and the link or the nearest position on the link.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz"""


from src.geo_utils import great_circle
import numpy.linalg
import math


class LinkDistance:

    def __init__(self, pos: tuple, link):
        # (lat, lon) beschreibt den Punkt, in dessen Umkreis Links gesucht werden.
        # Dabei werden die Abstände von (lat, lon) zu den jeweiligen Links mittels
        # Ortogonalprojektion bestimmt.

        # Koordinaten in deren Umkreis links gesucht wurden
        self._lat_lon = pos

        # Ortogonalprojektion von Punkt auf Link
        self._matched_point: tuple = None

        # distance zw. punkt und ortogonalprojekton von Punkt auf Link
        self.distance = None

        # Fraction beschreibt die Position auf dem Link. (latMatched, lonMatched)
        # liegt ja nämlich vielleicht  irgendwo in der Mitte des Links, z.B. F=0.5
        # F=0: StartKnoten, F=1: EndKnoten, F=0.5 : mitte des Links,....
        self.fraction = None

        # Das dazugehörige Link-Objekt
        self.link = link

        # Gibt an, ob self schon vollständig initialisiert wurde (für weitere Details siehe _lazy_load(self))
        self.init = False

    def _lazy_load(self):
        """
        Diese Methode schließt die Initialisierung ab.
        :return: void
        """
        self.init = True
        self._initialize_matched_point_and_fraction()
        self.distance = great_circle(self._matched_point, self._lat_lon)

    def get_distance(self):
        if not self.init:
            self._lazy_load()
        return self.distance

    def get_fraction(self):
        if not self.init:
            self._lazy_load()

        return self.fraction

    def _calc_fraction(self, involved_segment):
        """Take note, that this function, should only be invoked if self._matched_point is already initialized."""
        distance = 0

        for seg in self._build_link_segments():
            if seg == involved_segment:
                distance += great_circle(seg[0], self._matched_point)
                self.fraction = distance/self.link.get_length()
                return
            else:
                distance += great_circle(seg[0], seg[1])

    @staticmethod
    def _calc_shrink_factor(a_lat, b_lat):
        """Taken from:
        https://github.com/graphhopper/graphhopper/blob/master/api/src/main/java/com/graphhopper/util
        /DistanceCalcEarth.java """
        return math.cos(math.radians((a_lat + b_lat) / 2))

    @staticmethod
    def _orthogonal_projection(vector_from, vector_to):
        return (numpy.vdot(vector_from, vector_to) / numpy.vdot(vector_to, vector_to)) * vector_to

    def _calc_matched_point_of_link_segment(self, a: tuple, b: tuple) -> tuple:
        """Calculates the matched point of a link_segment like the method calcCrossingPointToEdge in:
        https://github.com/graphhopper/graphhopper/blob/master/api/src/main/java/com/graphhopper/util
        /DistanceCalcEarth.java """

        shrink_factor = LinkDistance._calc_shrink_factor(a[0], b[0])
        segment_vector = numpy.array([b[0], b[1] * shrink_factor]) - numpy.array([a[0], a[1] * shrink_factor])
        point_vector = numpy.array([self._lat_lon[0], self._lat_lon[1] * shrink_factor]) - numpy.array(a)

        orthogonal_projection = LinkDistance._orthogonal_projection(point_vector, segment_vector)

        if orthogonal_projection[0] * segment_vector[0] < 0:
            matched_point_vector = numpy.array(a)

        else:
            if numpy.linalg.norm(orthogonal_projection) > numpy.linalg.norm(segment_vector):
                matched_point_vector = numpy.array(b)
            else:
                matched_point_vector = numpy.array(a) + orthogonal_projection

        matched_point = (matched_point_vector[0], matched_point_vector[1] / shrink_factor)

        return matched_point

    def _initialize_matched_point_and_fraction(self):

        link_segments = self._build_link_segments()
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
        self._calc_fraction(involved_segment)

    def _build_link_segments(self) -> list:
        segments = list()
        for i in range(len(self.link.__geometry) - 1):
            segment = (self.link.__geometry[i], self.link.__geometry[i+1])
            segments.append(segment)

        return segments


