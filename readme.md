[Picture 1]: doc/images/webPage.jpg  "Visualisation of Links and Nodes"
# Map Service
The Map Service is a tool, that loads data from the OpenStreetMap and prepares it for the user.  
It handles the memory management and provides functions for routing and map matching.  
## Requirements

1. Python: 3.7  
2. shapely  

## Installation
1. Install shapely
2. in work
### Installation Shapely
1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html )
2. Execute <code>conda install shapely</code> in Anaconda Prompt

## Configurations
in work

## Functions

### Example
<!--
was ist mit den imports 
(muss man wenn man unser programm nutzt immer über src gehen)??
-->
    from src.map_service import MapService
    from src.models.bounding_box import BoundingBox
    
    def test()
        """
        Print all nodes in Geohash 'u0v970'
        """
        mapService = MapService()
        bbox = BoundingBox.from_geohash("u0v970") # One way to create a BoundingBox
        nodes = mapService.get_nodes_in_bounding_box(bbox) # all in_bounding_box load the
                                                           # street data automatically
        for node in nodes:
            print(node, node.get_lat(), node.get_lon())
        


### Functions to get Link(s) 
#### Links in Bounding Box
    mapService.get_links_in_bounding_box(BoundingBox(south: float, 
                                                     west:  float, 
                                                     north: float, 
                                                     east:  float))
Return a array with Links in the Bounding Box.  
If BBox outside the already loaded tiles, the required tile's will be loaded

#### Links with osm way id
    mapService.get_links(38936691)
Return a array with Links that have the given way id.  

#### Link with Link id
    mapService.get_link(38936691, LinkId(38936691, NodeId(osmId, geoHash)))
Return a Link with the given Link id and Way id.  
### Functions to get Node(s) 
#### Node by Id
    mapService.get_node(NodeId(osmId, geoHash))
Return a Node with the given Node Id.
#### Nodes in BBox
    mapService.get_links_in_bounding_box(BoundingBox(south: float, 
                                                     west:  float, 
                                                     north: float, 
                                                     east:  float))
Return all Nodes as Array in the Bounding box.  
If BBox outside the already loaded tiles, the required tile's will be loaded


### Functions to get Tile(s)
#### Tile with geohash
    mapService.get_links_in_bounding_box("u0v970")
If not loaded the Interface will download the street data 
and return it as a Tile with nodes and Links
#### All Cached Tiles
    mapService.get_all_cached_tiles()
Return all already loaded Tiles
## Data Visualisation (testing)
After the start you have the opportunity to Visual your Links and Nodes. 
We implement a test web page under [localhost](http://http://localhost:5000/). 
![Picture 1]

In the Visualisation you can choose if you want to see all Nodes or Links in a Geohash.
Set Nodes and Links are preserved.

## Supported Geo function's
in work

## Wrongdoer
  
Lukas F. , Sebastian L. , Kai P.  
Supervisor:  
Prof. Beggel  
