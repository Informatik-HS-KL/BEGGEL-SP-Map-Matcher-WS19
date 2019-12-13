from src.map_service import MapService
from src.models.bounding_box import BoundingBox
from src.models.link import Link
from src.models.link_id import LinkId
from src.models.link_user import Pedestrian, Cyclist, Car
from src.models.node_id import NodeId
from src.utils.router import RouterDijkstra
from src.geo_hash_wrapper import GeoHashWrapper

def main():
    ghw = GeoHashWrapper()
    print(ghw._get_neighbors("rzzz"))


from src.rest.app import app
def start_server():

    if __name__ == '__main__':
        print("localhost:5000/api")
        app.run(host="localhost", port=5000)

main()
start_server()
