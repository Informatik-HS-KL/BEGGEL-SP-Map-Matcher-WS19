class NodeId:
    def __init__(self, osm_id, geohash):
        """
        :param osm_id: int
        :param geohash: str
        """
        self._osm_id = osm_id
        self._geohash = geohash

    def __eq__(self, other):
        if type(other) is not NodeId:
            return False
        assert (isinstance(other, NodeId))

        return other._osm_id == self._osm_id and other._geohash == self._geohash

    def __ne__(self, other):
        return not (self is other)

    def __repr__(self):
        return "NodeId: <osm_node_id: %s> <geohash: %s>" % (self._osm_id, self._geohash)

    def __hash__(self):
        return self._osm_id

    def get_osm_id(self):
        """
        :return: int
        """
        return self._osm_id

    def get_geohash(self):
        """
        :return: str
        """
        return self._geohash
