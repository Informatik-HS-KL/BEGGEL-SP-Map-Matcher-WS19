"""
Description: A Link is a part of a street which if at all has only intersections at the beginning and/or the end. A Link might
have a non-linear geometry. The geometry of a link is a LINESTRING.
For WKT see: (https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""




# """
# Part of street where there is no intersection and that has a fixed set of properties.
# A link might have a non-linear geometry. Geometry of a link is a LINESTRING!
# for WKT see:
# https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
#
# """

from .node import NodeId
from .link_id import LinkId
import src.map_service
from src.geo_utils import great_circle
from enum import Enum

class LinkUser(Enum):
    PEDESTRIAN = 1
    CYCLIST = 2
    CAR = 3


class Link:
    # Links sollen nur noch Referenzen auf die Knoten (also die nodeIds) enthalten.
    # In get_start_node bzw. get_end_node wird dann über mapService der entsprechende Knoten geladen.

    def __init__(self, link_id, geometry: list, node_ids: list):
        """
        :param startNode: Node Start of this Link
        :param endNode: Node End of this Link
        """
        self.__start_node_id = node_ids[0]
        self.__end_node_id = node_ids[len(node_ids)-1]
        self.__outs = []
        self.__link_id = link_id
        self.__geometry = geometry  # contains the (lat, lon)-tupel of all nodes of the link
        self.__node_ids = node_ids
        self.__tags = None

        self._map_service = src.map_service.MapService()

    def get_bbox(self):
        """
        Todo: lässt sich mit shapely einfach lösen (wenn wir shapely verwenden!!!!)
        :return:
        """
       # BoundingBox.get_bbox_from_points(self.__start_node_id)

    def get_start_node(self):
        """
        :return Gibt den Startknoten (als Node) zurück.
        """

        # return self.__startNode

        return self._map_service.get_node(self.__start_node_id)

    def get_end_node(self):
        """ :return Gibt den Endknoten (als Node) zurück.
        """
        return self._map_service.get_node(self.__end_node_id)

    # def get_links(self):
    #     return self.__startNode.get_links().extend(self.__endNode.get_links())

    def get_links_at_start_node(self):
        """
        Gibt alle vom Startknoten ausgehende Links zurück (exclusive self).
        :return: Liste von Link-Objekten
        """
        nodelinks = self.get_start_node().get_links()
        links = filter(lambda l: l!=self, nodelinks)
        return list(links)

    def get_links_at_end_node(self):
        """
        Gibt alle vom Endknoten ausgehende Links zurück (exclusive self).
        :return: Liste von Link-Objekten
        """

        nodelinks = self.get_end_node().get_links()
        links = filter(lambda l: l != self, nodelinks)
        return list(links)

    def get_tags(self):
        """
        Attributes of this Link
        :return: dict
        """
        # TODO
        return self.__tags

    def set_tags(self, tags: dict):
        self.__tags = tags

    def get_link_id(self):
        return self.__link_id

    def get_way_osm_id(self):
        return self.__link_id.osm_way_id

    def __repr__(self):
        return "Link: <link_id: %s> <geometry: %s> <node_ids: %s>" % (self.__link_id, self.__geometry, self.__node_ids)

    def __str__(self):
        return "Link: <start_node_id: %s> <end_node_id: %s>" % (self.__start_node_id, self.__end_node_id)

    def to_geojson(self):
        """
        Todo: Wenn wir shapely verwenden, dann geht das hier komfortabler!!!
        returns link as geojson feature
        """

        line_string_coordinates = []
        for p in self.__geometry:
            line_string_coordinates.append([p[0], p[1]])

        data = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": line_string_coordinates
            },
            "properties": {
                "osm_way_id": self.get_way_osm_id(),
                "start_node": {
                    "geohash": self.get_link_id().get_start_node_id().geohash,
                    "id": self.get_link_id().get_start_node_id().osm_node_id
                }
            }
        }
        return data

    def to_wkt(self):
        """
        Todo: An neue Linkstruktur anpassen (verwenden wir hier shapely oder nicht?)!!!
        return WKT String from self
        :return:
        """
        return "LINESTRING (%s %s, %s %s)" % (self.get_start_node().get_lat(), self.get_start_node().get_lon(), \
                                                     self.get_end_node().get_lat(), self.get_end_node().get_lon())

    def get_length(self):
        """
        Todo: An neue Linkstruktur anpassen (verwenden wir hier shapely oder nicht?)!!!
        """
        return great_circle(self.get_start_node().get_latlon(), self.get_end_node().get_latlon())

    def is_from_start(self):
        pass

    def is_to_start(self):
        pass

    def is_usable_by(self) -> list:
        """
        Returns a list, which contains all kinds of permitted users for this link
        :return: list, which contains LinkUser-Objects or is empty
        """
        permitted_link_users = list()
        if self.is_usable_by_pedestrians():
            permitted_link_users.append(LinkUser.PEDESTRIAN)
        if self.is_usable_by_cyclists():
            permitted_link_users.append(LinkUser.CYCLISTI)
        if self.is_usable_by_cars():
            permitted_link_users.append(LinkUser.CAR)

    def is_usable_by_pedestrians(self) -> bool:
        """
        Checks whether pedestrians are permitted to use the link.
        """
        if "highway" in self.__tags:
            if self.__tags.get("highway") == "residential":
                if self.__tags.get("foot") is not None and self.__tags.get("foot") != "no":
                    return True

            elif self.__tags["highway"] == "living_street":
                if self.__tags.get("foot") is not None and self.__tags.get("foot") != "no":
                    return True

            elif self.__tags["highway"] == "pedestrian":
                return True

            elif self.__tags["highway"] == "footway":
                return True

            elif self.__tags["highway"] == "bridleway":
                if self.__tags.get("foot") is not None and self.__tags.get("foot") != "no":
                    return True

            elif self.__tags["highway"] == "path":
                if self.__tags.get("foot") is not None and self.__tags.get("foot") != "no":
                    return True

            elif self.__tags["highway"] == "steps":
                return True

        sidewalk_val = self.__tags.get("sidewalk")
        if sidewalk_val == "both" or sidewalk_val == "left" or sidewalk_val == "right":
            if self.__tags.get("foot") is not None and self.__tags.get("foot") != "no":
                return True

        foot_val = self.__tags.get("foot")
        if foot_val == "yes" or foot_val == "designated" or foot_val == "permissive":
            return True

        return False

    def is_usable_by_cyclists(self) -> bool:
        """
        Checks whether cyclists are permitted to use the link.
        """
        highway_val = self.__tags.get("highway")
        bicycle_val = self.__tags.get("bicycle")

        if bicycle_val == "no":
            return False

        if highway_val is not None:

            if highway_val == "residential" or highway_val == "cycleway" or highway_val == "bridleway" or highway_val == "path":
                return True

            elif highway_val == "steps":
                if self.__tags.get("ramp:bicycle") == "yes":
                    return True

        if bicycle_val is not None:
            if bicycle_val == "yes" or bicycle_val == "designated" or bicycle_val == "use_sidepath" or bicycle_val == "permissive" or bicycle_val == "destination":
                return True

        if self.__tags.get("cycleway") is not None and self.__tags.get("cycleway") != "no":
            return True

        if self.__tags.get("bicycle_road") == "yes":
            return True

        if self.__tags.get("cyclestreet") == "yes":
            return True

        return False

    def is_usable_by_cars(self) -> bool:
        """Todo"""
        pass



    # beggel-changes
    # def isNavFromStart(self, vehicleType):
    #     """
    #     Kann der Link vom Startknoten zum Endknoten befahren werden.
    #
    #     :param _self:
    #     :return:
    #     """
    #     return 0
    #
    # def isNavToStart(self):
    #     """
    #     Kann der Link vom Endknoten zum StartKnoten befahren werden.
    #
    #     :param _self:
    #     :return:
    #     """
    #     return 0
