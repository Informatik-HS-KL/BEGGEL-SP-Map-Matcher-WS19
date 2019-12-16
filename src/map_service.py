"""
Description: The MapService is the center of this whole API. That means that the whole functionality this API should
offer is located in the MapService, e.g. getting nodes and links that satisfy certain criteria. Therefore the MapService
is managing the obtainment and caching of Tiles, the latter for improving the performance.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

from .geohash_wrapper import GeoHashWrapper
from .models.bounding_box import BoundingBox
from src.models import LinkId, NodeId, Tile, LinkDistance
from src.geo_utils import great_circle
from src.config import MapServiceConfig, CONFIG
from src.utils.overpass_wrapper import OverpassWrapperClientSide


def __one_node_in_circle(points, circle_center_lat_lon, circle_radius):
    """
    Check if one of the points in the circle
    :param points: list of points like [(lat, lon),(lat, lon),...]
    :param circle_center_lat_lon: the center of the circle as tuple (lat, lon)
    :param circle_radius: radius of the circle (unit of measurement like great_circle() Method)
    :return: True if one of the points inside the circle else False
    """
    for point in points:
        if abs(great_circle(point, circle_center_lat_lon)) <= circle_radius:
            return True
    return False


def _get_links_in_circle(links, circle_center_lat_lon, circle_radius):
    """
    Returns a list with links inside the given circle (point and radius)
    The Circle is geometric and no depict of the earth
    :param links: a list with links that may be in a circle
    :param circle_center_lat_lon: the center of the circle as tuple in (lat, lon)
    :param circle_radius: radius of the circle (unit of measurement like great_circle() Method)
    :return: returns a list of all links inside the circle
    """
    links_in_circle = []
    for link in links:
        points = link.get_geometry()
        if __one_node_in_circle(points, circle_center_lat_lon, circle_radius):
            links_in_circle.append(link)
            continue
    return links_in_circle


def _get_smaller_tile(tile, smaller_geohash_str):
    all_links = tile.get_links()
    all_nodes = tile.get_nodes()
    nodes = {}
    links = {}
    osm_ids = set()
    for node in all_nodes:  # alle Nodes, die direkt im Tile liegen
        if node.get_geohash()[:len(smaller_geohash_str)] == smaller_geohash_str:
            nodes[node.get_id()] = node

    for link in all_links:  # alle Links, die direkt im Tile liegen
        for n_id in link.get_node_ids():
            if n_id in nodes:
                osm_ids.add(link.get_id().osm_way_id)
                links[link.get_id()] = link
                break

    for link in all_links:  # alle Links, die auf einem Weg im Tile liegen
        if link not in links and link.get_way_osm_id() in osm_ids:
            links[link.get_id()] = link

    for link in links.values():  # Alle nodes aus den nachgeladenen Links und Nodes
        for node_id in link.get_node_ids():
            if node_id not in nodes:
                nodes[node_id] = tile.get_node(node_id)

    return Tile(smaller_geohash_str, nodes, links)


class MapService:
    """
    Access for API-User
    """

    _tile_cache = {}  # Structure {geohash:Tile class}

    def __init__(self):
        """"""

        self.config = CONFIG
        self._geohash_level = self.config.getint("DEFAULT", "geohashlevel")
        self.overpass_wrapper = OverpassWrapperClientSide(self.config)

    def set_config(self, config_path):
        """
        Sets Custom Config
        :return:
        """

        self.config = MapServiceConfig()
        self.config.read(config_path)
        self._geohash_level = self.config.getint("DEFAULT", "geohashlevel")

    def get_config(self):
        """ Getter
            :return: config Object vom MapServiceConfig
        """

        return self.config

    def set_overpass_wrapper(self, opw):
        """
        Sets Overpass Wrapper which will be use to download tiles from overpass api
        :param opw: Overpass Wrapper Object with custom Config
        :return: none
        """
        self.overpass_wrapper = opw

    def get_nodes_in_bounding_box(self, bbox: BoundingBox):
        """
        Knoten einer Boundingbox zurückgeben.
        Knoten werden aus den Tiles geladen
        :param bbox Object
        :return: List(Node-Object, ...)
        """
        ret = []

        for geoHash in GeoHashWrapper().get_geohashes(bbox, self._geohash_level):
            tile = self.get_tile(geoHash)
            for node in tile.get_nodes():
                if node in bbox:
                    ret.append(node)

        return ret

    def get_links_in_bounding_box(self, bbox):
        """
        :param bbox: BoundingBox-Object
        :return: list(link-Object, ...)
        """
        ret = []

        for geoHash in GeoHashWrapper().get_geohashes(bbox, self._geohash_level):
            tile = self.get_tile(geoHash)
            for link in tile.get_links():
                if link in bbox:
                    ret.append(link)

        return ret

    def get_tile(self, geohash_str):
        """Stellt sicher das immer nur Tile's mit dem vorgegebenen Level geladen werden """

        if len(geohash_str) == self._geohash_level:
            return self.__get_tile(geohash_str)

        if len(geohash_str) > self._geohash_level:
            tile = self.__get_tile(geohash_str[:self._geohash_level])
            small_tile = _get_smaller_tile(tile, geohash_str)
            return small_tile

        nodes = {}
        links = {}
        bbox = BoundingBox.from_geohash(geohash_str)
        for tile_geoHash in GeoHashWrapper().get_geohashes(bbox, self._geohash_level):
            nodes.update(self.__get_tile(tile_geoHash).get_nodes_with_keys())
            links.update(self.__get_tile(tile_geoHash).get_links_with_keys())

        return Tile(geohash_str, nodes, links)

    def __get_tile(self, geohash_str):
        """Gibt das entprechende Tile zurück. Liegt es noch nicht im Tile-Cache,
        so wird es erst noch geladen und im Cache gespeichert.
        """

        if geohash_str not in self._tile_cache:
            self._tile_cache[geohash_str] = self.overpass_wrapper.load_tile(geohash_str)

        return self._tile_cache[geohash_str]

    def get_all_cached_tiles(self):
        """
        :return: dict(geohashstr, Tile-Object)
        """
        return self._tile_cache

    def get_link_by_id(self, link_id: LinkId):
        """Gibt den Link mit der entsprechenden Id zurück."""

        tile = self.get_tile(link_id.get_geohash()[:self._geohash_level])
        return tile.get_link(link_id)

    def get_link(self, way_id, start_node_id: NodeId):
        """Gibt den Link zurück, der den entsprechenden Knoten als Startknoten hat
        und Teil des entsprechenden Way's ist"""

        tile = self.get_tile(start_node_id.get_geohash()[:self._geohash_level])
        return tile.get_link(LinkId(way_id, start_node_id))

    def get_links(self, way_id):
        """
        Returns all Links in way id
        :param way_id:
        :return: [Link, Link]
        """

        result = []
        for geohash, tile in self._tile_cache.items():
            for linksid, link in tile.get_links_with_keys().items():
                if linksid.osm_way_id == way_id:
                    result.append(link)

        return result

    def get_linkdistances_in_radius(self, pos, max_distance):
        """ Match wenn Link Bbox mit pos und radius überlappt können nicht erreicht werden. Liste wird nach tatsächer
        distance sortiert und nur die max_nbr geringen Abstände zurückgegeben.
        :param pos:
        :param max_distance:
        :return: Link Distance Objects
        """

        bbox = BoundingBox.get_bbox_from_point(pos, max_distance)
        links = self.get_links_in_bounding_box(bbox)
        # links = _get_links_in_circle(links, pos, max_distance)
        linkdists = []
        for link in links:
            linkdists.append(LinkDistance(pos, link))

        # Sortieren und Filter der LinkDistance-Objekte:
        linkdists.sort(key=lambda l: l.get_distance())
        linkdists = list(filter(lambda ld: ld.get_distance() <= max_distance, linkdists))

        return linkdists

    def get_node(self, nodeid: NodeId):
        """
        :param nodeid:
        :return: Node-Object
        """
        tile = self.get_tile(nodeid.get_geohash()[:self._geohash_level])
        return tile.get_node(nodeid)
