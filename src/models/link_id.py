from .node import NodeId


class LinkId:

    def __init__(self, osm_way_id, start_node_id: NodeId):
        self._osm_way_id = osm_way_id
        self._geohash = start_node_id.get_geohash()
        self._start_node_id = start_node_id

    def __eq__(self, other):
        if type(other) is not LinkId:
            return False
        assert (isinstance(other, LinkId))

        return other._osm_way_id == self._osm_way_id and self._start_node_id == other._start_node_id and \
            other._geohash == self._geohash

    def __repr__(self):
        return "LinkId: <osm_way_id: %s> <start_node_id: %s>" % (self._osm_way_id, self._start_node_id)

    def __ne__(self, other):
        return not (self is other)

    def __hash__(self):
        return hash("%s%s" % (self._osm_way_id, self._geohash))

    def get_start_node_id(self):
        """
        :return: NodeId-Object
        """
        return self._start_node_id

    def get_osm_way_id(self):
        """
        :return: int
        """
        return self._osm_way_id

    def get_geohash(self):
        """
        :return: str
        """
        return self._geohash
