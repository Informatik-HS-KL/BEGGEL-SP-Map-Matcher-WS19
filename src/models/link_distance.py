from src.geo_utils import orthogonal_projection, vector_subtraction, vector_addition, great_circle, vectors_have_same_direction, vector_norm


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
        Diese Methode lädt bzw. berechnet die Attribute self._matched_point, self.distance, self.fraction und
        self.Link = link. Hierfür wird im Wesentlichen eine Orthogonalprojektion durchgeführt.
        :return: void
        """

        # _lazy_load schließt die Initialisierung des Objektes ab.
        self.init = True

        # Darstellung des Links als Vektor vom Start- zum Endknoten
        link_vector = vector_subtraction(self.link.get_end_node().get_latlon(), self.link.get_start_node().get_latlon())

        # Vektor vom Startknoten des Links zu dem Punkt, in dessen Umkreis nach Links gesucht wurde.
        point_vector = vector_subtraction(self._lat_lon, self.link.get_start_node().get_latlon())

        # Die Komponente von point_vector die parallel zu link_vector verläuft.
        parallel_component = orthogonal_projection(point_vector, link_vector)

        # Ermittlung von self._matched_point
        if vectors_have_same_direction(parallel_component, link_vector):

            # Wenn Orthogonalprojektion nicht auf dem Link landet und sich self.pos näher am Endknoten befindet.
            if vector_norm(parallel_component) > vector_norm(link_vector):
                self._matched_point = self.link.get_end_node.get_latlon()
            # Wenn die Orthogonalprojektion auf dem Link landet ("Schönwetter-Fall)
            else:
                self._matched_point = vector_addition(self.link.get_start_node().get_latlon(), parallel_component)

        else:  # Wenn Orthogonalprojektion nicht auf dem Link landet und sich self.pos näher am Startknoten befindet.
            self._matched_point = self.link.get_start_node.get_latlon()
            
        self.distance = great_circle(self._matched_point, self._lat_lon)

        distance_from_start_node_to_matched_point = great_circle(self.link.get_start_node().get_latlon(), self._matched_point)
        self.fraction = self.link.get_length() / distance_from_start_node_to_matched_point

    def get_distance(self):
        if not self.init:
            self._lazy_load()
        return self.distance

    def get_fraction(self):
        if not self.init:
            self._lazy_load()
        return self.fraction
