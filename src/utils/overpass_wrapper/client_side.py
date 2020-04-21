import collections
import time

from src.models import Tile, BoundingBox
from .overpass_wrapper import OverpassWrapper


class OverpassWrapperClientSide(OverpassWrapper):
    """
    Subclass of OverpassWrapper which determines the intersections of ways on the client-side.
    """

    def __init__(self, config):
        """"""
        super(OverpassWrapperClientSide, self).__init__(config)

    def _get_intersections(self, osm_ways):
        """
        Searches for Intersections of OSM-Ways and returns the osm-ids of the corresponding nodes.
        :param osm_ways: raw osm way data parsed from json
        :return: list(int)
        """

        all_nodes = []
        for way in osm_ways:
            all_nodes.extend(way["nodes"])

        crossing_osm_ids = list(map(lambda x: x[0], filter(lambda i: i[1] > 1, collections.Counter(all_nodes).items())))
        return crossing_osm_ids

    def _build_query(self, geohash, q_filter: str):
        """
        Returns the URL to download the data, which is required to build the tile with the specified geohash.
        :param geohash: str
        :param q_filter: str
        """

        bbox_str = "%s" % BoundingBox.from_geohash(geohash)
        query = '?data=[out:json];way%s%s->.ways;node(w.ways)->.nodes;.nodes out body; .ways out;' % (
            bbox_str, q_filter)

        # adding this will also download the POIs in the region
        # TODO: make it configuration to download pois
        query += 'node%s["amenity"];out;' % (bbox_str)

        return query

    def _create_tile(self, geo_hash, elements: dict):
        """
        :param geo_hash: str
        :param elements: raw dict data from overpass json api
        :return: Tile-Object
        """

        t0 = time.time()

        osm_nodes = list(filter(lambda e: e["type"] == "node", elements))

        osm_ways = list(filter(lambda e: e["type"] == "way", elements))
        osm_id_nodes_dict = dict(
            map(lambda n: self._create_node(n["id"], (n["lat"], n["lon"]), n.get("tags")), osm_nodes))

        crossings_osm_ids = self._get_intersections(osm_ways)

        links = self._build_link_dictionary(geo_hash, osm_ways, crossings_osm_ids, osm_id_nodes_dict)
        # nodes = dict(map(lambda n: (n.get_id(), n), filter(lambda x: x.get_geohash()[:len(geo_hash)] == geo_hash,
        #                                                    osm_id_nodes_dict.values())))
        nodes = dict(map(lambda n: (n.get_id(), n), osm_id_nodes_dict.values()))
        t = Tile(geo_hash, nodes, links)

        t1 = time.time()

        return t
