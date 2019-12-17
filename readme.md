[Picture 1]: doc/images/webPage1.jpg  "Visualisation of Links and Nodes"
[Picture 2]: doc/images/webPage.jpg  "Visualisation of Routing"
[Picture 3]: doc/images/webPage3.jpg  "Visualisation of Link Distance"

# Map Service
The Map Service is an interface to the [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API). 
It downloads street data and takes over their administration. 
The street data are downloaded and stored in Tiles. 
In the Tiles there are links that extend from intersection to intersection and nodes that represent individual points on the road.  
It has implemented functions for routing and determining links within a certain radius to allow the user to easily map matching.  
For a simpler visualisation of the links and nodes, a website was created using [Leaflet](https://leafletjs.com/). 

## Requirements
1. Python: 3.7 [(download)](https://www.python.org/downloads/)
2. shapely
3. geohash2

## Installation


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
By Default all street types will be loaded.  
More information about the street types you can find [here](https://wiki.openstreetmap.org/wiki/Key:highway#Special_road_types)  
 
## Models
The following paragraph discusses the data model in the Map Service

### Nodes
Nodes are a depict of the nodes of Overpass.  
They have an ID consisting of a Lvl 12 Geohash and the Node Id from osm Node.  
There are 2 types of Nodes:  
one indicates the street shape and the other is an intersection.
You can recognize them by the fact that crossings have links and shapes have parent links.  
Nodes can be output as geojson and wkt.

### Links
Links are road sections between crossings.  
They have an ID consisting of a osm way Id and the start node Id.
The link contains the tags from Overpass.
Links can be output as geojson and wkt.

### Tiles
The map service groups all links and nodes into groups. These groups are the tiles.  
A Tile has a range of an [geohash](https://en.wikipedia.org/wiki/Geohash) (base32).

### Link User
The rules for using the links are defined in the Link User subclasses.  
These subclasses must have the methods can_navigate_from_start and can_navigate_to_start, which use a boolean to indicate whether the link can be used.  
Link users are currently available as drivers, cyclists and pedestrians.

## Code Example
This example load a Tile with the Geohash 'u0v970' from Overpass and print all nodes. 

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
            
## Functions
Below is a list of the basic functions.  
All functions that receive a bounding box load any needed tiles.

### Get Link(s) 

    mapService = MapService()
    
    # To get Links in an BBox
    mapService.get_links_in_bounding_box(BoundingBox.from_geohash("u0v970"))
    # returns a list with links
    
    # To get Links with osm way id
    mapService.get_links(38936691)
    # returns a list with Nodes

    # To get a single Link
    mapService.get_link(38936691, NodeId(418726074, "u0v978xvcgrt"))
    # returns a Link or None if nothing found

### Get Node(s) 
    mapService = MapService()
    
    # To get a single Node
    mapService.get_node(NodeId(418726074, "u0v978xvcgrt"))
    # returns a Node or None if nothing found

    # To get all Nodes in BBox
    mapService.get_nodes_in_bounding_box(BoundingBox.from_geohash("u0v970"))
    # returns a list with Nodes
    
###  Get Tile(s)
    mapService = MapService()
    
    # To get a Tile
    # (If not loaded the Interface will download the street data 
    # and return it as a Tile with nodes and Links.)
    mapService.get_tile("u0v970")
    # returns the Tile
    
    # To get all already loaded Tiles
    mapService.get_all_cached_tiles()
    # returns all Tiles as a dictionary with the keyword as a geohash

### Routing
    
def routing():
    mapService = MapService()

    # Init Router with Linkuser (Car, Cyclist or Pedestrian)
    router = RouterDijkstra(Car())

    # set the start link (fraction default 0, from_start_to_end default true )
    router.set_start_link(mapService.get_link(314409401, NodeId(258779029, "u0v9045fe6u1")))
    ## optional fraction (position on link: 1>= fraction >= 0)
    # router.set_start_link(mapService.get_link(314409401, NodeId(258779029, "u0v9045fe6u1")),0.0)
    ## optional fraction and position (from_start_to_end as boolean)
    # router.set_start_link(mapService.get_link(314409401, NodeId(258779029, "u0v9045fe6u1")),1.0, True)

    # set the end link (fraction default 0, from_start_to_end default true )
    router.set_end_link(mapService.get_link(25779169, NodeId(281181557, "u0v922p75804")))
    ## optional fraction (position on link: 1>= fraction >= 0)
    # router.set_end_link(mapService.get_link(25779169, NodeId(281181557, "u0v922p75804")),0.0)
    ## optional fraction and position (from_start_to_end as boolean)
    # router.set_end_link(mapService.get_link(25779169, NodeId(281181557, "u0v922p75804")),1.0, True)

    # Calculates the shortest route and returns it as a list of nodes
    result = router.compute()  # Returns a tuple with total wight and the way
    print("Way weight: ",result[0], "in", result[1])
    for link in result[2]:
        print("next Link: ", link)
        
This example calculates the route using the Dijkstra. 
The function returns a tuple with total weight, unit and the route as list with links. 
The Dijkstra also takes into account one-way streets.
    
### Distances
    
    def example():
        mapService = MapService()
        bbox = BoundingBox.from_geohash("u0v970")

    nodes = mapService.get_nodes_in_bounding_box(bbox)

    linkdists = mapService.get_linkdistances_in_radius(nodes[1].get_latlon(), 150)  # meter
    for ld in linkdists:
        print("LinkDistance: ", ld.get_distance(), "m", "Fraction: ", ld.get_fraction())

This example prints out all links with their distances around the first point (Node) in the Tile.
    
## Data Visualisation
With the code <code>rest.app.run(host="localhost", port=5000)</code> you can start a web server for visualize.
There you can display nodes, links and crossings in an specific geohash. 
Furthermore you can calculate the shortest route between two points or 
you display all links in an certain radius.

![Picture 1]


## Creator
- Lukas F.
- Sebastian L.
- Kai P.  

Supervisor:
- Prof. Beggel