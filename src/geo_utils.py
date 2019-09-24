from src.models.Tile import Tile

def printPretty(tile : Tile):
    """"""

    for n in tile.get_nodes():
        print("-"*20)
        print("Node:", n.get_id())
        print("Links", [(l.get_start_node(), l.get_end_node()) for l in n.get_links()])


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


def firstIntervalContainsSecondInterval(first_interval: tuple, second_interval: tuple, overflow_mark: float):
    """Diese Methode überprüft, ob interval_2 eine Teilmenge von interval_1 ist.
    Die Rückgabe erfolgt als boolean. Beachte: interval_1 == interval_2 liefert ebenfalls True."""

    if first_interval == second_interval:
        return True

    a2, b2 = second_interval

    return number_is_in_interval(a2, first_interval, overflow_mark) and \
        number_is_in_interval(b2, first_interval, overflow_mark)