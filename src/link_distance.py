from math import sqrt
from src.models.node import Node, NodeId
from math import acos, sin, cos, radians


class LinkDistance:

    def __init__(self, pos: tuple):
        # (lat, lon) beschreibt den Punkt, in dessen Umkreis Links gesucht werden.
        # Dabei werden die Abstände von (lat, lon) zu den jeweiligen Links mittels
        # Ortogonalprojektion bestimmt.
        self._lat = pos[0]
        self._lon = pos[1]
        # Ortogonalprojektion von Punkt auf Link
        self._latMatched = None
        # Ortogonalprojektion von Punkt auf Link
        self._lonMatched = None

        # distance zw. punkt und ortogonalprojekton von Punkt auf Link
        self.distance = None

        # Fraction beschreibt die Position auf dem Link. (latMatched, lonMatched)
        # liegt ja nämlich vielleicht  irgendwo in der Mitte des Links, z.B. F=0.5
        # F=0: StartKnoten, F=1: EndKnoten, F=0.5 : mitte des Links,....
        self.fraction = None

        # Das dazugehörige Link-Objekt
        self.Link = None


def distance_node_link(node, link):
    link_point = __get_nearest_point_on_link_to_point(link, node.get_latlon())
    return distance_between_nodes(link_point, node)


def distance_between_nodes(node_a: Node, node_b: Node):
    # TODO aus Internet Kopierter Code kenntlich machen ??
    #  von: https://blog.petehouston.com/calculate-distance-of-two-locations-on-earth/

    lon1, lat1, lon2, lat2 = map(radians, [node_a.get_lon(), node_a.get_lat(), node_b.get_lon(), node_b.get_lat()])
    return  6371 * (
        acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
    )


def __get_nearest_point_on_link_to_point(link, node: Node):
    """ Methode berücksichtigt nicht dass die Erde Rund ist
    :param link gerade auf die der zu berechende Punkt liegen muss
    :param node
    :return Node Pseudo Node only lat, lon """
    start_node = link.get_start_node()
    end_node = link.get_end_node()
    if (start_node.get_lon() <= node.get_lon() <= end_node.get_lon() or
            end_node.get_lon() <= node.get_lon() <= start_node.get_lon()):
        # Berechne Lotfußpunkt
        d = end_node.get_lat() * node.get_lat() + end_node.get_lon() * node.get_lon()
        s = (-1) * (
                (d + end_node.get_lon()*start_node.get_lon() + end_node.get_lat()*start_node.get_lat())
                /
                (pow(end_node.get_lon(), 2) + pow(start_node.get_lon(), 2))
             )
        lat = start_node.get_lat() + s * end_node.get_lat()
        lon = start_node.get_lon() + s * end_node.get_lon()

        return Node(NodeId("", ""), (lat, lon))  # Pseudo Node only lat, lon

    if abs(start_node.get_lon() - node.get_lon()) < abs(start_node.get_lon() - node.get_lon()):
        return start_node
    else:
        return end_node

# def ortogonalproj(link, point: tuple):
#    ax = link.get_start_node().get_lat()
#    ay = link.get_start_node().get_lon()
#
#    gy2 = link.get_end_node().get_lat() - link.get_start_node().get_lat()
#    gx2 = link.get_end_node().get_lon()
#
#    px = point[0]
#    py = point[1]
#
#    d_zaeler = (px - ay) * gy2 - gx2 * (py - ax)
#    d_nenner = sqrt(gx2 * gx2 + gy2 * gy2)
#
#    return d_zaeler / d_nenner
