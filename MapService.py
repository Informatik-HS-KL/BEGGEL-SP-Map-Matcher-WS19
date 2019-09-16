

class MapService:

    # maps geohash --> Tile class
    tileCache = {}
    geoHashLevel = 5


    def getNodesInBoundingBox(_self, latLon1, latLon2):

            ret = []

            for geoHash  in geoHashWrapper.getGeoHashes(latLon1,latLon2,geoHashLevel):
                tile = getOrLoadTile (geoHash);
                for node in tile._nodes:
                    if GeoUtil.contains (node, latLon1,latLon2);
                        ret.append(node);
             return ret;


    def getOrLoadTile (_self, geoash):
        if geohash not in tileCache:
            tileCache[geohash] = OverPassWrapper.loadTile(geoHash)


        return tileCache[geohash];
