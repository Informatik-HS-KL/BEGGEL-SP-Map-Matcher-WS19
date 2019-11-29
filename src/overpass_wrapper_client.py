import collections
import time
import requests
from .geo_hash_wrapper import GeoHashWrapper

from src.models.tile import Tile
from src.models.node import Node, NodeId
from src.models.link_id import LinkId
from src.models.link import Link
from src.models.bounding_box import BoundingBox
from src.overpass_wrapper import OverpassWrapper

from . import CONFIG


class OverpassWrapperClientSide(OverpassWrapper):
    """
        Subclass of OverpassWrapper which determines the intersections of ways on the client-side.
    """

    def __init__(self, full_geohash_level, OVERPASS_URL):
        """"""
        super(OverpassWrapperClientSide, self).__init__(full_geohash_level, OVERPASS_URL)
        self.ghw = GeoHashWrapper()
        self.counter = 0

    def load_tile(self, geo_hash):
        """
        Loads the required data from the Overpass-Server, builds and returns the tile with the specified
        geohash.
        """

        q_filter = self._filter_query(CONFIG)
        elements = self._download(self.OVERPASS_URL, geo_hash, q_filter)

        return self._create_tile(geo_hash, elements)

    def _download(self, host_endpoint, geo_hash, q_filter):
        """
        Downloading data from the Overpass-Server and parsing the response to a list.
        :return: list, which contains osm-elements
        """

        self.counter += 1
        print(self.counter, geo_hash)

        query_str = self._build_query(geo_hash, q_filter)
        url = host_endpoint + query_str
        print(url)

        resp = requests.get(url)
        try:
            elements = resp.json().get("elements")
            return elements

        except Exception as e:
            raise Exception("Download Tile Failed %s" % resp.text)

    def _create_tile(self, geo_hash, elements: dict):
        """
        :param geo_hash: geohash as str
        :param elements: raw dict data from overpass json api
        :return: Tile Object
        """

        print("Build Datamodel ...")
        t0 = time.time()

        osm_nodes = list(filter(lambda e: e["type"] == "node", elements))
        osm_ways = list(filter(lambda e: e["type"] == "way", elements))
        osm_id_nodes_dict = dict(
            map(lambda n: self.__create_node(n["id"], (n["lat"], n["lon"]), n.get("tags")), osm_nodes))

        crossings_osm_ids = self._crossings(osm_ways)

        links = self._build_link_dictionary(geo_hash, osm_ways, crossings_osm_ids, osm_id_nodes_dict)
        # nodes = dict(map(lambda n: (n.get_id(), n), filter(lambda x: x.get_geohash()[:len(geo_hash)] == geo_hash,
        #                                                    osm_id_nodes_dict.values())))
        nodes = dict(map(lambda n: (n.get_id(), n), osm_id_nodes_dict.values()))
        t = Tile(geo_hash, nodes, links)

        t1 = time.time()
        print("Zeit in s:", t1 - t0, "Links:", len(links), "Nodes:", len(nodes), "Crossingids:", len(crossings_osm_ids))
        return t

    def _crossings(self, osm_ways):
        """
        Search for Crossings in osm Ways and returns them as Nodes
        :param osm_nodes: raw osm nodes data parsed from json
        :param osm_ways: raw osm way data parsed from json
        :return: List of NodeId
        """

        all = []
        for way in osm_ways:
            all.extend(way["nodes"])

        crossing_osm_ids = dict(filter(lambda i: i[1] > 1, collections.Counter(all).items()))
        return crossing_osm_ids

    def _build_link_dictionary(self, geohash: str, osm_ways: list, crossings: list, nodes: dict):
        """
        :param osm_ways: raw way data from overpass as dict
        :param crossings: List of Nodeids represent crossings in street
        :param nodes: List of Node Objects
        :return: dict {LinkId: Link}
        """
        links = {}

        for way in osm_ways:
            way_nodes_ids = way["nodes"]

            link_geometry = []
            link_node_ids = []

            for i in range(len(way_nodes_ids)):

                node_id = nodes[way_nodes_ids[i]].get_id()
                node_pos = nodes[way_nodes_ids[i]].get_latlon()

                link_geometry.append(node_pos)
                link_node_ids.append(node_id)

                is_end = way_nodes_ids[-1] == way_nodes_ids[i]
                is_start = way_nodes_ids[0] == way_nodes_ids[i]
                is_crossing = way_nodes_ids[i] in crossings

                link = None

                if is_end or (not is_start and is_crossing):

                    link = self._init_link(link_geometry, link_node_ids, way, nodes)

                elif self._is_entering_tile(nodes[way_nodes_ids[i]].get_id(),
                                            nodes[way_nodes_ids[i+1]].get_id(), geohash):

                    link_geometry = [nodes[way_nodes_ids[i]].get_latlon(), nodes[way_nodes_ids[i+1]].get_latlon()]
                    link_node_ids = [nodes[way_nodes_ids[i]].get_id(), nodes[way_nodes_ids[i+1]].get_id()]
                    link = self._init_link(link_geometry, link_node_ids, way, nodes)

                elif self._is_leaving_tile(nodes[way_nodes_ids[i]].get_id(),
                                           nodes[way_nodes_ids[i+1]].get_id(), geohash):

                    link = self._init_link(link_geometry, link_node_ids, way, nodes)
                    links[link.get_id()] = link

                    link_geometry = [nodes[way_nodes_ids[i]].get_latlon(), nodes[way_nodes_ids[i+1]].get_latlon()]
                    link_node_ids = [nodes[way_nodes_ids[i]].get_id(), nodes[way_nodes_ids[i+1]].get_id()]
                    link = self._init_link(link_geometry, link_node_ids, way, nodes)

                if link is not None:
                    links[link.get_id()] = link
                    # Re-Initialization for the next link
                    link_geometry = [node_pos]
                    link_node_ids = [node_id]
        return links

    def _init_link(self, link_geometry, link_node_ids, way, nodes):
        link_id = LinkId(way["id"], link_node_ids[0])
        link = Link(link_id, link_geometry, link_node_ids)
        link.set_tags(way.get("tags"))
        for nid in link_node_ids:
            nodes[nid.osm_node_id].add_parent_link(link)
        if nodes.get(link_node_ids[0].osm_node_id):
            nodes[link_node_ids[0].osm_node_id].add_link(link)
        if nodes.get(link_node_ids[-1].osm_node_id):
            nodes[link_node_ids[-1].osm_node_id].add_link(link)
        return link

    def _is_entering_tile(self, node_id, next_node_id, geohash):
        akt_hash = node_id.geohash[:len(geohash)]
        next_hash = next_node_id.geohash[:len(geohash)]
        return akt_hash != geohash and next_hash == geohash

    def _is_leaving_tile(self, node_id, next_node_id, geohash):
        akt_hash = node_id.geohash[:len(geohash)]
        next_hash = next_node_id.geohash[:len(geohash)]
        return akt_hash == geohash and next_hash != geohash

    @staticmethod
    def _build_query(geohash, q_filter: str):
        """
        Returns the URL to download the data, which is required to build the tile with the specified geohash.
        The intersections of ways are NOT determined on server-side.
        """

        bbox_str = "%s" % BoundingBox.from_geohash(geohash)
        query = '?data=[out:json];way%s%s->.ways;node(w.ways)->.nodes;.nodes out body; .ways out;' % (
            bbox_str, q_filter)
        return query

    @staticmethod
    def _filter_query(config, conf_section="HIGHWAY_CARS"):
        """
        Builds the query-filter depending on the specified config-section.
        """

        query = "(if: "
        options = config.options(conf_section, no_defaults=True)
        for option in options:
            if config.getboolean(conf_section, option):
                query += 't["highway"] == "%s" ||' % option

        return query[:-2] + ")"

    def __create_node(self, osm_id, pos: tuple, tags=None):
        node_id = NodeId(osm_id, self.ghw.get_geohash(pos, level=self.full_geohash_level))
        node = Node(node_id, pos)
        node.set_tags(tags)
        return osm_id, node
