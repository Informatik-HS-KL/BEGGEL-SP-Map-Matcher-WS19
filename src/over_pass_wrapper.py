"""
Description: The OverpassWrapper is not only used to obtain OpenStreetMap-Data via the Overpass-API, but also to parse
the obtained data into the convenient model-objects.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

import collections
import time
from abc import ABC, abstractmethod
import requests
from .geo_hash_wrapper import GeoHashWrapper

from src.models.tile import Tile
from src.models.node import Node, NodeId
from src.models.link_id import LinkId
from src.models.link import Link
from src.models.bounding_box import BoundingBox

from . import CONFIG


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
        """
        Loads the required data, builds and returns the tile with the specified geohash.
        """
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
        """
        Create Tile of given Overpass Data
        :param geohash: geohash of tile
        :param elements: json data from nodes and ways as dict
        :return: Tile
        """
        ghw = GeoHashWrapper()
        intersections = set()

        number_of_intersections = int(elements[0]["tags"]["nodes"])
        for k in range(1, number_of_intersections + 1):
            intersections.add(elements[k]["id"])

        osm_nodes = list(filter(lambda e: e["type"] == "node", elements[number_of_intersections + 1:]))
        nodes = self._build_node_dictionary(osm_nodes)

        osm_ways = list(filter(lambda e: e["type"] == "way", elements[number_of_intersections + 1:]))
        links = self._build_link_dictionary(osm_ways, intersections, ghw)

        return Tile(geohash, nodes, links)

    def _build_node_dictionary(self, osm_nodes: list):
        """
        return dictionary with NodeId: Node
        :param osm_nodes: list of all Nodes in downloaded data
        :return: dict {Nodeid: Node}
        """
        node_list = list(map(lambda n: self.__create_node(n["id"], (n["lat"], n["lon"]), n.get("tags")), osm_nodes))

        return dict(map(lambda n: (n.get_id(), n), node_list))

    def _build_link_dictionary(self, osm_ways: list, intersections: set, geohash_wrapper):
        """
        returns dictionary with LinkId : Link
        :param osm_ways: Ways from osm data as dict
        :param intersections: set of intersections between ways
        :param geohash_wrapper:
        :return: dict with {LinkId: Link}
        """
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
                    link.set_tags(way.get("tags"))
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

    @staticmethod
    def _build_query(geohash, q_filter: str):
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
        """
        Creates Node Object from given Data
        :param osm_id:
        :param pos: tuple lat/lon
        :param tags: dict
        :return: Node
        """
        node_id = NodeId(osm_id, GeoHashWrapper().get_geohash(pos, level=self.full_geohash_level))
        node = Node(node_id, pos)
        node.set_tags(tags)
        return node


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

        links = self._build_link_dictionary(osm_ways, crossings_osm_ids, osm_id_nodes_dict)
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

    def _build_link_dictionary(self, osm_ways: list, crossings: list, nodes: dict):
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

                if node_id.osm_node_id in crossings or way_nodes_ids[-1] == node_id.osm_node_id and i != 0:  # Wenn Kreuzung oder Ende des
                    # Ways erreicht. Ausnahme: wir befinden uns noch am Anfang des Links (closed link)!!!
                    link_id = LinkId(way["id"], link_node_ids[0])
                    link = Link(link_id, link_geometry, link_node_ids)
                    link.set_tags(way.get("tags"))
                    links[link_id] = link

                    for nid in link_node_ids:
                        nodes[nid.osm_node_id].add_parent_link(link)

                    nodes[link_node_ids[0].osm_node_id].add_link(link)
                    nodes[link_node_ids[-1].osm_node_id].add_link(link)

                    #  Re-Initialization for the next link
                    link_geometry = [node_pos]
                    link_node_ids = [node_id]

        return links

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
