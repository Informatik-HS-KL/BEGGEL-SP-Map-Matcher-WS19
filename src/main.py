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

main()