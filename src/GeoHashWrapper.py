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

        bboxMiddle = ( (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2 )
        geoHashforMiddle = self.getGeoHash(bboxMiddle, level-1)
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

    def overlapse(self, bbox1, bbox2):
        """"""

        

    def isFirstBboxLargerThanSecondBbox(self, bbox1, bbox2):
        """"""

    def getBoundingBox(self, geoHash) :
         """implement with lib"""
