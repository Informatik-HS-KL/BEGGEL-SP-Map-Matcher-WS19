"""
"""

from src import GeoUtil, GeoHashWrapper
from src.OverPassWrapper import OverPassWrapper

class MapService:
    """"""
    # maps geohash --> Tile class
    tileCache = {}
    geoHashLevel = 5

    def getNodesInBoundingBox(self, latLon1, latLon2):
        """
        Knoten einer Boudingbox zurückgeben.
        Knoten werden aus den Tiles geladen
        :param latLon1:
        :param latLon2:
        :return:
        """
        ret = []
        geoHashLevel = None

        for geoHash in GeoHashWrapper.getGeoHashes(latLon1, latLon2, geoHashLevel):
            tile = self.getOrLoadTile (geoHash)
            for node in tile._nodes:
                if GeoUtil.contains (node, latLon1, latLon2):
                    ret.append(node)

        return ret


    def getOrLoadTile(self, geohash):
        """"""
        if geohash not in self.tileCache:
            self.tileCache[geohash] = OverPassWrapper().loadTile(geohash)

        return self.tileCache[geohash]



    def getAllCachedTiles(self):
        return self.tileCache