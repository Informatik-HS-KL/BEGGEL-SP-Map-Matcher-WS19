import requests
from flask import jsonify
from flask import Response, request, Blueprint
from src.MapService import MapService
from src.GeoHashWrapper import GeoHashWrapper
from src.models.BoundingBox import BoundingBox

mapservice = MapService()
api = Blueprint('api', __name__)

def _resp(data):
    """
    :param data:
    :return:
    """
    return jsonify(data)


@api.route('tiles')
@api.route('tiles/')
def get_tiles():
    """ :return List of Geohashes of the cached Tiles
    """

    tiles = mapservice.getAllCachedTiles()
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

    geohashes = GeoHashWrapper().getGeoHashes(tuple(bbox), 5)
    return _resp(geohashes)

@api.route('/tiles/<string:geohash>')
def get_tile(geohash):
    """ :return tile of given GeoHash
    """
    if len(geohash) < 3:
        return jsonify({"Error": "Level have to be >= 4"})

    tile = mapservice.getOrLoadTile(geohash)
    data = []

    for node in tile.get_nodes():
        point = {
            "type": "Point",
            "coordinates": list(node.get_latlon())
        }
        data.append(point)

    return _resp(data)

@api.route('/tiles/<string:geohash>/nodes')
def get_nodes(geohash):
    """ :return Nodes of tile of Geohash
    """
    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    tile = mapservice.getOrLoadTile(geohash)
    data = []
    for node in tile.get_nodes():
        point = {
            "type": "Point",
            "coordinates": list(node.get_latlon())
        }
        data.append(point)

    return _resp(data)

@api.route('/tiles/<string:geohash>/links')
def get_links(geohash):
    """ :return Links of Tile of given hash
    """

    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    tile = mapservice.getOrLoadTile(geohash)

    data = []
    for link in tile.get_links():
        linestr = {
            "type": "LineString",
            "coordinates": [list(link.get_start_node().get_latlon()), list(link.get_end_node().get_latlon())]
        }
        data.append(linestr)

    return _resp(data)

@api.route('/tiles/<string:geohash>/nodes/crossroads')
def get_crossroads(geohash):
    """
    Nodes wich represents a Crossing
    :param geohash:
    :return: json
    """
    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    tile = mapservice.getOrLoadTile(geohash)
    data = []
    for node in tile.get_nodes():
        if len(node.get_links()) > 2:
            point = {
                "type": "Point",
                "coordinates": list(node.get_latlon())
            }
            data.append(point)

    return _resp(data)


@api.route('/tiles/sum', methods=["GET"])
def sum_tiles():
    """ Fasst mehrere Tiles in get zusammen
        ?hashes=1,2,3
    """
    # TODO HIER KÖNNTE UNS DER HAUPSPEICHER VOLL LAUFEN

    hashes_s = request.args.get("hashed", "")
    hashes_list = hashes_s.split(",")
    nodes = {}
    for hash in hashes_list:
        tile = mapservice.getOrLoadTile(hash)
        nodes.update(tile.get_nodes())

    return _resp(nodes)