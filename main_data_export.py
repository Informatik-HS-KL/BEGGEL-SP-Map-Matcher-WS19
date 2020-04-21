from src.map_service import MapService
#from src.map_service import MapService

from src.geohash_wrapper import GeoHashWrapper
from src.models import BoundingBox, Car
from src.models import Link
from src.models import Node
from src.rest.app import app


def main():
    """
    This methods runs all tests from the directory tests. If any test fails the corresponding assertion will print an
    error. Otherwise nothing happens.
    :return: None
    """

    mapService = MapService()

    #nodes = mapService.get_nodes_in_bounding_box(BoundingBox (48.161844064843976, 11.572936935405323,48.1675975217803,11.578730506877491))
    nodes = mapService.get_nodes_in_bounding_box(BoundingBox (48.1301415 - 0.01,   11.5579533 - 0.01 ,48.1301415 + 0.01,   11.5579533 + 0.01))

    counter =0;
    for node in nodes:
        if "amenity" in node.get_tags() and counter < 20:
            counter = counter +1
            print("--------- Found POI at: " + node.to_wkt())
            for k,v in node.get_tags().items():
                print("  " + k + " --> " + v )



    # parse links
    links = mapService.get_links_in_bounding_box(BoundingBox (48.161844064843976, 11.572936935405323,48.1675975217803,11.578730506877491))



    for link in links[:1]:
        print(link.to_wkt())
        print(link.to_geojson())
        print(link.get_geometry())
        for k,v in link.get_tags().items():
            print(k + " --> " + v )
        print ("Car from Start: " , link.is_navigatable_from_start(Car()));
        print ("Car to Start: " , link.is_navigatable_to_start(Car()));
        print("Start Note: " , link.get_start_node().get_id())
        print("End Note: " , link.get_end_node().get_id().get_osm_id())
        print("Length Meter:" , link.get_length())


main()
#start_server()


