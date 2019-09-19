import requests
from flask import jsonify
from flask import Flask, Response, request, render_template
from src.MapService import MapService
app = Flask(__name__)

mapservice = MapService()

@app.route('/')
def rootpage():
    return render_template('anzeige.html')

@app.route('/tiles')
@app.route('/tiles/')
def get_tiles():
    """
    """

    tiles = mapservice.getAllCachedTiles()
    return jsonify({"description": "All Cached Tiles", "tiles": list(tiles.keys())})

@app.route('/tiles/<string:geohash>')
def get_tile(geohash):
    """
    """
    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    tile = mapservice.getOrLoadTile(geohash)
    data = []

    for node in tile.getNodes():
        point = {
            "type": "Point",
            "coordinates": list(node.getLatLon())
        }
        data.append(point)

    return jsonify(data)

@app.route('/tile/<string:geohash>/nodes')
def get_nodes(geohash):
    """
    """
    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    tile = mapservice.getOrLoadTile(geohash)
    data = []
    for node in tile.getNodes():
        point = {
            "type": "Point",
            "coordinates": list(node.getLatLon())
        }
        data.append(point)

    return jsonify(data)

@app.route('/tiles/<string:geohash>/links')
def get_links(geohash):
    """
    """

    if len(geohash) < 4:
        return jsonify({"Error": "Level have to be >= 4"})

    tile = mapservice.getOrLoadTile(geohash)

    data = []
    for link in tile.getLinks():
        linestr = {
            "type": "LineString",
            "coordinates": [list(link.startNode.getLatLon()), list(link.endNode.getLatLon())]
        }
        data.append(linestr)

    return jsonify(data)

    return str(tile.getLinks())


if __name__ == '__main__':
    app.run(host="0.0.0.0")
