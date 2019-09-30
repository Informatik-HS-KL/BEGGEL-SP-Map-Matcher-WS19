"""
"""

from src.geo_hash_wrapper import GeoHashWrapper
from src.over_pass_wrapper import OverpassWrapper
from src.models.bounding_box import BoundingBox


class MapService:
    """"""
    # maps geohash --> Tile class
    _tileCache = {}
    _geoHashLevel = 5

    def get_nodes_in_bounding_box(self, bbox: BoundingBox):
        """
        Knoten einer Boudingbox zurückgeben.
        Knoten werden aus den Tiles geladen
        :param bbox:
        :return:
        """
        ret = []

        for geoHash in GeoHashWrapper().get_geohashes(bbox, self._geoHashLevel):
            tile = self.get_or_load_tile(geoHash)
            for node in tile.get_nodes():
                if node in bbox:
                    ret.append(node)

        return ret

    def get_links_in_bounding_box(self, bbox):
        pass

    def get_or_load_tile(self, geohash):
        """"""
        if geohash not in self._tileCache:
            self._tileCache[geohash] = OverpassWrapper().load_tile(geohash)

        return self._tileCache[geohash]

    def get_all_cached_tiles(self):
        return self._tileCache

    def load_link(self, id):
        pass

    def load_link(self, way_id, start_node):
        pass

    def load_links(self, way_id):
        pass

    def get_links_in_radius(self, pos, max_distance):
        pass
