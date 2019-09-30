

class LinkDistance:
    # (lat, lon) beschreibt den Punkt, in dessen Umkreis Links gesucht werden.
    # Dabei werden die Abstände von (lat, lon) zu den jeweiligen Links mittels
    # Ortogonalprojektion bestimmt.
    _lat
    _lon
    # Ortogonalprojektion von Punkt auf Link
    _latMatched
    # Ortogonalprojektion von Punkt auf Link
    _lonMatched

    # distance zw. punkt und ortogonalprojekton von Punkt auf Link
    distance

    # Fraction beschreibt die Position auf dem Link. (latMatched, lonMatched)
    # liegt ja nämlich vielleicht  irgendwo in der Mitte des Links, z.B. F=0.5
    # F=0: StartKnoten, F=1: EndKnoten, F=0.5 : mitte des Links,....
    fraction

   # Das dazugehörige Link-Objekt
    Link