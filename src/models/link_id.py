from .node import NodeId

class LinkId:

    def __init__(self, osm_way_id, start_node_id: NodeId):
        self.osm_way_id = osm_way_id
        self.geohash = start_node_id.geohash
        self.start_node_id = start_node_id

    def __eq__(self, other):
        if type(other) is not LinkId:
            return False
        assert (isinstance(other, LinkId))

        return other.osm_way_id == self.osm_way_id and self.start_node_id == other.start_node_id and \
            other.geohash == self.geohash

    def __ne__(self, other):
        return not (self is other)

    def __hash__(self):
        return hash("%s%s" % (self.osm_way_id, self.geohash))

    def get_start_node_id(self):
        """Getter Startnode
        :return: Nodeid
        """

        return self.start_node_id