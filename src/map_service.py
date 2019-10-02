"""
"""

from src.geo_hash_wrapper import GeoHashWrapper
from src.over_pass_wrapper import OverpassWrapper
from src.models.bounding_box import BoundingBox
from src.models.link import LinkId
from src.models.node import NodeId
from src.models.tile import Tile
import geohash2 as geohash


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
            tile = self.get_tile(geoHash)
            for node in tile.get_nodes():
                if node in bbox:
                    ret.append(node)

        return ret

    def get_links_in_bounding_box(self, bbox):
        pass

    def get_tile(self, geohash):
        """Stellt sicher das immer nur Tile's mit dem vorgegebenen Level geladen werden """
        if len(geohash) >= self._geoHashLevel:
            return self.__get_tile(geohash[:self._geoHashLevel])
        nodes = {}
        links = {}
        bbox = geohash.decode_exactly(geohash)
        for tile_geoHash in GeoHashWrapper().get_geohashes(bbox, self._geoHashLevel):
            nodes.update(self.__get_tile(tile_geoHash).get_nodes())
            links.update(self.__get_tile(tile_geoHash).get_links())
        return Tile(geohash, nodes, links)

    def __get_tile(self, geohash):
        """Gibt das entprechende Tile zurück. Liegt es noch nicht im Tile-Cache,
        so wird es erst noch geladen und im Cache gespeichert."""
        if geohash not in self._tileCache:
            self._tileCache[geohash] = OverpassWrapper().load_tile(geohash)

        return self._tileCache[geohash]

    def get_all_cached_tiles(self):
        return self._tileCache

    def get_link_by_id(self, link_id: LinkId):
        """Gibt den Link mit der entsprechenden Id zurück."""
        return self.get_link(link_id.osm_way_id, link_id.start_node_id)

    def get_link(self, way_id, start_node_id: NodeId):
        """Gibt den Link zurück, der den entsprechenden Knoten als Startknoten hat
        und Teil des entsprechenden Way's ist"""
        tile = self.get_tile(start_node_id.geohash[:self._geoHashLevel])
        pass

    def get_links(self, way_id):
        pass

    def get_links_in_radius(self, pos, max_distance):
        pass
