"""
https://github.com/vinsci/geohash/

"""
import geohash2 as Geohash
from src.models.BoundingBox import BoundingBox


class GeoHashWrapper:

    base32 = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'b', 'c', 'd', 'e', 'f',
              'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

    def __init__(self):
        pass

    def getGeoHash(self, pos: tuple, level):
        """Wrapper fpr Geohash Lib"""
        return Geohash.encode(pos[0], pos[1], precision=level)

    def getGeoHashes(self, bbox: BoundingBox, level: int):
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

        bboxMiddle = ((bbox.south + bbox.north) / 2, (bbox.west + bbox.east) / 2)
        geoHashforMiddle = self.getGeoHash(bboxMiddle, level - 1)
        boundingBoxBig = geoHashforMiddle[:-1]

#        if self.isFirstBboxLargerThanSecondBbox():
#            raise Exception("Willst du die ganze welt runterladen oder was?")

        listOfGeoHashes = []
        for b in self.base32:
            newGeoHash = geoHashforMiddle + b
            if bbox.overlap(BoundingBox.from_geohash(newGeoHash)):
                listOfGeoHashes.append(newGeoHash)

        return listOfGeoHashes


    def isFirstBboxLargerThanSecondBbox(self, bbox1, bbox2):
        """"""

    def getBoundingBox(self, geohash):
        """implement with lib"""
