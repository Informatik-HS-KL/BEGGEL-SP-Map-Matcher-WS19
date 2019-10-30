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





class OverpassWrapperServerSide:
    OVERPASS_URL = CONFIG.get("DEFAULT", "overpass_url")
    full_geohash_level = CONFIG.getint("DEFAULT", "full_geohash_level")
    counter = 0

    def __init__(self, OVERPASS_URL, full_geohash_level, counter):
        self.OVERPASS_URL = OVERPASS_URL
        self.full_geohash_level
        self.counter = counter

    def load_tile(self, geo_hash):
        """ Daten von der Overpass api laden
            from geohash to Boundingbox
        """
        # ---------------------
        self.counter += 1
        print(self.counter, __name__, geo_hash)
        # ---------------------------
        ghw = GeoHashWrapper()

        q_filter = self._filterQuery(CONFIG)
        url = self._buildQuery(geo_hash, q_filter)
        print(url)
        resp = requests.get(url)
        try:
            elements = resp.json().get("elements")
        except Exception as e:
            print(resp.text)

        nodes = {}  # Initalize
        intersections = set()
        links = {}  # Initalize

        number_of_intersections = int(elements[0]["tags"]["nodes"])
        for k in range(1, number_of_intersections + 1):
            intersections.add(elements[k]["id"])

        for k in range(number_of_intersections + 1, len(elements)):
            element = elements[k]
            if element["type"] == "node":

                node = self.__create_node(element["id"], (element["lat"], element["lon"]), element.get("tags"))
                nodes[node.get_id()] = node

            elif element["type"] == "way":
                way_nodes_ids = element["nodes"]
                way_nodes_positions = element["geometry"]

                link_geometry = []
                link_node_ids = []

                for i in range(0, len(way_nodes_ids) - 1):  # Building the links that put together the way.

                    if (way_nodes_ids[i] in intersections and i != 0) or i == len(
                            way_nodes_ids) - 1:  # reached end of link

                        end_node_pos = (way_nodes_positions[i]["lat"], way_nodes_positions[i]["lon"])
                        end_node_id = NodeId(way_nodes_ids[i], ghw.get_geohash(end_node_pos,
                                                                               level=self.full_geohash_level))

                        link_geometry.append(end_node_pos)
                        link_node_ids.append(end_node_id)
                        link_id = LinkId(element["id"], link_node_ids[0])
                        link = Link(link_id, link_geometry, link_node_ids)
                        links.update({link_id: link})

                        #  Re-Initialization for the next link
                        link_geometry = [end_node_pos]
                        link_node_ids = [end_node_id]

                    else:
                        node_pos = (way_nodes_positions[i]["lat"], way_nodes_positions[i]["lon"])
                        node_id = NodeId(way_nodes_ids[i], ghw.get_geohash(node_pos,
                                                                           level=self.full_geohash_level))
                        link_geometry.append(node_pos)
                        link_node_ids.append(node_id)

        return Tile(geo_hash, nodes, links)

    def _buildQuery(self, geohash, q_filter: str):
        """Return Url to Download Tile"""

        bbox_str = "%s" % BoundingBox.from_geohash(geohash)
        query = '[out:json];way%s%s->.ways;node(w.ways)->.nodes;relation.nodes->.intersections;foreach.ways->.w((' \
                '.ways; - .w;)->.otherWays;node(w.w)->.currentWayNodes;node(' \
                'w.otherWays)->.otherWayNodes;node.currentWayNodes.otherWayNodes->.currentIntersections;(' \
                '.intersections; .currentIntersections;)->.intersections;);.intersections out count;.intersections ' \
                'out ids;.nodes out body; .ways out geom;' % (bbox_str, q_filter)
        url = "%s?data=%s" % (self.OVERPASS_URL, query)
        return url

    def _filterQuery(self, config, conf_section="HIGHWAY_CARS"):
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


class OverpassWrapperClientSide(OverpassWrapper):

    def __init__(self, full_geohash_level, OVERPASS_URL):
        """"""
        super(OverpassWrapperClientSide, self).__init__(full_geohash_level, OVERPASS_URL)
        self.ghw = GeoHashWrapper()
        self.counter = 0

    def load_tile(self, geo_hash):
        """ Daten von der Overpass api laden
            from geohash to Boundingbox
        """

        q_filter = self._filterQuery(CONFIG)
        elements = self._download(self.OVERPASS_URL, geo_hash, q_filter)

        return self._create_tile(geo_hash, elements)

    def _download(self, host_endpoint, geo_hash, q_filter):
        """
        Downloading data from Overpass-Server and parsing response to list.
        :return: list containing osm-elements
        """

        # ---------------------
        self.counter += 1
        print(self.counter, geo_hash)
        # ---------------------

        query_str = self._buildQuery(geo_hash, q_filter)
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

    def _buildQuery(self, geohash, q_filter: str):
        """Return Url to Download Tile"""

        bbox_str = "%s" % BoundingBox.from_geohash(geohash)
        query = '?data=[out:json];way%s%s->.ways;node(w.ways)->.nodes;.nodes out body; .ways out geom;' % (
            bbox_str, q_filter)
        return query

    def _filterQuery(self, config, conf_section="HIGHWAY_CARS"):
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
