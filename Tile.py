
## In a tile all informration of the map is stored for a geohash rectangle (e.g. ezs42)



class Tile:
   ## maps nodeId --> Node object

   def __init__(self):
      """"""
      self._nodes = {}
      self._links = {}
      self._geohash = None

