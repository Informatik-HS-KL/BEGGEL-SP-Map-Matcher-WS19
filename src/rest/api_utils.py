
def createGeoJson(geotype, coords, data=None):
    """
    Simple geojson creator
    geotype can be:
        LineString
        Point
    coords:
        Linestring: [[lat,lon], ...]
        Point: [lat,lon]
    :param geotype:
    :param coords:
    :return:
    """

    if not data:
        data = {}
    geojson = {
        "type": "Feature",
        "geometry": {
            "type": geotype,
            "coordinates": coords
        },
        "properties": data
    }
    return geojson

