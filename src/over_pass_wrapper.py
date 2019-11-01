"""
Description: The OverpassWrapper is not only used to obtain OpenStreetMap-Data via the Overpass-API, but also to parse
the obtained data into the convenient model-objects.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

# """
# Läd daten von der OVerpass schnittstelle in eine Kachel
# """
import collections
from abc import ABC, abstractmethod
import requests
from .geo_hash_wrapper import GeoHashWrapper

from src.models.tile import Tile
from src.models.node import Node, NodeId
from src.models.link_id import LinkId
from src.models.link import Link
from src.models.bounding_box import BoundingBox

from . import CONFIG


# Todo: Testen !!!

class OverpassWrapper(ABC):
    """
    ABSTRACT BASE CLASS
    """

    def __init__(self, full_geohash_level, OVERPASS_URL):
        # self.full_geohash_level = CONFIG.getint("DEFAULT", "full_geohash_level")
        # self.OVERPASS_URL = CONFIG.get("DEFAULT", "overpass_url")
        self.full_geohash_level = full_geohash_level
        self.OVERPASS_URL = OVERPASS_URL

    @abstractmethod
    def load_tile(self, geo_hash):
        pass


class OverpassWrapperServerSide(OverpassWrapper):
    """
    Subclass of OverpassWrapper which determines the intersections of ways on the server-side.
    """

    def __init__(self, full_geohash_level, OVERPASS_URL):
        super(OverpassWrapperServerSide, self).__init__(full_geohash_level, OVERPASS_URL)
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

    def _create_tile(self, geohash, elements):
        ghw = GeoHashWrapper()
        intersections = set()  # Initialize

        number_of_intersections = int(elements[0]["tags"]["nodes"])
        for k in range(1, number_of_intersections + 1):
            intersections.add(elements[k]["id"])

        osm_nodes = list(filter(lambda e: e["type"] == "node", elements[number_of_intersections + 1:]))
        nodes = self._build_node_dictionary(osm_nodes)

        osm_ways = list(filter(lambda e: e["type"] == "way", elements[number_of_intersections + 1:]))
        links = self._build_link_dictionary(osm_ways, intersections, ghw)

        return Tile(geohash, nodes, links)

    def _build_node_dictionary(self, osm_nodes: list):
        node_list = list(map(lambda n: self.__create_node(n["id"], (n["lat"], n["lon"]), n.get("tags")), osm_nodes))

        return dict(map(lambda n: (n.get_id(), n), node_list))

    def _build_link_dictionary(self, osm_ways: list, intersections: set, geohash_wrapper):
        links = {}

        print("length of osm_ways: {}".format(len(osm_ways)))
        for way in osm_ways:
            way_nodes_ids = way["nodes"]
            way_nodes_positions = way["geometry"]

            link_geometry = []
            link_node_ids = []

            for i in range(0, len(way_nodes_ids)):  # Building the links that put together the way.

                if (way_nodes_ids[i] in intersections and i != 0) or i == len(
                        way_nodes_ids) - 1:  # reached end of link

                    end_node_pos = (way_nodes_positions[i]["lat"], way_nodes_positions[i]["lon"])
                    end_node_id = NodeId(way_nodes_ids[i], geohash_wrapper.get_geohash(end_node_pos,
                                                                                       level=self.full_geohash_level))

                    link_geometry.append(end_node_pos)
                    link_node_ids.append(end_node_id)
                    link_id = LinkId(way["id"], link_node_ids[0])
                    link = Link(link_id, link_geometry, link_node_ids)
                    links.update({link_id: link})

                    #  Re-Initialization for the next link
                    link_geometry = [end_node_pos]
                    link_node_ids = [end_node_id]

                else:
                    node_pos = (way_nodes_positions[i]["lat"], way_nodes_positions[i]["lon"])
                    node_id = NodeId(way_nodes_ids[i], geohash_wrapper.get_geohash(node_pos,
                                                                                   level=self.full_geohash_level))
                    link_geometry.append(node_pos)
                    link_node_ids.append(node_id)

        return links

    def _download(self, host_endpoint, geo_hash, q_filter):
        """
        Downloading data from the Overpass-Server and parsing the response to a list.
        :return: list, which contains osm-elements
        """

        # ---------------------
        self.counter += 1
        print(self.counter, geo_hash)
        # ---------------------

        query_str = self._build_query(geo_hash, q_filter)
        url = host_endpoint + query_str
        print(url)

        resp = requests.get(url)
        try:
            elements = resp.json().get("elements")
            return elements

        except Exception as e:
            raise Exception("Download Tile Failed %s" % resp.text)

    def _build_query(self, geohash, q_filter: str):
        """
        Returns the URL to download the data, which is required to build the tile with the specified geohash.
        The intersections of ways are determined on server-side.
        """

        bbox_str = "%s" % BoundingBox.from_geohash(geohash)
        query = '?data=[out:json];way%s%s->.ways;node(w.ways)->.nodes;relation.nodes->.intersections;foreach.ways->.w((' \
                '.ways; - .w;)->.otherWays;node(w.w)->.currentWayNodes;node(' \
                'w.otherWays)->.otherWayNodes;node.currentWayNodes.otherWayNodes->.currentIntersections;(' \
                '.intersections; .currentIntersections;)->.intersections;);.intersections out count;.intersections ' \
                'out ids;.nodes out body; .ways out geom;' % (bbox_str, q_filter)

        return query

    def _filter_query(self, config, conf_section="HIGHWAY_CARS"):
        """
        Erstellt Query aus gegebenen Highways aus der Config
        conf_section: Section in der config.ini die zur Erstellung der Query herangezogen werden soll
        """

        query = "(if: "
        options = config.options(conf_section, no_defaults=True)
        for option in options:
            if config.getboolean(conf_section, option):
                query += 't["highway"] == "%s" ||' % option

        return query[:-2] + ")"

    def __create_node(self, osm_id, pos: tuple, tags=None):
        node_id = NodeId(osm_id, GeoHashWrapper().get_geohash(pos, level=self.full_geohash_level))
        node = Node(node_id, pos)
        node.set_tags(tags)
        return node


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------


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
        :return: list, which ontains osm-elements
        """

        # ---------------------
        self.counter += 1
        print(self.counter, geo_hash)
        # ---------------------

        query_str = self._build_query(geo_hash, q_filter)
        url = host_endpoint + query_str
        print(url)

        resp = requests.get(url)
        try:
            elements = resp.json().get("elements")
            return elements

        except Exception as e:
            raise Exception("Download Tile Failed %s" % resp.text)

    def _crossings(self, nodes_osm, ways_osm):

        nodes_dict = dict(map(lambda node: (node["id"], node), nodes_osm))

        all = []
        for way in ways_osm:
            all.extend(way["nodes"])

        crossing_ids = filter(lambda i: i[1] > 1, collections.Counter(all).items())

        node_ids = []
        for cid in crossing_ids:
            n = nodes_dict[cid[0]]
            node_id = NodeId(cid[0], self.ghw.get_geohash((n["lat"], n["lon"]), level=self.full_geohash_level))
            node_ids.append(node_id)

        return node_ids

    def _create_tile(self, geo_hash, elements: dict):
        """
        Erstellt eine Kachel.
        :return: Tile
        """

        print("Build Datamodel ...")

        links = {}
        nodes_osm = list(filter(lambda e: e["type"] == "node", elements))
        ways_osm = list(filter(lambda e: e["type"] == "way", elements))

        node_list = list(map(lambda n: self.__create_node(n["id"], (n["lat"], n["lon"]), n.get("tags")), nodes_osm))

        nodeids = {}  # {nodeids: [linked_node_ids]}

        crossings = self._crossings(nodes_osm, ways_osm)

        print(len(crossings))

        for way in ways_osm:
            way_nodes_ids = way["nodes"]
            way_nodes_positions = way["geometry"]

            link_geometry = []
            link_node_ids = []

            for i in range(len(way_nodes_ids)):
                node_pos = (way_nodes_positions[i]["lat"], way_nodes_positions[i]["lon"])
                node_id = NodeId(way_nodes_ids[i], self.ghw.get_geohash(node_pos, level=self.full_geohash_level))

                link_geometry.append(node_pos)
                link_node_ids.append(node_id)

                if node_id in crossings:
                    link_id = LinkId(way["id"], link_node_ids[0])
                    link = Link(link_id, link_geometry, link_node_ids)
                    links[link_id] = link

                    #  Re-Initialization for the next link
                    link_geometry = [node_pos]
                    link_node_ids = [node_id]

        nodes = dict(map(lambda n: (n.get_id(), n), node_list))

        t = Tile(geo_hash, nodes, links)
        t.set_crossings(crossings)
        return t

    def _build_query(self, geohash, q_filter: str):
        """
        Returns the URL to download the data, which is required to build the tile with the specified geohash.
        The intersections of ways are NOT determined on server-side.
        """

        bbox_str = "%s" % BoundingBox.from_geohash(geohash)
        query = '?data=[out:json];way%s%s->.ways;node(w.ways)->.nodes;.nodes out body; .ways out geom;' % (
            bbox_str, q_filter)
        return query

    def _filter_query(self, config, conf_section="HIGHWAY_CARS"):
        """Erstellt Query aus gegebenen Highways aus der Config
           conf_section: Section in der config.ini die zur Erstellung der Query herangezogen werden soll
        """

        query = "(if: "
        options = config.options(conf_section, no_defaults=True)
        for option in options:
            if config.getboolean(conf_section, option):
                query += 't["highway"] == "%s" ||' % option

        return query[:-2] + ")"

    def __create_node(self, osm_id, pos: tuple, tags=None):
        node_id = NodeId(osm_id, GeoHashWrapper().get_geohash(pos, level=self.full_geohash_level))
        node = Node(node_id, pos)
        node.set_tags(tags)
        return node
