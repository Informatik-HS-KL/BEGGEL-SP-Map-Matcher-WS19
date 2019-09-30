from src.map_service import MapService
from src.models.bounding_box import BoundingBox

def main():
    """
    """

    mapService = MapService()
    # mapService.setConfig1()
    # mapService.setConfig2()
    # mapService.setConfig3()
    # mapService.setApiKey("dsffdsfds")

    bbox = BoundingBox(49.24742019, 7.27371679, 49.38637445, 7.40483063)
    nodes = mapService.get_nodes_in_bounding_box(bbox)

    for node in nodes:
        print(node, node.get_lat(), node.get_lon())

    ##todo
    links = mapService.get_links_in_bounding_box(bbox)

    # Jeder Link soll die Information enthalten, von wem er benutzt werden kann (also z.B. Radfahrer, Fußgänger, Autos)
    links.navigatable # car, bike, pedestrial
    # Links sollen in bestimmte nützliche Geoformate umgewandelt werden können (Wkt, geoJson):
    link.toWkt()
    link.toGeoJson()
    # Ausgehende Links am Start- bzw. Endknoten eines Links sollen geliefert werden können:
    link.getLinksAtStartNode()
    link.getLinksAtEndNode()

    # Länge des links in metern
    # Haversine formula
    # https://medium.com/@petehouston/calculate-distance-of-two-locations-on-earth-using-python-1501b1944d97
    link.getLength()

    # Es muss klar, in welcher Richtung der Link befahren werden kann.
    # Kann der link vom Startknoten zum Endknoten befahren werden.
    link.isFromStart()
    # Kann der link vom Endknoten zum Startknoten befahren werden.
    link.isToStart()

    # Auch Links sollen eine Id haben die sich wie folgt zusammensetzt: (wayId , startNoteId, geoHash[volle Länge])
    link.id

    # Es soll möglich sein einen Link anhand seiner Id zu "laden" (wir "laden" aber immer noch das ganze Tile):
    mapService.loadLink(link.id)
    # Es soll möglich sein einen Link anhand von wayId und StartknotenId zu "laden" (wir "laden" aber immer noch das ganze Tile):
    mapService.loadLink(link.id.way_id,link.id.startNode)

    # Es soll möglich sein, alle zu Links, aus denen sich ein Way zusammensetzt, zu "laden" (wir "laden" aber immer noch das ganze Tile):
    List<Link> ll = mapService.loadLinks(link.id.way_id)

    # Nodes bekommen eine Id in der folgenden Form: (nodeId, geoHash [volle länge])
    node.id

    # Es werden alle Links im Umkreis einer Koordinate zurückgegeben (Radius=maxDistance).
    List<LinkDistance> listDistanceData = mapService.getLinksinRadius (lat, lon, maxDistance)



main()