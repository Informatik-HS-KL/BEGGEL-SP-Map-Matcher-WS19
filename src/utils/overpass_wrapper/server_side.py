import time
from src.models import Tile, BoundingBox
from .overpass_wrapper import OverpassWrapper


class OverpassWrapperServerSide(OverpassWrapper):
    """
    Subclass of OverpassWrapper which determines the intersections of osm-ways on the server-side.
    """

    def __init__(self, config):
        super(OverpassWrapperServerSide, self).__init__(config)

    def _get_intersections(self, number_of_intersections, elements):
        """
        Returns the osm-ids of the nodes which are intersections of OSM-Ways.
        :param number_of_intersections: int
        :param elements: dict
        :return: list(int)
        """
        intersections = list()

        for k in range(1, number_of_intersections + 1):
            intersections.append(elements[k]["id"])

        return intersections

    def _create_tile(self, geo_hash, elements: dict):
        """
        :param geo_hash: str
        :param elements: raw dict data from overpass json api
        :return: Tile-Object
        """

        print("Build Datamodel ...")
        t0 = time.time()

        number_of_intersections = int(elements[0]["tags"]["nodes"])
        intersections = self._get_intersections(number_of_intersections, elements)

        osm_nodes = list(filter(lambda e: e["type"] == "node", elements[number_of_intersections + 1:]))

        osm_ways = list(filter(lambda e: e["type"] == "way", elements[number_of_intersections + 1:]))
        osm_id_nodes_dict = dict(
            map(lambda n: self._create_node(n["id"], (n["lat"], n["lon"]), n.get("tags")), osm_nodes))

        links = self._build_link_dictionary(geo_hash, osm_ways, intersections, osm_id_nodes_dict)
        # nodes = dict(map(lambda n: (n.get_id(), n), filter(lambda x: x.get_geohash()[:len(geo_hash)] == geo_hash,
        #                                                    osm_id_nodes_dict.values())))
        nodes = dict(map(lambda n: (n.get_id(), n), osm_id_nodes_dict.values()))
        t = Tile(geo_hash, nodes, links)

        t1 = time.time()
        print("Zeit in s:", t1 - t0, "Links:", len(links), "Nodes:", len(nodes), "Crossingids:", len(intersections))
        return t

    def _build_query(self, geohash, q_filter: str):
        """
        Returns the URL to download the data, which is required to build the tile with the specified geohash.
        The intersections of ways are determined on server-side.
        :param geohash: str
        :param q_filter: str
        """

        bbox_str = "%s" % BoundingBox.from_geohash(geohash)
        query = '?data=[out:json];way%s%s->.ways;node(w.ways)->.nodes;relation.nodes->.intersections;foreach.ways->.w((' \
                '.ways; - .w;)->.otherWays;node(w.w)->.currentWayNodes;node(' \
                'w.otherWays)->.otherWayNodes;node.currentWayNodes.otherWayNodes->.currentIntersections;(' \
                '.intersections; .currentIntersections;)->.intersections;);.intersections out count;.intersections ' \
                'out ids;.nodes out body; .ways out geom;' % (bbox_str, q_filter)

        return query
