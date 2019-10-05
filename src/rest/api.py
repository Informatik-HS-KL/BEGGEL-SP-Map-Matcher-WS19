import requests
from flask import jsonify
from flask import Response, request, Blueprint
from src.map_service import MapService
from src.geo_hash_wrapper import GeoHashWrapper
from src.models.bounding_box import BoundingBox
from src.models.link import Link

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
    """
    :param data:
    :return:
    """

    #return Response(response=, status=200, mimetype="text/html")
    return jsonify(data)


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

    tiles = map_service.get_all_cached_tiles()
    data = {}
    for k, v in tiles.items():
        bbox = BoundingBox.from_geohash(k)
        data[k] = {
            "nodes.length": len(v.get_nodes()),
            "bbox": {
                "south": bbox.south,
                "west": bbox.west,
                "north": bbox.north,
                "east": bbox.east
            }
        }

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

    geohashes = GeoHashWrapper().get_geohashes(BoundingBox(south, west,north,east), 5)

    data = {}

    for geohash in geohashes:
        data[geohash] = {
            "south": BoundingBox.from_geohash(geohash).south,
            "west": BoundingBox.from_geohash(geohash).west,
            "north": BoundingBox.from_geohash(geohash).north,
            "east": BoundingBox.from_geohash(geohash).east,
        }
    return _resp(data)


@api.route('/tiles/<string:geohash>')
@api.route('/tiles/<string:geohash>/')
def get_tile(geohash):
    """ :return tile of given GeoHash
    """
    if len(geohash) < 3:
        return jsonify({"Error": "Level have to be >= 4"})

    tile = map_service.get_tile(geohash)
    data = {
        "geohash": tile.get_geohash(),
        "nodes.length": len(tile.get_nodes()),
        "links.length": len(tile.get_links()),
        "bbox": str(BoundingBox.from_geohash(geohash))
    }

    return _resp(data)


@api.route('/tiles/<string:geohash>/nodes')
def get_nodes(geohash):
    """ :return Nodes of tile of Geohash
    """
    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    tile = map_service.get_tile(geohash)
    data = []
    for node in tile.get_nodes():
        point = {
            "type": "Point",
            "coordinates": list(node.get_latlon()),
            "osmid": str(node.get_id())
        }
        data.append(point)

    return _resp(data)


@api.route('/tiles/<string:geohash>/nodes/<int:osmid>')
def get_node(geohash, osmid):
    """ :return Nodes of tile of Geohash
    """
    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    tile = map_service.get_tile(geohash)
    node = tile.get_node(osmid)
    if not node:
        return _resp({"error": "No Node with osm id:" + str(osmid)})
    point = {
        "type": "Point",
        "coordinates": list(node.get_latlon()),
        "osmid": osmid
    }
    return _resp(point)


@api.route('/tiles/<string:geohash>/links')
def get_links(geohash):
    """ :return Links of Tile of given hash
    """

    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    tile = map_service.get_tile(geohash)

    data = []
    for linkid, link in tile.get_links().items():
        linestr = {
            "type": "LineString",
            "coordinates": [list(link.get_start_node().get_latlon()), list(link.get_end_node().get_latlon())],
            "way_id": linkid.osm_way_id
        }
        data.append(linestr)

    return _resp(data)


@api.route('/tiles/<string:geohash>/crossroads')
def get_crossroads(geohash):
    """
    Nodes wich represents a Crossing
    :param geohash:
    :return: json
    """
    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    tile = map_service.get_tile(geohash)
    data = []
    for node in tile.get_nodes():
        if len(node.get_links()) > 2:
            point = {
                "type": "Point",
                "coordinates": list(node.get_latlon())
            }
            data.append(point)

    return _resp(data)


@api.route('/ways/<string:way_id>/links', methods=["GET"])
def get_way_links(way_id):
    """Links eines Ways"""

    data = []
    for link in map_service.get_links(way_id):
        linestr = {
            "type": "LineString",
            "coordinates": [list(link.get_start_node().get_latlon()), list(link.get_end_node().get_latlon())]
        }
        data.append(linestr)

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
