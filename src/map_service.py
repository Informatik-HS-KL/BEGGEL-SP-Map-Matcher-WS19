"""
Description: The MapService is the center of this whole API. That means that the whole functionality this API should
offer is located in the MapService, e.g. getting nodes and links that satisfy certain criteria. Therefore the MapService
is managing the obtainment and caching of Tiles, the latter for improving the performance.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""


from src.geo_hash_wrapper import GeoHashWrapper
from src.models.bounding_box import BoundingBox
from src.models.link_id import LinkId
from src.models.node import NodeId
from src.models.tile import Tile
from src.models.link_distance import LinkDistance

from . import CONFIG


class MapService:
    """"""
    # maps geohash --> Tile class
    _tileCache = {}
    _geoHashLevel = CONFIG.getint("DEFAULT", "geohashlevel")

    def __init__(self):
        """"""
        self.name = "A"


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

        ret = []

        for geoHash in GeoHashWrapper().get_geohashes(bbox, self._geoHashLevel):
            tile = self.get_tile(geoHash)
            for link in tile.get_links():
                if link in bbox:
                    ret.append(link)

        return ret

    def get_tile(self, geohash_str):
        """Stellt sicher das immer nur Tile's mit dem vorgegebenen Level geladen werden """

        if len(geohash_str) >= self._geoHashLevel:
            # TODO kleinerer Geohash zurückgeben
            return self.__get_tile(geohash_str[:self._geoHashLevel])
        nodes = {}
        links = {}
        bbox = BoundingBox.from_geohash(geohash_str)
        for tile_geoHash in GeoHashWrapper().get_geohashes(bbox, self._geoHashLevel):
            nodes.update(self.__get_tile(tile_geoHash).get_nodes_with_keys())
            links.update(self.__get_tile(tile_geoHash).get_links_with_keys())

        return Tile(geohash_str, nodes, links)

    def __get_tile(self, geohash_str):
        """Gibt das entprechende Tile zurück. Liegt es noch nicht im Tile-Cache,
        so wird es erst noch geladen und im Cache gespeichert."""

        # from src.over_pass_wrapper import OverpassWrapperServerSide
        from src.over_pass_wrapper import OverpassWrapperClientSide

        full_geohash_level = CONFIG.getint("DEFAULT", "full_geohash_level")
        OVERPASS_URL = CONFIG.get("DEFAULT", "overpass_url")

        # self.opw = OverpassWrapperServerSide(full_geohash_level, OVERPASS_URL)
        self.opw = OverpassWrapperClientSide(full_geohash_level, OVERPASS_URL)

        if geohash_str not in self._tileCache:
            self._tileCache[geohash_str] = self.opw.load_tile(geohash_str)

        return self._tileCache[geohash_str]

    def get_all_cached_tiles(self):
        return self._tileCache

    def get_link_by_id(self, link_id: LinkId):
        """Gibt den Link mit der entsprechenden Id zurück."""

        tile = self.get_tile(link_id.geohash[:self._geoHashLevel])
        return tile.get_link(link_id)

    def get_link(self, way_id, start_node_id: NodeId):
        """Gibt den Link zurück, der den entsprechenden Knoten als Startknoten hat
        und Teil des entsprechenden Way's ist"""

        tile = self.get_tile(start_node_id.geohash[:self._geoHashLevel])
        return tile.get_link(LinkId(way_id, start_node_id))

    def get_links(self, way_id):
        """
        ACHTUNG: DAS HIER IST NOCH NICHT PERFORMANT
        TODO
        :param way_id:
        :return: [Link, Link]
        """

        result = []
        for geohash, tile in self._tileCache.items():
            print(geohash)
            for linksid, link in tile.get_links_with_keys().items():
                if linksid.osm_way_id == way_id:
                    result.append(link)

        return result

    # beggel-changes
    # def get_linkdistances_in_radius(self, pos, max_distance, max_nbr=10):
    def get_linkdistances_in_radius(self, pos, max_distance):
        """ Pseudo Match: Links deren knoten nicht in der BoundingBox liegt, die von der gegebenen Position ausgeht,
            können nicht erreicht werden.
            Liste wird nach tatsächer distance sortiert und nur die max_nbr geringen Abstände zurückgegeben.
        :param pos:
        :param max_distance:
        :return:
        """

        bbox = BoundingBox.get_bbox_from_point(pos, max_distance)
        links = self.get_links_in_bounding_box(bbox)
        linkdists = []
        for link in links:
            linkdists.append(LinkDistance(pos, link))

        ## sortieren und filtern

        return linkdists

    def get_node(self, nodeid: NodeId):
        """
        :param nodeid:
        :return: Node-Object
        """

        tile = self.get_tile(nodeid.geohash[:self._geoHashLevel])
        return tile.get_node(nodeid)
