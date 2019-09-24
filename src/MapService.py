"""
"""

from src import GeoHashWrapper
from src.OverPassWrapper import OverPassWrapper
from src.models.BoundingBox import BoundingBox


class MapService:
    """"""
    # maps geohash --> Tile class
    tileCache = {}
    geoHashLevel = 5

    def getNodesInBoundingBox(self, bbox: BoundingBox):
        """
        Knoten einer Boudingbox zurückgeben.
        Knoten werden aus den Tiles geladen
        :param bbox:
        :return:
        """
        ret = []
        geoHashLevel = None

        for geoHash in GeoHashWrapper().getGeoHashes(bbox, geoHashLevel):
            tile = self.getOrLoadTile(geoHash)
            for node in tile._nodes:
                if node in bbox:
                    ret.append(node)

        return ret

    def getOrLoadTile(self, geohash):
        """"""
        if geohash not in self.tileCache:
            self.tileCache[geohash] = OverPassWrapper().loadTile(geohash)

        return self.tileCache[geohash]

    def getAllCachedTiles(self):
        return self.tileCache
