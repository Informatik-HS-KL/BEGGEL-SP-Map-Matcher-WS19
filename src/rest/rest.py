import requests
from flask import jsonify
from flask import Flask, Response, request, render_template
from src.MapService import MapService
from src.GeoHashWrapper import GeoHashWrapper
app = Flask(__name__)

mapservice = MapService()

@app.route('/')
def rootpage():
    return render_template('anzeige.html')

@app.route('/tiles')
@app.route('/tiles/')
def get_tiles():
    """ :return List of Geohashes of the cached Tiles
    """

    tiles = mapservice.getAllCachedTiles()
    return jsonify({"description": "All Cached Tiles", "tiles": list(tiles.keys())})

@app.route('/geohashes', methods=["GET"])
def get_geohashes():
    """ :return tile of given GeoHash
    """

    bbox_str = request.args.get("bbox")

    bbox = []
    for val in bbox_str.split(","):
        bbox.append(float(val))

    geohashes = GeoHashWrapper().getGeoHashes(tuple(bbox), 5)

    print(tuple(bbox))
    print(geohashes)

    return str(geohashes)

@app.route('/tiles/<string:geohash>')
def get_tile(geohash):
    """ :return tile of given GeoHash
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

    return jsonify(data)

@app.route('/tiles/<string:geohash>/nodes')
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

    return jsonify(data)

@app.route('/tiles/<string:geohash>/links')
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

    return jsonify(data)

@app.route('/tiles/<string:geohash>/nodes/crossroads')
def get_crossroads(geohash):

    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    tile = mapservice.getOrLoadTile(geohash)
    data = []
    for node in tile.get_nodes():
        if len(node.get_links()) > 2:
            point = {
                "type": "Point",
                "coordinates": list(node.get_latlon())
                #"coordinates": list(node.get_latlon())

            }
            data.append(point)

    return jsonify(data)

@app.route('/tiles/<string:geohash>/links')
def get_route():
    pass


if __name__ == '__main__':
    app.run(host="0.0.0.0")
