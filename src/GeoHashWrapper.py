"""
https://github.com/vinsci/geohash/

"""
import geohash2 as Geohash
from src.utils import decode2Box


class GeoHashWrapper:

    def getGeoHash(self, pos: tuple, level):
        """Wrapper fpr Geohash Lib"""
        return Geohash.encode(pos[0], pos[1], precision=level)

    def getGeoHashes(self, bbox, level):
        """
        latLonMiddle = mitte der boundiung box
        geoHashforMiddle  = getGeoHash(latLonMiddle, level -1 );
        boundingBoxBig = getBoundingBox(geoHashforMiddle)

        if (boundingBoxBig larger than latLon1, latlLon2):
             raise "not Implemented yet";

        base32 = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'b', 'c', 'd', 'e', 'f',
                   'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};

        for b in base32:
            newGeash = geoHashforMiddle + b;
            if newgeohash overlaps with  latLon1, latlLon2:
                listOfGeoHashes.append (newgeohash);

        return listOfGeoHashes;
        """

        bboxMiddle = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
        geoHashforMiddle = self.getGeoHash(bboxMiddle, level - 1)
        boundingBoxBig = geoHashforMiddle[:-1]

#        if self.isFirstBboxLargerThanSecondBbox():
#            raise Exception("Willst du die ganze welt runterladen oder was?")

        base32 = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'b', 'c', 'd', 'e', 'f',
                  'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

        listOfGeoHashes = []
        for b in base32:
            newGeoHash = geoHashforMiddle + b
            if self.overlap(decode2Box(newGeoHash), bbox):
                listOfGeoHashes.append(newGeoHash)

        return listOfGeoHashes

    @staticmethod
    def overlap(bounding_box1, bounding_box2):
        """Diese Methode überprüft, ob sich zwei Bounding-Boxen überlappen.
           Rückgabe erfolgt als boolean.
           Beachte: Wenn die beiden Bounding-Boxen sich lediglich an ihren Rändern berühren, so zählt dies NICHT als Überlappung"""
        if bounding_box1 == bounding_box2:
            return True

        lat_interval_1 = (bounding_box1[0], bounding_box1[2])
        lat_interval_2 = (bounding_box2[0], bounding_box2[2])

        if not GeoHashWrapper.overlap_intervalls(lat_interval_1, lat_interval_2,
                                                 90):  # Hier wird wird nie ein overflow passieren
            return False

        lon_interval_1 = (bounding_box1[1], bounding_box1[3])
        lon_interval_2 = (bounding_box2[1], bounding_box2[3])

        if not GeoHashWrapper.overlap_intervalls(lon_interval_1, lon_interval_2, 180):
            return False

        return True

    @staticmethod
    def overlap_intervalls(interval_1, interval_2, overflow_mark):
        """Diese Methode überprüft, ob sich zwei Zahlenintervalle überschneiden.
           overflow_mark gibt an, ab welchem (positiven) Wert die Zahlen überlaufen, also wieder im negativen Bereich landen
           (Bei Längengraden wäre overflow_mark = 180).
           Die Rückgabe erfolgt als boolean.
           Beachte: Überlappen sich lediglich die Ränder von intervall_1 und intervall_2, so wird False zurückgegeben."""

        if interval_1 == interval_2:
            return True

        a1, b1 = interval_1
        a2, b2 = interval_2

        if GeoHashWrapper.number_is_in_intervall(a1, interval_2, overflow_mark, excluding_endpoints=True):
            return True
        if GeoHashWrapper.number_is_in_intervall(b1, interval_2, overflow_mark, excluding_endpoints=True):
            return True

        if GeoHashWrapper.number_is_in_intervall(a2, interval_1, overflow_mark, excluding_endpoints=True):
            return True
        if GeoHashWrapper.number_is_in_intervall(b2, interval_1, overflow_mark, excluding_endpoints=True):
            return True

        return False

    @staticmethod
    def number_is_in_intervall(number, interval, overflow_mark, excluding_endpoints=False):
        """Diese Methode überprüft, ob eine Zahl innerhalb eines Zahlenintervalls liegt. overflow_mark gibt an,
        ab welchem (positiven) Wert die Zahlen überlaufen, also wieder im negativen Bereich landen (bei Längengraden
        wäre overflow_mark = 180). Die Rückgabe erfolgt als boolean. exluding_endpoints gibt an, ob es sich um ein offenes
         oder ein geschlossenes Intervall handelt (excluding_endpoints=False --> geschlossenes Intervall)."""

        a, b = interval

        if excluding_endpoints:
            if (a < number < b and a <= b) or ((a < number <= overflow_mark or -overflow_mark <= number < b) and b < a):
                return True
            return False
        else:
            if (a <= number <= b and a <= b) or (
                    (a <= number <= overflow_mark or -overflow_mark <= number <= b) and b < a):
                return True
            return False

    def isFirstBboxLargerThanSecondBbox(self, bbox1, bbox2):
        """"""

    def getBoundingBox(self, geohash):
        """implement with lib"""

    @staticmethod
    def firstBboxContainsSecondBbox(bbox_1, bbox_2):
        """Diese Methode überprüft, ob bbox_2 eine Teilmenge von bbox_1 ist.
        Die Rückgabe erfolgt als boolean. Beachte: bbox_1 == bbox_2 liefert ebenfalls True."""

        if bbox_1 == bbox_2:
            return True

        lat_intervall_1 = (bbox_1[0], bbox_1[2])
        lat_intervall_2 = (bbox_2[0], bbox_2[2])

        if not GeoHashWrapper.firstIntervallContainsSecondIntervall(lat_intervall_1, lat_intervall_2, 90):
            return False

        lon_intervall_1 = (bbox_1[1], bbox_1[3])
        lon_intervall_2 = (bbox_2[1], bbox_2[3])

        if not GeoHashWrapper.firstIntervallContainsSecondIntervall(lon_intervall_1, lon_intervall_2, 180):
            return False

        return True

    @staticmethod
    def firstIntervallContainsSecondIntervall(interval_1, interval_2, overflow_mark):
        """Diese Methode überprüft, ob intervall_2 eine Teilmenge von intervall_1 ist.
        Die Rückgabe erfolgt als boolean. Beachte: intervall_1 == intervall_2 liefert ebenfalls True."""

        if interval_1 == interval_2:
            return True

        a2, b2 = interval_2
        if not (GeoHashWrapper.number_is_in_intervall(a2, interval_1,
                                                      overflow_mark) and GeoHashWrapper.number_is_in_intervall(b2,
                                                                                                               interval_1,
                                                                                                               overflow_mark)):
            return False

        return True
