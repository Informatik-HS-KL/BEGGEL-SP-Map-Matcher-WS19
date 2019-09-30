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

    links.navigatable # car, bike, pedestrial
    link.toWkt()
    link.toGeoJson()
    link.getLinksAsStartNode()
    link.getLinksAsEndNode()

    # lange des links in metern
    #Haversine formula
    #https://medium.com/@petehouston/calculate-distance-of-two-locations-on-earth-using-python-1501b1944d97
    link.getLength()

    ## kann der link vom Start knoten zum End knoten befahren werden
    link.isFromStart()
    ## kann der link vom End knoten zum Start knoten befahren werden
    link.isToStart()

    # (wayId , startNoteId, geoHash[volle länge])
    link.id

    mapService.loadLink (link.id)

    mapService.loadLink(link.id.way_id,link.id.startNode)

    List<Link> ll = mapService.loadLinks(link.id.way_id)

    # (nodeId, geoHash [volle länge])
    node.id

    List<LinkDistance> listDistanceData = mapService.getLinksinRadius (lat, lon, maxDistance)



main()