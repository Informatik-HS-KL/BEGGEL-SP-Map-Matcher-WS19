"""
Description: This file contains util methods for the REST-API.
WARNING: depreciated
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""


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

