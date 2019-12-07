from src.map_service import MapService
from src.models.bounding_box import BoundingBox
from src.models.link import Link
from src.models.link_id import LinkId
from src.models.link_user import Pedestrian, Cyclist, Car
from src.models.node_id import NodeId
from src.utils.router import RouterDijkstra


def main():
    """ Test Main
    """
    mapService = MapService()
    linksA = mapService.get_link_by_id(LinkId(37755038, NodeId(2206819858, "u0v92eb6ngct")))
    linksB = mapService.get_link_by_id(LinkId(145913348, NodeId(1592414992, "u0v92tm9768g")))

    # Link: <link_id: LinkId: <osm_way_id: 145913348> <start_node_id: NodeId: <osm_node_id: 1592414943> <geohash: u0v92tjry3y9>>
    linksA = mapService.get_link_by_id(LinkId(206630217, NodeId(1592414943, "u0v92tjry3y9")))

    print("Link a",linksA.get_id())
    print("sn: ")
    for link in linksA.get_links_at_start_node():
        print(link.get_id(), linksA in link.get_links_at_end_node() or linksA in link.get_links_at_start_node())
    print("en:")
    for link in linksA.get_links_at_start_node():
        print(link.get_id(), linksA in link.get_links_at_end_node() or linksA in link.get_links_at_start_node())
    print("sn als Car: ")
    for link in linksA.get_links_at_start_node(Car()):
        print(link.get_id(), linksA in link.get_links_at_end_node() or linksA in link.get_links_at_start_node())
    print("en als Car:")
    for link in linksA.get_links_at_start_node(Car()):
        print(link.get_id(), linksA in link.get_links_at_end_node() or linksA in link.get_links_at_start_node())

    print()
    print("Link b", linksB.get_id())
    print("sn: ")
    for link in linksB.get_links_at_start_node():
        print(link.get_id(), linksB in link.get_links_at_end_node() or linksB in link.get_links_at_start_node())
    print("en:")
    for link in linksB.get_links_at_start_node():
        print(link.get_id(), linksB in link.get_links_at_end_node() or linksB in link.get_links_at_start_node())
    print("sn als Car: ")
    for link in linksB.get_links_at_start_node():
        print(link.get_id(), linksB in link.get_links_at_end_node() or linksB in link.get_links_at_start_node())
    print("en als Car:")
    for link in linksB.get_links_at_start_node():
        print(link.get_id(), linksB in link.get_links_at_end_node() or linksB in link.get_links_at_start_node())
    #

    # router = RouterDijkstra(Car())  # Mit Laden: ~13 ohne 0.85
    # router.set_max_iterations(mapService.config.getint("DEFAULT", "max_dijkstra_iterations"))
    #
    # router.set_start_link(linksA)
    # router.set_end_link(linksB)
    # result_nodes = router.compute()
    # for node in result_nodes:
    #     print(node)


from src.rest.app import app
def start_server():

    if __name__ == '__main__':
        print("localhost:5000/api")
        app.run(host="localhost", port=5000)

start_server()
# main()