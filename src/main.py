from src.map_service import MapService
from src.models.bounding_box import BoundingBox
from src.models.link import Link
from src.models.node import NodeId, Node
from src.models.tile import Tile
from src.models.link_distance import LinkDistance

def main():
    """
    """

    mapService = MapService()
    # mapService.setConfig1()
    # mapService.setConfig2()
    # mapService.setConfig3()
    # mapService.setApiKey("dsffdsfds")
    # mapservice.set_config("cachelevel",5)

    #bbox = BoundingBox(49.24742019, 7.27371679, 49.38637445, 7.40483063)
    #nodes = mapService.get_nodes_in_bounding_box(bbox)

    #for node in nodes:
    #    print(node, node.get_lat(), node.get_lon())

    ## todo
    #link = mapService.get_links_in_bounding_box(bbox)

    # Jeder Link soll die Information enthalten, von wem er benutzt werden kann (also z.B. Radfahrer, Fußgänger, Autos)
    # link.navigatable # car, bike, pedestrial
    # Links sollen in bestimmte nützliche Geoformate umgewandelt werden können (Wkt, geoJson):
    #link.to_wkt()
    #link.to_geojson()
    # Ausgehende Links am Start- bzw. Endknoten eines Links sollen geliefert werden können:
    #link.get_links_at_startnode()
    #link.get_links_at_endnode()

    # Länge des links in metern
    # Haversine formula
    # https://medium.com/@petehouston/calculate-distance-of-two-locations-on-earth-using-python-1501b1944d97
    # link.get_length()

    # Es muss klar, in welcher Richtung der Link befahren werden kann.
    # Kann der link vom Startknoten zum Endknoten befahren werden.
    #link.is_from_start()
    # Kann der link vom Endknoten zum Startknoten befahren werden.
    #link.is_to_start()

    # Auch Links sollen eine Id haben die sich wie folgt zusammensetzt: (wayId , startNoteId, geoHash[volle Länge])
    # link.id

    # Es soll möglich sein einen Link anhand seiner Id zu "laden" (wir "laden" aber immer noch das ganze Tile):
    #mapService.load_link(link.id)
    # Es soll möglich sein einen Link anhand von wayId und StartknotenId zu "laden" (wir "laden" aber immer noch das ganze Tile):
    #mapService.load_link(link.id.way_id,link.id.start_node)

    # Es soll möglich sein, alle zu Links, aus denen sich ein Way zusammensetzt, zu "laden" (wir "laden" aber immer noch das ganze Tile):
    #listLink = mapService.load_links(link.id.way_id)

    # Nodes bekommen eine Id in der folgenden Form: (nodeId, geoHash [volle länge])
    # node.id

    # Es werden alle Links im Umkreis einer Koordinate zurückgegeben (Radius=maxDistance).
    listDistanceData = mapService.get_links_in_radius((1.0, 2.0), 50)

def main2():

    ms = MapService()

    nodes = ms.get_nodes_in_bounding_box(BoundingBox.from_geohash("u0v3h"))
    print([ n.get_latlon() for n in nodes])
    #print(ms.get_nodes_in_bounding_box(BoundingBox.from_geohash("u0v3h")))

    print(ms.get_tile("u0v3h"))

    print(LinkDistance(((49.4035415, 7.5638974))).get_matched())

main2()
#main()
