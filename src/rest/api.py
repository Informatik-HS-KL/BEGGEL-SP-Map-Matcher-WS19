"""
Description: This file defines the endpoints of the REST-API.
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""
import time

from flask import jsonify
from flask import request, Blueprint
from src.map_service import MapService
from src.geo_hash_wrapper import GeoHashWrapper
from src.models.bounding_box import BoundingBox
from src.models.node import NodeId
from src.utils.router import RouterBaseDijkstra, RouterLinkDijkstra, RouterDijkstra
from src.models.link_user import Car

from .mapservice_wrapper import MapserviceWrapper

map_service = MapService()
api = Blueprint('api', __name__)


def documentation():

    data = [
        { "url": "/api/tiles/","description":"Get all cached tiles infos"},
        {"url":"/api/tiles/<geohash>/", "description": "get tile infos of given geohash"},
        { "url":"/api/tiles/<geohash>/nodes", "description":"get nodes of given tile"},
        { "url":"/api/tiles/<geohash>/nodes/1", "description":"get specific node of tile"},
        { "url": "/api/tiles/<geohash>/crossroads", "description":"get crossroads of tile"},
        { "url": "/api/geohashes?bbox=south,west,north,east", "description": "Liste aller geohashes, die von dieser bbox betroffen sind"}
    ]
    return data

def _resp(data):
    """ Response Wrapper
    :param data:
    :return:
    """

    #return Response(response=, status=200, mimetype="text/html")
    jdata = None
    try:
        jdata = jsonify(data)
        return jdata

    except Exception as e:
        print(data)

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
    data = msw.get_dict_geohashes()
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


@api.route('/tiles/<string:geohash>/nodes/crossroads')
def get_crossroads(geohash):
    """
    Nodes wich represents a Crossing
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
    """ ?geofrom=geohash&geoto=geohash&osmfrom=osmid&osmto=osmid

    u0v90hsp01h2 OSM:1298232519

    u0v90jk7p21y OSM:266528360

    ?geofrom=u0v90hsp01h2&geoto=u0v90jk7p21y&osmfrom=1298232519&osmto=266528360
    """

    full_geohash_from = request.args.get("geofrom")
    full_geohash_to = request.args.get("geoto")

    osmid_from = request.args.get("osmfrom")
    osmid_to = request.args.get("osmto")

    node_id_from = NodeId(int(osmid_from), full_geohash_from)
    node_id_to = NodeId(int(osmid_to), full_geohash_to)

    node_from = map_service.get_node(node_id_from)
    node_to = map_service.get_node(node_id_to)

    data = []
    result_nodes = []

    # router = RouterBaseDijkstra(Car())  # Mit Laden: ~11 ohne 1,21
    # router = RouterLinkDijkstra(Car())  # Mit Laden: ~12 ohne 3,31
    router = RouterDijkstra(Car())  # Mit Laden: ~13 ohne 0.85
    start_time = time.time()
    router.set_start_link(node_from.get_parent_links()[0])
    router.set_end_link(node_to.get_parent_links()[0])
    result_nodes = router.compute()
    print("Zeit: ", time.time() - start_time)
    print("Loaded Tiles:",map_service.get_all_cached_tiles())
    for node in result_nodes:

        data.append(node.to_geojson())

    return _resp(data)


@api.route('/ways/<int:way_id>/links', methods=["GET"])
def get_way_links(way_id):
    """Links eines Ways"""

    msw = MapserviceWrapper(map_service)
    data = msw.get_dict_way_links()
    return _resp(data)

@api.route('/linkdistance', methods=["GET"])
def get__linkdistance():
    """Calculate Link Distances Canidates"""

    from src.models.link_distance import LinkDistance

    pos = float(request.args.get("lat")), float(request.args.get("lon"))

    msw = MapserviceWrapper(map_service)
    data = msw.get_dict_linkdistances(pos, radius=100)
    return _resp(data)


@api.route('/samples', methods=["GET"])
def samples():
    data = {
        "Homburg":{
            "bbox": "49.293105512,7.2850287149,49.3553136219,7.3705160806",
            "tiles": ["u0v0t", "u0v0y", "u0v0r"],
        },
        "Köln":{
            "bbox": "50.9099067349,6.9170473881,50.9700490766,7.0025347539",
            "tiles": ["u1hcv", "u1hcw", "u1hcz"]
        },
    }
    return jsonify(data)


