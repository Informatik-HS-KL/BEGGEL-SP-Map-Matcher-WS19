"""
Wrapper Klass for Mapservice which will be used to get REST link access to Mapservice für Rest Api
"""

from src.geo_hash_wrapper import GeoHashWrapper
from src.models.bounding_box import BoundingBox
from src.models.link_user import Car
from src.utils.router import RouterDijkstra


class MapserviceWrapper:

    def __init__(self, mapservice):

        self.ms = mapservice

    def get_dict_tiles(self):
        """
        :return: dict
        """

        tiles = self.ms.get_all_cached_tiles()
        data = {}
        for k, v in tiles.items():
            bbox = BoundingBox.from_geohash(k)
            data[k] = {
                "nodes.length": len(v.get_nodes()),
                "bbox": {
                    "south": bbox.south,
                    "west": bbox.west,
                    "north": bbox.north,
                    "east": bbox.east
                }
            }
        return data

    def get_dict_stats(self):
        """
        :return: dict
        """

        tiles = self.ms.get_all_cached_tiles()

        count_nodes = 0
        count_links = 0
        all_tiles = []

        for k, v in tiles.items():
            all_tiles.append(k)
            count_links += len(v.get_links())
            count_nodes += len(v.get_nodes())

        data = {
            "count:tiles": len(all_tiles),
            "count:nodes": count_nodes,
            "count:links": count_links
        }
        return data

    def get_dict_geohashes(self, bbox):
        """

        :param bbox:
        :return: dict
        """

        geohashes = GeoHashWrapper().get_geohashes(bbox, 5)

        data = {}

        for geohash in geohashes:
            data[geohash] = {
                "south": BoundingBox.from_geohash(geohash).south,
                "west": BoundingBox.from_geohash(geohash).west,
                "north": BoundingBox.from_geohash(geohash).north,
                "east": BoundingBox.from_geohash(geohash).east,
            }

        return data

    def get_dict_tile(self, geohash):
        """

        :param geohash:
        :return: dict
        """

        tile = self.ms.get_tile(geohash)
        data = {
            "geohash": tile.get_geohash(),
            "nodes.length": len(tile.get_nodes()),
            "links.length": len(tile.get_links()),
            "bbox": str(BoundingBox.from_geohash(geohash))
        }
        return data

    def get_dict_nodes(self, geohash):
        """

        :param geohash:
        :return: dict
        """

        tile = self.ms.get_tile(geohash)
        data = []
        for node in tile.get_nodes():
            data.append(node.to_geojson())

        return data

    def get_dict_node(self, geohash, osm_id):
        """

        :param nodeid:
        :return: dict
        """

        tile = self.ms.get_tile(geohash)
        node = tile.get_node_from_osm_id(osm_id)
        if not node:
            return {"error": "No Node with osm id:" + str(osm_id)}

        return node.to_geojson()

    def get_dict_links(self, geohash):
        """
        :return: dict
        """

        data = []
        tile = self.ms.get_tile(geohash)

        for link in tile.get_links():
            data.append(link.to_geojson())

        return data

    def get_dict_link(self, linkid):
        """

        :param linkid:
        :return: dict
        """
        return

    def get_dict_intersections(self, geohash):
        """

        :param geohash:
        :return: dict
        """

        tile = self.ms.get_tile(geohash)
        data = []
        for node in tile.get_nodes():
            if len(node.get_links()) > 2:
                point = node.to_geojson()
                data.append(point)

        return data

    def get_dict_way_links(self, way_id):
        """

        :param wayid:
        :return: dict
        """

        data = []
        for link in self.ms.get_links(way_id):
            data.append(link.to_geojson())

        return data

    def get_dict_linkdistances(self, pos, radius):
        """

        :param point:
        :return: dict
        """

        linkdists = self.ms.get_linkdistances_in_radius(pos, radius)

        data = [radius, []]
        for ld in linkdists:
            ld_data = {
                "link": ld.link.to_geojson(),
                "distance": ld.get_distance(),
                "fraction": ld.get_fraction()
            }
            data[1].append(ld_data)

        return data

    def get_list_route(self, pos1: tuple, pos2: tuple):
        circle_size = 20

        try:
            start_link = self.ms.get_linkdistances_in_radius(pos1, circle_size)[0].get_link()
            end_link = self.ms.get_linkdistances_in_radius(pos2, circle_size)[0].get_link()
        except Exception:
            return {"exception": "no link found"}

        # router = RouterBaseDijkstra(Car())  # Mit Laden: ~11 ohne 1,21
        # router = RouterLinkDijkstra(Car())  # Mit Laden: ~12 ohne 3,31
        router = RouterDijkstra(Car())  # Mit Laden: ~13 ohne 0.85
        router.set_max_iterations(self.ms.config.getint("DEFAULT", "max_dijkstra_iterations"))

        router.set_start_link(start_link)
        router.set_end_link(end_link)
        try:
            result = router.compute()
        except Exception as e:
            return {"exception": str(e)}
        print(result)
        length = "{:.3f}".format(result[0]) + " " + result[1]
        data = [length, []]
        link_list = result[2]

        for link in link_list:
            data[1].append(link.to_geojson())

        return data
