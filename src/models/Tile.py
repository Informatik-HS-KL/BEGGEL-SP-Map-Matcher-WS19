
## In a tile all informration of the map is stored for a geohash rectangle (e.g. ezs42)

class Tile:
   ## maps nodeId --> Node object

   def __init__(self, geoHash, nodes : list, links : list):
      """"""

      self._nodes = nodes
      self._links = links
      self._geohash = geoHash

   def addNode(self, node):
      self._nodes.update({node._id: node})

   def getNodes(self):
      return self._nodes

   def getLinks(self):
      return  self._links
