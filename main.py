from src.map_service import MapService
from src.models.bounding_box import BoundingBox
from src.models.link import Link

def main():
    """ Test Main
    """
    mapService = MapService()
    bbox = BoundingBox.from_geohash("u0v970")
    nodes = mapService.get_nodes_in_bounding_box(bbox)

    links = mapService.get_links_in_bounding_box(bbox)

    for l in links:
        print(l)

    linkdists = mapService.get_linkdistances_in_radius(nodes[1].get_latlon(), 150) # meter
    for ld in linkdists:
        print("LinkDistance: ", ld.get_distance(),"m", "Fraction: ", ld.get_fraction())

def main2():
    mapService = MapService()

    tile = mapService.get_tile("u0v90")
    mapService.get_tile("u0v91")
    mapService.get_tile("u33dc")
    #mapService.get_tile("u33d")

    for i in tile.get_links():
        print(i.get_geometry())

from src.rest.app import app
def start_server():

    if __name__ == '__main__':
        print("localhost:5000/api")
        app.run(host="localhost", port=5000)

main2()
#main()
start_server()#
for i in t1.get_links():
    print(Link)