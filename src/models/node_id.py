class NodeId:
    def __init__(self, osm_node_id, geohash):
        """:param geohash: geohash wird in voller Länge (als String) angegeben."""
        self.osm_node_id = osm_node_id
        self.geohash = geohash

    def __eq__(self, other):
        if type(other) is not NodeId:
            return False
        assert (isinstance(other, NodeId))

        return other.osm_node_id == self.osm_node_id and other.geohash == self.geohash

    def __ne__(self, other):
        return not (self is other)

    def __repr__(self):
        return "NodeId: <osm_node_id: %s> <geohash: %s>" % (self.osm_node_id, self.geohash)

    def __hash__(self):
        return self.osm_node_id

    def get_osm_node_id(self):
        return self.osm_node_id

    def get_geohash(self):
        return self.geohash