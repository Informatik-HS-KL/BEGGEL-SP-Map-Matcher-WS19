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
1. Install [Conda](https://docs.conda.io/en/latest/miniconda.html )
2. Execute <code>conda install shapely</code> in Anaconda Prompt

## Configurations
in work

## Functions
A list of the base Functions from Map Service
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
        nodes = mapService.get_nodes_in_bounding_box(bbox) # [..]_in_bounding_box functions load the
                                                           # not yet loaded street data automatically
        for node in nodes:
            print(node, node.get_lat(), node.get_lon())
        


### Functions to get Link(s) 
#### Links in Bounding Box
    mapService.get_links_in_bounding_box(BoundingBox(south: float, 
                                                     west:  float, 
                                                     north: float, 
                                                     east:  float))
Returns a array with Links in the Bounding Box.  
If the Box is span over the already loaded tiles, the required will be loaded

#### Links with osm way id
    mapService.get_links(38936691)
Returns a array with Links that have the given way id.  

#### Link with Link id
    mapService.get_link(38936691, NodeId(418726074, "u0v978xvcgrt"))
Returns a Link with the given Link id and Way id.  
### Functions to get Node(s) 
#### Node by Id
    mapService.get_node(NodeId(418726074, "u0v978xvcgrt"))
Returns a Node with the given Node Id.
#### Nodes in BBox
    mapService.get_links_in_bounding_box(BoundingBox(south: float, 
                                                     west:  float, 
                                                     north: float, 
                                                     east:  float))
Returns all Nodes as Array in the Bounding box.  
If the Box is span over the already loaded tiles, the required will be loaded

### Functions to get Tile(s)
#### Tile with geohash
    mapService.get_links_in_bounding_box("u0v970")
If not loaded the Interface will download the street data 
and return it as a Tile with nodes and Links
#### All Cached Tiles
    mapService.get_all_cached_tiles()
Returns all already loaded Tiles
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
