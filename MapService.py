"""
"""

import GeoUtil
import GeoHashWrapper

class MapService:
    """"""
    # maps geohash --> Tile class
    tileCache = {}
    geoHashLevel = 5

    def getNodesInBoundingBox(self, latLon1, latLon2):
        """"""
        ret = []
        geoHashLevel = None

        for geoHash in GeoHashWrapper.getGeoHashes(latLon1, latLon2, geoHashLevel):
            tile = getOrLoadTile (geoHash)
            for node in tile._nodes:
                if GeoUtil.contains (node, latLon1, latLon2)
                    ret.append(node)
         return ret


    def getOrLoadTile(self, geoash):
        """"""
        if geohash not in tileCache:
            tileCache[geohash] = OverPassWrapper.loadTile(geoHash)

        return tileCache[geohash]

