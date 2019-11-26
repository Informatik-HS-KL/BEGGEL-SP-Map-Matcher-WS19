"""
Description: The GeohashWrapper encapsulates the functionality of the following geohash-library:
https://github.com/vinsci/geohash/
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

# """
# https://github.com/vinsci/geohash/
#
# """
import geohash2 as geohash
from src.models.bounding_box import BoundingBox


class GeoHashWrapper:
    base32 = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'b', 'c', 'd', 'e', 'f',
              'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

    def __init__(self):
        pass

    def get_geohash(self, pos: tuple, level):
        """Wrapper fpr Geohash Lib"""
        return geohash.encode(pos[0], pos[1], precision=level)

    def get_geohashes(self, bbox: BoundingBox, level: int):
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

        bbox_middle = ((bbox.south + bbox.north) / 2, (bbox.west + bbox.east) / 2)
        # Wir gehen ein geohash-Level höher:
        geohash_for_middle = self.get_geohash(bbox_middle, level - 1)
        # bounding_box_big = geohash_for_middle[:-1]
        # Wir bestimmen die BoundingBox, die der Kachel entspricht.
        big_bounding_box = BoundingBox.from_geohash(geohash_for_middle)

        # Wenn bbox nicht in big_bounding_box liegt, dann müsste man eigentlich noch ein geohash-Level höher gehen. Das
        # ist derzeit allerdings noch nicht implementiert.
        if bbox not in big_bounding_box:
            raise Exception("Die angegebene BoundingBox ist zu groß, da sie in keiner Kachel mit geohash_level = %s "
                            "enthalten ist." % (level - 1))

        list_of_geo_hashes = []
        for b in self.base32:
            new_geohash = geohash_for_middle + b
            if bbox.overlap(BoundingBox.from_geohash(new_geohash)):
                list_of_geo_hashes.append(new_geohash)

        return list_of_geo_hashes
