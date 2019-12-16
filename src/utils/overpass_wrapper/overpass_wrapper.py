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
from src.geo_hash_wrapper import GeoHashWrapper
from src.models.tile import Tile
from src.models.node import Node, NodeId
from src.models.link_id import LinkId
from src.models.link import Link
from src.models.bounding_box import BoundingBox


class OverpassWrapper(ABC):
    """
    ABSTRACT BASE CLASS
    """

    def __init__(self, config):
        self.ghw = GeoHashWrapper()
        self.full_geohash_level = config.getint("DEFAULT", "full_geohash_level")
        self.OVERPASS_URL = config.get("DEFAULT", "overpass_url")
        self.config = config

    def load_tile(self, geo_hash):
        """
        Loads the required data from the Overpass-Server, builds and returns the tile with the specified
        geohash.
        """

        q_filter = self._filter_query(self.config)
        elements = self._download(self.OVERPASS_URL, geo_hash, q_filter)

        return self._create_tile(geo_hash, elements)

    def _download(self, host_endpoint, geo_hash, q_filter):
        """
        Downloading data from the Overpass-Server and parsing the response to a list.
        :return: list, which contains osm-elements
        """

        query_str = self._build_query(geo_hash, q_filter)
        url = host_endpoint + query_str
        print(geo_hash)
        print(url)

        resp = requests.get(url)
        try:
            elements = resp.json().get("elements")
            return elements

        except Exception as e:
            raise Exception("Download Tile Failed %s" % resp.text)

    @abstractmethod
    def _create_tile(self, geo_hash, elements: dict):
        """
        :param geo_hash: geohash as str
        :param elements: raw dict data from overpass json api
        :return: Tile Object
        """
        pass

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

                    if len(link_node_ids) < 2:
                        continue

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

    @abstractmethod
    def _build_query(self, geohash, q_filter: str):
        """
        Returns the URL to download the data, which is required to build the tile with the specified geohash.
        """
        pass

    def _filter_query(self, config, conf_section="HIGHWAY_CARS"):
        """
        Builds the query-filter depending on the specified config-section.
        """

        query = "(if: "
        options = config.options(conf_section, no_defaults=True)
        for option in options:
            if config.getboolean(conf_section, option):
                query += 't["highway"] == "%s" ||' % option

        return query[:-2] + ")"

    def _create_node(self, osm_id, pos: tuple, tags=None):
        node_id = NodeId(osm_id, self.ghw.get_geohash(pos, level=self.full_geohash_level))
        node = Node(node_id, pos)
        node.set_tags(tags)
        return osm_id, node
