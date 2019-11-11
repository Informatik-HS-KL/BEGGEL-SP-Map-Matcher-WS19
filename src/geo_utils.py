"""
Description: This files offers some mathematical and geographic-related methods.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

# from src.models.tile import Tile
from math import radians, degrees, sin, cos, asin, acos, sqrt, isclose
from src.models.tile import Tile
from src.models.node import Node


def great_circle(point1: tuple, point2: tuple):
    """
    Angaben in KM
    :param point1:
    :param point2:
    :return:
    """
    lat1, lon1 = point1
    lat2, lon2 = point2

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    result = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)

    # Rundungsfehler beseiten
    if result > 1.0:
        result = 1

    if result < -1.0:
        result = -1

    return 6371 * (acos(result))


def convert_meter_2_lat(meter):
    """
    Convert meter to latitude difference
    :return: lat-difference in float
    """

    meter_per_lat = great_circle((0, 0), (1, 0)) * 1000
    lat_per_meter = 1 / meter_per_lat
    return meter * lat_per_meter


def convert_meter_2_lon(meter):
    """
    Convert meter to latitude difference
    :return: lat-difference in float
    """
    meter_per_lon = great_circle((0, 0), (0, 1)) * 1000
    lon_per_meter = 1 / meter_per_lon
    return meter * lon_per_meter


def number_is_in_interval(number, interval, overflow_mark, excluding_endpoints=False):
    """Diese Methode überprüft, ob eine Zahl innerhalb eines Zahlenintervals liegt. overflow_mark gibt an,
    ab welchem (positiven) Wert die Zahlen überlaufen, also wieder im negativen Bereich landen (bei Längengraden
    wäre overflow_mark = 180). Die Rückgabe erfolgt als boolean. exluding_endpoints gibt an, ob es sich um ein offenes
     oder ein geschlossenes interval handelt (excluding_endpoints=False --> geschlossenes interval)."""

    a, b = interval

    if excluding_endpoints:
        return (a < number < b and a <= b) or \
               ((a < number <= overflow_mark or -overflow_mark <= number < b) and b < a)

    return (a <= number <= b and a <= b) or (
            (a <= number <= overflow_mark or -overflow_mark <= number <= b) and b < a)


def overlap_intervals(interval_1, interval_2, overflow_mark):
    """Diese Methode überprüft, ob sich zwei Zahlenintervale überschneiden.
       overflow_mark gibt an, ab welchem (positiven) Wert die Zahlen überlaufen, also wieder im negativen Bereich landen
       (Bei Längengraden wäre overflow_mark = 180).
       Die Rückgabe erfolgt als boolean.
       Beachte: Überlappen sich lediglich die Ränder von interval_1 und interval_2, so wird False zurückgegeben."""

    if interval_1 == interval_2:
        return True

    a1, b1 = interval_1
    a2, b2 = interval_2

    return (number_is_in_interval(a1, interval_2, overflow_mark, excluding_endpoints=True) or
            number_is_in_interval(b1, interval_2, overflow_mark, excluding_endpoints=True) or
            number_is_in_interval(a2, interval_1, overflow_mark, excluding_endpoints=True) or
            number_is_in_interval(b2, interval_1, overflow_mark, excluding_endpoints=True))


def first_interval_contains_second_interval(first_interval: tuple, second_interval: tuple, overflow_mark: float):
    """Diese Methode überprüft, ob interval_2 eine Teilmenge von interval_1 ist.
    Die Rückgabe erfolgt als boolean. Beachte: interval_1 == interval_2 liefert ebenfalls True."""

    if first_interval == second_interval:
        return True

    a2, b2 = second_interval

    return number_is_in_interval(a2, first_interval, overflow_mark) and \
           number_is_in_interval(b2, first_interval, overflow_mark)


def dot_product(a: tuple, b: tuple):
    if not len(a) == len(b):
        raise Exception('The Vectors have not the same length')
    if len(a) == 0:
        raise Exception('The Vectors have no items')
    """Bildet das Skalarprodukt von zwei Vectoren"""
    return sum([x * y for x, y in zip(a, b)])


def vector_addition(a: tuple, b: tuple):
    if not len(a) == len(b):
        raise Exception('The Vectors have not the same length')
    if len(a) == 0:
        raise Exception('The Vectors have no items')
    """Addiert zwei Vectoren"""
    return tuple([x + y for x, y in zip(a, b)])


def scalar_multiplication(scalar, vec):
    if len(vec) == 0:
        raise Exception('The Vectors have no items')
    """Skalarmultiplikation"""
    return tuple([scalar * y for y in vec])


def orthogonal_projection(vec_from, vec_to):
    return scalar_multiplication(dot_product(vec_from, vec_to) / dot_product(vec_to, vec_to), vec_to)


def vector_subtraction(vector_a, vector_b):
    if not len(vector_a) == len(vector_b):
        raise Exception('The Vectors have not the same length')
    if len(vector_a) == 0:
        raise Exception('The Vectors have no items')
    return tuple([x - y for x, y in zip(vector_a, vector_b)])


def vector_norm(v: tuple):
    if len(v) == 0:
        raise Exception('The Vector has no items')

    return sqrt(dot_product(v, v))


def is_nullvector(v: tuple) -> bool:
    """Überprüft, ob v der Nullvektor ist.
    :return: bool"""
    for i in range(0, len(v)):
        if i != 0:
            return False

    return True


def vectors_are_parallel(a: tuple, b: tuple) -> bool:
    """Überprüft, ob zwei Vektoren (gleicher Dimension) parallel zueinander sind.
    :return: boolean"""
    if not len(a) == len(b):
        raise Exception('The Vectors have not the same length')
    if len(a) == 0:
        raise Exception('The Vectors have no items')

    if is_nullvector(a) or is_nullvector(b):  # Der Nullvektor ist zu jedem anderen Vektor parallel.
        return True

    factor = None

    for i in range(0, len(a)):
        if a[i] != 0 and b[i] != 0:
            factor = b[0] / a[0]

    if factor is None:
        return False

    for i in range(0, len(a)):
        # isclose überprüft hier, ob die ersten zehn Ziffern (nicht Nachkommastellen) übereinstimmen.
        if not isclose(b[i], a[i] * factor, rel_tol=1e-10):
            return False

    return True


def vectors_have_same_direction(a: tuple, b: tuple) -> bool:
    """Überprüft, ob zwei Vektoren (gleicher Dimension) in die gleiche Richtung zeigen.
    :return: boolean
    :raises: wirft Exception, wenn a und b unterschiedliche Dimensionen oder Dimension 0 haben."""

    if not len(a) == len(b):
        raise Exception('The Vectors have not the same length')
    if len(a) == 0:
        raise Exception('The Vectors have no items')

    if is_nullvector(a) or is_nullvector(b):
        return True

    # Diese Schleife überprüft, ob a und b in jeder Komponente das gleiche Vorzeichen haben.
    for i in range(0, len(a)):
        if b[i] != 0:
            if a[i] / b[i] < 0:
                return False

    return vectors_are_parallel(a, b)


# Dieser Codesnipsel veranschaulicht, dass sich die spherische Geometrie nicht immer so verhält, wie man es erwartet.
# sn = (49.4217069, 7.5606304)
# mpoint = (49.421703949999994, 7.56109395)
# pos = (49.42216749999999, 7.561096899999999)
# print(great_circle(sn, mpoint))
# print(great_circle(mpoint, pos))
#
# print(vector_norm(vector_subtraction(mpoint, sn)))
# print(vector_norm(vector_subtraction(pos, mpoint)))

def point_to_point_dijkstra(initial, initial_fraction, end, end_fraction, weight_prop="length"):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)

    initial = initial.get_start_node()
    end = end.get_end_node()

    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        print(current_node.get_id().geohash)
        visited.add(current_node)
        destinations = [link.get_end_node() for link in current_node.get_links()] + [link.get_start_node() for link in
                                                                                     current_node.get_links()]
        destinations = list(filter(lambda n: n != current_node, list(destinations)))
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            # node.get_parent_link().get(weight_prop) # "length" as weigh factor
            weight = 1 + weight_to_current_node  # graph.get[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}

        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
        print(current_node)
    # Reverse path
    path = path[::-1]

    return path


def link_to_link_dijkstra(initial, initial_fraction, end_link, end_fraction, weight_function):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous link, weight)

    shortest_paths = {initial: (None, 0)}
    current_link = initial
    visited = set()

    while current_link != end_link:
        print(current_link.get_link_id().geohash)
        visited.add(current_link)
        destinations = [link for link in current_link.get_links_at_start_node()] + \
                       [link for link in current_link.get_links_at_end_node()]
        destinations = list(filter(lambda n: n != current_link, list(destinations)))
        weight_to_current_node = shortest_paths[current_link][1]

        for next_link in destinations:
            weight = weight_function.get_wight(next_link, 1) + weight_to_current_node
            if next_link not in shortest_paths:
                shortest_paths[next_link] = (current_link, weight)
            else:
                current_shortest_weight = shortest_paths[next_link][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_link] = (current_link, weight)

        next_destinations = {link: shortest_paths[link] for link in shortest_paths if link not in visited}

        if not next_destinations:
            return "Route Not Possible"
        # next link is the destination with the lowest weight
        current_link = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_link is not None:
        path.append(current_link)
        next_link = shortest_paths[current_link][0]
        current_link = next_link
        print(current_link)
    # Reverse path
    path = path[::-1]

    return path

def test_dijkstra(initial, initial_fraction, end_link, end_fraction, weight_function, from_start_to_end):

    if from_start_to_end:
        initial.get_links_at_end_node()
    else:
        initial.get_links_at_start_node()