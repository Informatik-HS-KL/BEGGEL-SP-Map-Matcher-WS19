from src.geo_utils import orthogonal_projection, vector_subtraction, vector_addition, great_circle


class LinkDistance:

    def __init__(self, pos: tuple, link):
        # (lat, lon) beschreibt den Punkt, in dessen Umkreis Links gesucht werden.
        # Dabei werden die Abstände von (lat, lon) zu den jeweiligen Links mittels
        # Ortogonalprojektion bestimmt.
        self._lat_lon = pos  # Koordinaten in deren Umkreis links gesucht wurden
        # Ortogonalprojektion von Punkt auf Link
        self._matched_point: tuple = None
        # Ortogonalprojektion von Punkt auf Link

        # distance zw. punkt und ortogonalprojekton von Punkt auf Link
        self.distance = None

        # Fraction beschreibt die Position auf dem Link. (latMatched, lonMatched)
        # liegt ja nämlich vielleicht  irgendwo in der Mitte des Links, z.B. F=0.5
        # F=0: StartKnoten, F=1: EndKnoten, F=0.5 : mitte des Links,....
        self.fraction = None

        # Das dazugehörige Link-Objekt
        self.Link = link

        self.init = False

    def lazy_load(self):
        self.init = True
        link_vector = vector_subtraction(self.Link.get_end_node().get_latlon(), self.Link.get_start_node().get_latlon())
        point_vector = vector_subtraction(self._lat_lon, self.Link.get_start_node().get_latlon())
        self._matched_point = vector_addition(
            orthogonal_projection(point_vector, link_vector), self.Link.get_start_node().get_latlon())
        self.distance = great_circle(self._matched_point, self._lat_lon)
        distance = great_circle(self.Link.get_start_node().get_latlon(), self._matched_point)
        self.fraction = self.Link.get_length() / distance

    def get_distance(self):
        if not self.init:
            self.lazy_load()
        return self.distance

    def get_fraction(self):
        if not self.init:
            self.lazy_load()
        return self.fraction