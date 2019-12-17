"""
Description: This files offers some mathematical and geographic-related methods.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""
from math import radians, sin, cos, acos, sqrt, isclose


def great_circle(point1: tuple, point2: tuple):
    """
    Angaben in Meter
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

    return 6371 * (acos(result)) * 1000


def convert_meter_2_lat(meter):
    """
    Converts a range in meter into a range in latitude-degrees.
    :param meter:
    :return: lat-range in float
    """

    meter_per_lat = great_circle((0, 0), (1, 0))
    lat_per_meter = 1 / meter_per_lat
    return meter * lat_per_meter


def convert_meter_2_lon(meter, lat):
    """
    Converts a range in meter into a range in longitude-degrees.
    :param meter:
    :param lat:
    :return: lon-range in float
    """

    meter_per_lon = great_circle((lat, 0), (lat, 1))
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
