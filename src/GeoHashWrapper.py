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

        if self.isFirstBboxLargerThanSecondBbox():
            raise Exception("Willst du die ganze welt runterladen oder was?")

        base32 = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'b', 'c', 'd', 'e', 'f',
                  'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

        listOfGeoHashes = []
        for b in base32:
            newGeoHash = geoHashforMiddle + b
            if self.overlaps(decode2Box(newGeoHash), bbox):
                listOfGeoHashes.append(newGeoHash)

        return listOfGeoHashes

    @staticmethod
    def overlap(bbox1, bbox2):
        """"""
        lat_intervall_1 = (bbox1[0], bbox1[2])
        lat_intervall_2 = (bbox2[0], bbox2[2])

        if not GeoHashWrapper.overlap_intervalls(lat_intervall_1, lat_intervall_2, 90): # Hier wird wird nie ein overflow passieren
            return False

        lon_intervall_1 = (bbox1[1], bbox1[3])
        lon_intervall_2 = (bbox2[1], bbox2[3])

        if not GeoHashWrapper.overlap_intervalls(lon_intervall_1, lon_intervall_2, 180):
            return False

        return True

    @staticmethod
    def overlap_intervalls(intervall_1, intervall_2, overflow_mark):
        """Diese Methode überprüft, ob sich zwei Zahlenintervalle überschneiden.
           overflow_mark gibt an, ab welchem (positiven) Wert die Zahlen überlaufen, also wieder im negativen Bereich landen
           (Bei Längengraden wäre overflow_mark = 180)"""

        a1, b1 = intervall_1
        a2, b2 = intervall_2

        if GeoHashWrapper.number_is_in_intervall(a1, intervall_2, overflow_mark):
            return True
        if GeoHashWrapper.number_is_in_intervall(b1, intervall_2, overflow_mark):
            return True

        if GeoHashWrapper.number_is_in_intervall(a2, intervall_1, overflow_mark):
            return True
        if GeoHashWrapper.number_is_in_intervall(b2, intervall_1, overflow_mark):
            return True

        return False

    @staticmethod
    def number_is_in_intervall(number, intervall, overflow_mark):
        """Diese Methode überprüft, ob eine Zahl innerhalb eines Zahlenintervalls liegt.
            overflow_mark gibt an, ab welchem (positiven) Wert die Zahlen überlaufen, also wieder im negativen Bereich landen
            (Bei Längengraden wäre overflow_mark = 180)"""

        a, b = intervall
        if (a < number < b and a < b) or ((a < number <= overflow_mark or -overflow_mark < number < b) and b < a):
            return True

        return False

    def isFirstBboxLargerThanSecondBbox(self, bbox1, bbox2):
        """"""

    def getBoundingBox(self, geoHash):
        """implement with lib"""


# bbox1 = (31.27, -110.19, 37.64, -102.1)
# bbox2 = (-5.8, 46.3, 6.3, 60.9)
# print(GeoHashWrapper.overlapse(bbox1, bbox2))
