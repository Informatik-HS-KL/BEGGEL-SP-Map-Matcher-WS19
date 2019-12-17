"""
Description: The GeohashWrapper encapsulates the functionality of the following geohash-library:
https://github.com/vinsci/geohash/
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
https://github.com/vinsci/geohash/
"""

import geohash2 as geohash
from .models import BoundingBox


class GeoHashWrapper:
    base32 = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'b', 'c', 'd', 'e', 'f',
              'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

    def __init__(self):
        pass

    def get_geohash(self, pos: tuple, level):
        """
        :param pos: tuple(lat, lon)
        :param level: int
        :return: str
        """

        return geohash.encode(pos[0], pos[1], precision=level)

    def get_geohashes(self, bbox: BoundingBox, level: int):
        """
        Returns the geohashes of the tiles which overlap with bbox.
        :param bbox: BoundingBox-Object
        :param level: int
        :raises: Exception if bbox is too big
        :return: list(str)
        """

        bbox_middle = ((bbox.south + bbox.north) / 2, (bbox.west + bbox.east) / 2)
        # Wir gehen ein geohash-Level höher:
        geohash_for_middle = self.get_geohash(bbox_middle, level - 1)

        base_geohashes = [geohash_for_middle]

        if bbox not in BoundingBox.from_geohash(geohash_for_middle):
            neighbors = self.get_neighbors(geohash_for_middle)

            if bbox not in self._get_bounding_box_from_neighbors(neighbors):
                raise Exception(
                    "Die angegebene BoundingBox ist zu groß, da sie die Größe einer Kachel mit geohash_level = %s "
                    "überschreitet." % (level - 1))
            else:
                base_geohashes.extend(list(neighbors.values()))

        found_geohashes = []

        for base_geohash in base_geohashes:

            for b in self.base32:
                new_geohash = base_geohash + b
                if bbox.overlap(BoundingBox.from_geohash(new_geohash)):
                    found_geohashes.append(new_geohash)

        return found_geohashes

    def _get_bounding_box_from_neighbors(self, neighbors: dict):
        """
        Returns the Bounding Box which is covering the neighbors.
        :param neighbors: dict
        :return: BoundingBox-Object
        """

        west = BoundingBox.from_geohash(neighbors["west"]).west
        east = BoundingBox.from_geohash(neighbors["east"]).east

        south = None
        if neighbors.get("south"):
            south = BoundingBox.from_geohash(neighbors["south"]).south
        else:
            south = BoundingBox.from_geohash(neighbors["east"]).south

        north = None
        if neighbors.get("north"):
            north = BoundingBox.from_geohash(neighbors["north"]).north
        else:
            north = BoundingBox.from_geohash(neighbors["east"]).north

        return BoundingBox(south, west, north, east)

    def get_neighbors(self, geohash_string):
        """
        Returns the geohashes of the neighbors Tiles.
        Adapted/copied from https://github.com/tammoippen/geohash-hilbert/blob/master/geohash_hilbert/_utils.py
        :param geohash_string: str
        :return: dict
        """
        lat, lon, lat_err, lon_err = geohash.decode_exactly(geohash_string)
        precision = len(geohash_string)

        north = lat + 2 * lat_err

        south = lat - 2 * lat_err

        east = lon + 2 * lon_err
        if east > 180:
            east -= 360

        west = lon - 2 * lon_err
        if west < -180:
            west += 360

        neighbours_dict = {
            'east': geohash.encode(lat, east,  precision),
            'west': geohash.encode(lat, west, precision),
        }

        if north <= 90:  # input cell not already at the north pole
            neighbours_dict.update({
                'north': geohash.encode(north, lon, precision),
                'north-east': geohash.encode(north, east, precision),
                'north-west': geohash.encode(north, west, precision),
            })

        if south >= -90:  # input cell not already at the south pole
            neighbours_dict.update({
                'south': geohash.encode(south, lon, precision),
                'south-east': geohash.encode(south, east, precision),
                'south-west': geohash.encode(south, west, precision),
            })

        return neighbours_dict
