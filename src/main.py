from src.map_service import MapService
from src.models.bounding_box import BoundingBox
from src.models.link import LinkUser


def main():
    """ Test Main
    """
    mapService = MapService()
    # bbox = BoundingBox.from_geohash("u0v970")
    # nodes = mapService.get_nodes_in_bounding_box(bbox)
    #
    # links = mapService.get_links_in_bounding_box(bbox)
    #
    # for l in links:
    #     print(l)
    #
    # linkdists = mapService.get_linkdistances_in_radius(nodes[1].get_latlon(), 150) # meter
    # for ld in linkdists:
    #     print("LinkDistance: ", ld.get_distance(),"m", "Fraction: ", ld.get_fraction())


    print("Tests zu LinkDirections:")
    mapService.get_tile("u155h")
    links = mapService.get_links(4353510)
    print(len(links))
    for link in links:
        print(link)
        print(link.is_navigatable_to_start(LinkUser.PEDESTRIAN))
        print(link.is_navigatable_from_start(LinkUser.PEDESTRIAN))
        print(link.is_navigatable_to_start(LinkUser.CYCLIST))
        print(link.is_navigatable_from_start(LinkUser.CYCLIST))
        print(link.is_navigatable_to_start(LinkUser.CAR))
        print(link.is_navigatable_from_start(LinkUser.CAR))

from src.rest.app import app
def start_server():

    if __name__ == '__main__':
        print("localhost:5000/api")
        app.run(host="localhost", port=5000)

main()


# start_server()
