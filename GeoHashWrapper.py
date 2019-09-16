"""
https://github.com/vinsci/geohash/

"""

class GeoHashWrapper:

    def getGeoHash(self, latLon, level):
        """"""
        pass

    def getGeoHashes(self, latLon1, latlLon2, level  ):

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

        pass

     def getBoundingBox(self, geoHash) :
         """implement with lib"""
