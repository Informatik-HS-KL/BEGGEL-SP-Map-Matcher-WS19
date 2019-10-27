from src.map_service import MapService
from src.models.bounding_box import BoundingBox
from src.models.link import Link
from src.models.node import NodeId, Node
from src.models.tile import Tile
from src.models.link_distance import LinkDistance
from src.over_pass_wrapper import OverpassWrapper

def main():
    """
    """
    mapService = MapService()
    bbox = BoundingBox.from_geohash("u0v970")
    nodes = mapService.get_nodes_in_bounding_box(bbox)

    for node in nodes:
        print(node, node.get_lat(), node.get_lon())

    links = mapService.get_links_in_bounding_box(bbox)

    for l in links:
        print(l.to_wkt())
        print(l.to_geojson())
        print(l.get_length())


    link = links[0]
    # Ausgehende Links am Start- bzw. Endknoten eines Links sollen geliefert werden können:

    startlinks = link.get_links_at_start_node()
    print(startlinks)
    endlinks = link.get_links_at_end_node()
    print(endlinks)

    # # Link Distance
    # link = mapService.get_link(38936694, NodeId(462739567, "u0v97b9yr5gy"))
    # pos = (49.4419412, 7.9026608)
    # ld = LinkDistance(pos, link)
    # print("Link Distance: ", ld.get_distance(),"Link Fraction:", ld.get_fraction())
    #
    # waylinks = mapService.get_links(38936691)
    # print(waylinks)
    # l = mapService.get_link(38936691, NodeId(1784694212, "u0v97b8pkp3w"))
    # print(l)
    #
    # listDistanceData = mapService.get_linkdistances_in_radius(pos, 50)
    #
    # for ld in listDistanceData:
    #     print("Ld", ld.link.get_link_id(), "Distance:", ld.get_distance())
    #     #print("linkID: " + ld.link.get_link_id().geohash)

    # Jeder Link soll die Information enthalten, von wem er benutzt werden kann (also z.B. Radfahrer, Fußgänger, Autos)
    # link.navigatable # car, bike, pedestrial
    # Links sollen in bestimmte nützliche Geoformate umgewandelt werden können (Wkt, geoJson):

    # Es muss klar, in welcher Richtung der Link befahren werden kann.
    # Kann der link vom Startknoten zum Endknoten befahren werden.
    # link.is_from_start()
    # Kann der link vom Endknoten zum Startknoten befahren werden.
    # link.is_to_start()

    # Auch Links sollen eine Id haben die sich wie folgt zusammensetzt: (wayId , startNoteId, geoHash[volle Länge])


from src.rest.app import app
def start_server():

    if __name__ == '__main__':
        print("localhost:5000/api")
        app.run(host="localhost", port=5000)

main()

start_server()
