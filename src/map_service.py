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
from src.geo_utils import great_circle

from . import CONFIG


def __one_of_the_nodes_in_circle(points, circle_center_latlon, circle_radius):
    """Prüft ob eines der Nodes innerhalb des Zirkels sind"""
    for point in points:
        if abs(great_circle(point, circle_center_latlon)) <= circle_radius:
            return True
    return False


def _get_links_in_circle(links, circle_center_latlon, circle_radius):
    """ Sortiert Links, die nicht in dem Kreis sind aus"""
    links_in_circle = []
    for link in links:
        points = link.get_geometry()
        if __one_of_the_nodes_in_circle(points, circle_center_latlon, circle_radius):
            links_in_circle.append(link)
    return links_in_circle


def get_smaller_tile(tile, smaller_geohash_str):
    gt_links = tile.get_links()
    gt_nodes = tile.get_nodes()
    nodes = {}
    links = {}
    way_ids = set()
    for node in gt_nodes:  # alle Nodes, die direkt im Tile liegen
        if node.get_id().geohash[:len(smaller_geohash_str)] == smaller_geohash_str:
            nodes[node.get_id()] = node

    for link in gt_links:  # alle Links, die direkt im Tile liegen
        s_node_id = link.get_node_ids()[0]
        e_node_id = link.get_node_ids()[len(link.get_node_ids()) - 1]

        if (s_node_id.geohash[:len(smaller_geohash_str)] == smaller_geohash_str or
                e_node_id.geohash[:len(smaller_geohash_str)] == smaller_geohash_str):
            way_ids.add(link.get_link_id().osm_way_id)
            links[link.get_link_id()] = link
        else:  # wenn Link nur mit einem Node zwischen Start und ende im Tile liegen
            for n_id in link.get_node_ids():
                if n_id in nodes:
                    links[link.get_link_id()] = link
                    break

    for link in gt_links:  # alle Links, die auf einem Weg im Tile liegen
        if link not in links and link.get_way_osm_id() in way_ids:
            links[link.get_link_id()] = link

    for link in gt_links:  # Alle nodes aus den nachgeladenen Links
        for node_id in link.get_node_ids():
            if node_id not in nodes:
                nodes[node_id] = tile.get_node(node_id)

    return Tile(smaller_geohash_str, nodes, links)


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

        if len(geohash_str) == self._geoHashLevel:
            return self.__get_tile(geohash_str)

        if len(geohash_str) > self._geoHashLevel:
            tile = self.__get_tile(geohash_str[:self._geoHashLevel])
            small_tile = get_smaller_tile(tile, geohash_str)
            return small_tile

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
            for linksid, link in tile.get_links_with_keys().items():
                if linksid.osm_way_id == way_id:
                    result.append(link)

        return result

    # def get_linkdistances_in_radius(self, pos, max_distance, max_nbr=10):
    def get_linkdistances_in_radius(self, pos, max_distance):
        """ Match wenn Link Bbox mit pos und radius überlappt
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
        linkdists.sort(key=lambda l: l.get_distance())
        return linkdists

    def get_node(self, nodeid: NodeId):
        """
        :param nodeid:
        :return: Node-Object
        """
        tile = self.get_tile(nodeid.geohash[:self._geoHashLevel])
        return tile.get_node(nodeid)
