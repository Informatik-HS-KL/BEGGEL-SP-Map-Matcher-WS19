from src.map_service import MapService
from src.models.bounding_box import BoundingBox
from src.models import Link
from src.models import LinkId
from src.models import Pedestrian, Cyclist, Car
from src.models import NodeId
from src.utils.router import RouterDijkstra
from src.geohash_wrapper import GeoHashWrapper
from src.rest.app import app


def main():
    ghw = GeoHashWrapper()
    print(ghw._get_neighbors("rzzz"))


def start_server():

    if __name__ == '__main__':
        print("localhost:5000/api")
        app.run(host="localhost", port=5000)


main()
start_server()
