[Picture 1]: doc/images/webPage.jpg  "Visualisation of Links and Nodes"
# Map Service
The Map Service is an interface to the [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API). 
He downloads street data and takes over their administration. 
The street data downloaded individually via a [Geohash](https://en.wikipedia.org/wiki/Geohash) and stored in Tiles. 
In the Tiles there are links that extend from intersection to intersection and nodes that represent individual points on the road.  
It has implemented functions for routing and determining links within a certain radius to allow the user to easily map matching.  
For a simpler check of the links and nodes, a website was created using [Leaflet](https://leafletjs.com/). 
## Requirements

1. Python: 3.7 [(download)](https://www.python.org/downloads/)
2. shapely
3. flask

## Installation
1. Install shapely
2. in work
### Installation Shapely
1. Install [Conda](https://docs.conda.io/en/latest/miniconda.html )
2. Execute <code>conda install shapely</code> in Anaconda Prompt

## Configurations
The base configurations of the Project are in the src/config.ini file.
In this configurations are 3 sections.
1. DEFAULT Selection  
In this selection are base parameters like overpass_url etc.
2. HIGHWAY_CARS Selection  
In this selection you can choose the loaded street types for vehicles.
By Default all street types will loaded.  
More information over the street types you can find [here](https://wiki.openstreetmap.org/wiki/Key:highway#Special_road_types)  

## Example
This example load a Tile with the Geohash 'u0v970' from Overpass and print all nodes. 
<!--
was ist mit den imports 
(muss man wenn man unser programm nutzt immer über src gehen)??
-->
    from src.map_service import MapService
    from src.models.bounding_box import BoundingBox
    
    def print_nodes_from_hash():
        """
        Print all nodes in Geohash 'u0v970'
        """
        mapService = MapService()
        bbox = BoundingBox.from_geohash("u0v970")  # One way to create a BoundingBox
        nodes = mapService.get_nodes_in_bounding_box(bbox)  # [..]_in_bounding_box functions load the
        # not yet loaded street data automatically
        for node in nodes:
            print(node, node.get_lat(), node.get_lon())
        


## Models
The following paragraph discusses the data model in the Map Service
### Nodes
Nodes are a reflection of the nodes of Overpass.
They have an ID consisting of a Lvl 12 Geohash and the Node Id from Overpass Node.

### Links

### Tiles

## Functions
Below is a list of the basic functions.  
All functions that receive a bounding box load any needed tiles.

### Functions to get Link(s) 

#### Links in Bounding Box
    mapService.get_links_in_bounding_box(BoundingBox(south: float, 
                                                     west:  float, 
                                                     north: float, 
                                                     east:  float))
Returns a array with Links in the Bounding Box.  

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

### Functions to get Tile(s)

#### Tile with geohash
    mapService.get_links_in_bounding_box("u0v970")
If not loaded the Interface will download the street data 
and return it as a Tile with nodes and Links.

#### All Cached Tiles
    mapService.get_all_cached_tiles()
Returns all already loaded Tiles.

### Routing
    
    def routing():
        mapService = MapService()
        
        # Init Router with Linkuser (Car, Cyclist or Pedestrian)
        router = RouterDijkstra(Car())
    
        # set the start link
        router.set_start_link(mapService.get_link(314409401, NodeId(258779029, "u0v9045fe6u1")))
        ## optional fraction (position on link: 1>= fraction >= 0)
        # router.set_start_link(mapService.get_link(314409401, NodeId(258779029, "u0v9045fe6u1")),0.0)
        ## optional fraction and position (from_start_to_end as boolean)
        # router.set_start_link(mapService.get_link(314409401, NodeId(258779029, "u0v9045fe6u1")),1.0, True)
    
        # set the end link
        router.set_end_link(mapService.get_link(25779169, NodeId(281181557, "u0v922p75804")))
        ## optional fraction (position on link: 1>= fraction >= 0)
        # router.set_end_link(mapService.get_link(25779169, NodeId(281181557, "u0v922p75804")),0.0)
        ## optional fraction and position (from_start_to_end as boolean)
        # router.set_end_link(mapService.get_link(25779169, NodeId(281181557, "u0v922p75804")),1.0, True)
    
        # Calculates the shortest route and returns it as a list of nodes
        result_nodes = router.compute()  # Returns a list of nodes as a way
This example calculates the route using the Dijkstra. 
The route is returned as a node list. 
The Dijkstra also takes into account one-way streets. 
    
### Distances

    def example()
        bbox = BoundingBox.from_geohash("u0v970")
        
        nodes = mapService.get_nodes_in_bounding_box(bbox)
        links = mapService.get_links_in_bounding_box(bbox)
        
        linkdists = mapService.get_linkdistances_in_radius(nodes[1].get_latlon(), 150) # meter
        for ld in linkdists:
            print("LinkDistance: ", ld.get_distance(),"m", "Fraction: ", ld.get_fraction())

This example prints out all links with their distances around the first point (Node) in the Tile.
    
## Own OverpassWrapper
You're able to create Your Own OverpassWrapper Class.
derive from the abstract OverpassWrapper and overwrite load_tile with your own 
 
## Data Visualisation (testing)
After the start you have the opportunity to Visual your Links and Nodes. 
We implement a test web page under [localhost](http://http://localhost:5000/). 
![Picture 1]

In the Visualisation you can choose if you want to see all Nodes or Links in a Geohash.
Set Nodes and Links are preserved.

## Contributer
  
Lukas F. , Sebastian L. , Kai P.  
Supervisor:  
Prof. Beggel  
