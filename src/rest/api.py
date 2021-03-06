"""
Description: This file defines the endpoints of the REST-API.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

from flask import jsonify
from flask import request, Blueprint
from src.map_service import MapService
from src.models import BoundingBox
from .mapservice_wrapper import MapserviceWrapper

map_service = MapService()
api = Blueprint('api', __name__)


def documentation():

    data = [
        {"url": "/api/tiles/", "description": "Get all cached tiles infos"},
        {"url": "/api/tiles/<geohash>/", "description": "get tile infos of given geohash"},
        {"url": "/api/tiles/<geohash>/nodes", "description": "get nodes of given tile"},
        {"url": "/api/tiles/<geohash>/nodes/1", "description": "get specific node of tile"},
        {"url": "/api/tiles/<geohash>/intersections", "description": "get intersections of tile"},
        {"url": "/api/geohashes?bbox=south,west,north,east", "description": "Liste aller geohashes, die von dieser bbox betroffen sind"}
    ]
    return data


def _resp(data):
    """ Response Wrapper
    :param data:
    :return:
    """

    # return Response(response=, status=200, mimetype="text/html")
    jdata = None
    try:
        jdata = jsonify(data)
        return jdata

    except:
        pass

    return jdata


@api.route('/')
def get_doc():
    """ :return
    """
    return _resp(documentation())


@api.route('tiles')
@api.route('tiles/')
def get_tiles():
    """ :return List of Geohashes of the cached Tiles
    """

    msw = MapserviceWrapper(map_service)
    data = msw.get_dict_tiles()
    return _resp({"description": "All Cached Tiles", "tiles": data})


@api.route('tiles/stats')
def get_tiles_stats():
    """ :return Statisiken zu allen tiles im cache
    """

    msw = MapserviceWrapper(map_service)
    data = msw.get_dict_stats()
    return _resp({"description": "All Cached Tiles", "tiles": data})


@api.route('/geohashes', methods=["GET"])
def get_geohashes():
    """ :return tile of given GeoHash
    """
    bbox_str = request.args.get("bbox")

    bbox = []
    for val in bbox_str.split(","):
        bbox.append(float(val))

    south, west, north, east = tuple(bbox)
    bbox = BoundingBox(south, west, north, east)

    msw = MapserviceWrapper(map_service)
    data = msw.get_dict_geohashes(bbox)
    return _resp(data)


@api.route('/tiles/<string:geohash>')
@api.route('/tiles/<string:geohash>/')
def get_tile(geohash):
    """ :return tile of given GeoHash
    """
    if len(geohash) < 3:
        return jsonify({"Error": "Level have to be >= 4"})

    msw = MapserviceWrapper(map_service)
    data = msw.get_dict_tile(geohash)
    return _resp(data)


@api.route('/tiles/<string:geohash>/nodes')
def get_nodes(geohash):
    """ :return Nodes of tile of Geohash
    """
    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    msw = MapserviceWrapper(map_service)
    data = msw.get_dict_nodes(geohash)
    return _resp(data)


@api.route('/tiles/<string:geohash>/nodes/<int:osmid>')
def get_node(geohash, osmid):
    """ :return Nodes of tile of Geohash
    """
    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    msw = MapserviceWrapper(map_service)
    data = msw.get_dict_node(geohash, osmid)

    return _resp(data)


@api.route('/tiles/<string:geohash>/links')
def get_links(geohash):
    """ :return Links of Tile of given hash
    """

    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    msw = MapserviceWrapper(map_service)
    return _resp(msw.get_dict_links(geohash))


@api.route('/tiles/<string:geohash>/nodes/intersections')
def get_intersections(geohash):
    """
    Nodes wich represents a intersections
    :param geohash:
    :return: json
    """
    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    msw = MapserviceWrapper(map_service)
    data = msw.get_dict_intersections(geohash)
    return _resp(data)


@api.route('/route')
def route():
    """ ?geofrom=geohash&geoto=geohash&start_lat=[Number]&start_lon=[Number]&end_lat=[Number]&end_lon=[Number]

    u0v90hsp01h2 OSM:1298232519

    u0v90jk7p21y OSM:266528360

    ?geofrom=u0v90hsp01h2&geoto=u0v90jk7p21y&osmfrom=1298232519&osmto=266528360
    """

    start_pos = float(request.args.get("start_lat")), float(request.args.get("start_lon"))
    end_pos = float(request.args.get("end_lat")), float(request.args.get("end_lon"))

    msw = MapserviceWrapper(map_service)
    data = msw.get_list_route(start_pos, end_pos)
    return _resp(data)


@api.route('/ways/<int:way_id>/links', methods=["GET"])
def get_way_links(way_id):
    """Links eines Ways"""

    msw = MapserviceWrapper(map_service)
    data = msw.get_dict_way_links(way_id)
    return _resp(data)


@api.route('/linkdistance', methods=["GET"])
def get_link_distance():
    """Calculate Link Distances Canidates"""

    try:
        pos = float(request.args.get("lat")), float(request.args.get("lon"))
        radius = int(request.args.get("radius"))

        msw = MapserviceWrapper(map_service)
        data = msw.get_dict_linkdistances(pos, radius=radius)
        return _resp(data)
    except ValueError:
        return _resp({"exception": "No position selected!"})


@api.route('/samples', methods=["GET"])
def samples():
    data = {
        "Homburg": {
            "bbox": "49.293105512,7.2850287149,49.3553136219,7.3705160806",
            "tiles": ["u0v0t", "u0v0y", "u0v0r"],
        },
        "Köln": {
            "bbox": "50.9099067349,6.9170473881,50.9700490766,7.0025347539",
            "tiles": ["u1hcv", "u1hcw", "u1hcz"]
        },
    }
    return jsonify(data)


