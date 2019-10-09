from src.geo_utils import great_circle, get_bbox_from_point
from src.map_service import MapService
from src.models.bounding_box import BoundingBox
from src.geo_hash_wrapper import GeoHashWrapper


class LinkDistance:

    _map_service = MapService()

    def __init__(self, pos: tuple):
        # (lat, lon) beschreibt den Punkt, in dessen Umkreis Links gesucht werden.
        # Dabei werden die Abstände von (lat, lon) zu den jeweiligen Links mittels
        # Ortogonalprojektion bestimmt.
        self._pos = pos
        self._lat = pos[0]
        self._lon = pos[1]
        # Ortogonalprojektion von Punkt auf Link
        self._latMatched = None
        # Ortogonalprojektion von Punkt auf Link
        self._lonMatched = None

        # distance zw. punkt und ortogonalprojekton von Punkt auf Link
        self.distance = None

        # Fraction beschreibt die Position auf dem Link. (latMatched, lonMatched)
        # liegt ja nämlich vielleicht  irgendwo in der Mitte des Links, z.B. F=0.5
        # F=0: StartKnoten, F=1: EndKnoten, F=0.5 : mitte des Links,....
        self.fraction = None

        # Das dazugehörige Link-Objekt
        self.Link = None

    def get_matched(self):
        """
        :return:
        """
        bbox = get_bbox_from_point(self._pos)
        nodes = self._map_service.get_nodes_in_bounding_box(bbox)
        for n in nodes:

        return
