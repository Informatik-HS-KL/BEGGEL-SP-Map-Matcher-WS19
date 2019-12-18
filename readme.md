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
4. flask

## Installation

git clone -b master https://github.com/Informatik-HS-KL/BEGGEL-SP-Map-Matcher-WS19.git

Run main.py with Conda Python Interpeter

### Installation Shapely
1. Install [Conda](https://docs.conda.io/en/latest/miniconda.html )
2. Execute <code>conda install shapely</code> in Anaconda Prompt

## Configurations

Set Your Own Config


    mapservice = MapService()
    mapservice.set_config('path/to/your/config.ini')
   
Default Configuation File you can see in Project: "src/config.ini"

In this configurations are 3 sections.
1. DEFAULT Selection  
In this selection are base parameters like overpass_url etc.
2. HIGHWAY_CARS Selection  
In this selection you can choose the loaded street types for vehicles.
By Default all street types will be loaded.  
More information about the street types you can find [here](https://wiki.openstreetmap.org/wiki/Key:highway#Special_road_types)  

 
## Models
The following paragraph discusses the data model in the Map Service

### NodeId
| Methods | Return | Description | 
| --- |--- | --- | 
| get_geohash() | str | Lvl 12, base32 Geohash like (u0v921ftzju8) | 
| get_osm_id() | int | |

### Node
Nodes are a depict of the nodes of Overpass.  
They have an ID consisting of a Lvl 12 Geohash and the Node Id from osm Node.  
There are 2 types of Nodes:  
one indicates the street shape and the other is an intersection.
You can recognize them by the fact that crossings have links and shapes have parent links.  
Nodes can be output as geojson and wkt.

| Methods | Return |Description |
| --- | --- | --- |
| get_parent_links() | list ||
| get_links() | list | Empty if Node is no start or end of link|
| get_id() | NodeId | |
| get_latlon() | tuple(lat, lon) | the exact position on map|
| get_lat() | float | |
| get_lon() | float| |
| get_tags() | dict| |
| get_osm_id() | int ||
| get_geohash() | str | Lvl 12, base32 Geohash |
| set_tag(dict) | None | Tags from overpass | 
| to_geojson() | dict | Node as geojson dic (geometry type: Point) |
| to_wkt() | str ||
| add_link(link: Link) | None ||
| add_parent_link(link: Link) |None|| 

### LinkId
| Methods | Return | Description | 
| --- |--- | --- | 
| get_start_node_id() | NodeId | |  
| get_osm_way_id() | int | |
| get_geohash() | str| Lvl 12, base32 Geohash | 


### Link
Links are road sections between crossings.  
They have an ID consisting of a osm way Id and the start node Id.
The link contains the tags from Overpass.
Links can be output as geojson and wkt.

| Methods | Return | Description |
| --- | --- | --- |
| get_bbox() | BoundingBox |returns a BoundingBox which covers the geometry of the Link |
| get_start_node() | Node | | 
| get_end_node() | Node | |
| get_links_at_start_node(user: LinkUser = None) | list | [Link, Link ,...]. Returns all outgoing links from the start-node (exclusive self). If the Linkuser is set, the outgoing Links will filter for usable   |
| get_links_at_end_node(user: LinkUser = None) | list | [Link, Link ,...]. Returns all outgoing links from the end-node (exclusive self). If the Linkuser is set, the outgoing Links will filter for usable  |
| get_tags() | dict | |
| get_id() | LinkId | Geohash in that Id ist Geohash of Startnode |
| get_way_osm_id() | int | Id given from Overpass Api|
| set_tags() | None | dict of tags from overpass api { "highway": "footway"} | 
| to_geojson() | dict | geojson like format | 
| to_wkt() | str | LINESTRING |
| get_length() | float | Returns the length of the link (in meter). |
| is_navigatable_from_start() | bool |Indicates, whether the specified user is permitted to use the link from the start-node to the end-node. |
| is_navigatable_to_start() | bool |Indicates, whether the specified user is permitted to use the link from the end-node to the start-node. | 
| get_link_segments() | list | [(lat,lon), ...]  Splits a link into segments, each consisting of two positions/coordinates.|
| get_geometry() | list | | 
| get_node_ids()| list | | 
| get_geohash() | str | Start Node Geohash |


### BoundingBox

| Methods | Return | Description | 
| --- |--- | --- |
| contains_link(link: Link) | bool | Returns True if self and the bounding box of link overlap. |
| contains_node(node: Node) | bool | Returns True if Node is located in self. |
| contains_bbox(bbox: BoundingBox) | bool | Returns True if self contains other. Remark: In case of self == other, True is returned.| 
| overlap(bbox: BoundingBox) | bool | Intersection between given BoundingBox | 
| get_bbox_from_point(pos: tuple, radius: int) | BoundingBox | static method. Returns a Bounding Box with pos as center. | 
| from_geohash(geohash: str)| BoundingBox| static method. Returns a Bounding Box which covers the Tile with the specified geohash. | 

### LinkDistance
Links that match a point in given radius.

| Methods | Return | Description | 
| --- |--- | --- |
| get_distance()| float | Returns the calculated distance between self_link and self_lat_lon. |
| get_fraction()| float | Returns the fraction as percentage, where the Link matched |
| get_link() | Link | |
| get_point() | tuple| (lat, lon)| 
 
### LinkUser
The rules for using the links are defined in the Link User subclasses.  
These subclasses must have the methods can_navigate_from_start and can_navigate_to_start, which use a boolean to indicate whether the link can be used.  
Link users are currently available as drivers, cyclists and pedestrians.

| Methods | Return | Description | 
| --- |--- | --- |
| can_navigate_from_start(link: Link) | bool|
| can_navigate_to_start(link: Link )| bool |

### Tile
The map service groups all links and nodes into groups. These groups are the tiles.  
A Tile has a range of an [geohash](https://en.wikipedia.org/wiki/Geohash) (base32).

| Methods | Return | Description | 
| --- |--- | --- |
| get_geohash() | str ||
| add_node(node) | None| | 
| add_link(link) | None||
| get_node(nid: NodeId) | Node | 
| get_link( linkid: LinkId) | Link | 
| get_node_from_osm_id(osmid: int) | Node | 
| get_nodes() | list |
| get_nodes_with_keys() | dict |
| get_links_with_keys() | dict |
| get_links() | list | 


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

### MapService 

| Methods | Return | Description | 
| --- |--- | --- |
| set_config("path/to/config.ini") | None | |
| get_config()| MapServiceConfig | Special ConfigParser Object |
| set_overpass_wrapper(opw: OverpassWrapper) | None | Default OverpassWrapperClientSide | 
| get_links(way_id: int)| list | [Link, ...] |
| get_links_in_bounding_box(BoundingBox) | list | [Link, ...] | 
| get_nodes_in_bounding_box(bbox: BoundingBox)| list | [Node, ...]|
| get_tile(geohash: str) | Tile | |
| get_link_by_id(linkid: LinkId)| Link | | 
| get_links(way_id: int) | list | [Link, ...]|
| get_linkdistances_in_radius(pos:tuple, max_dist: float)| list | [Linkdistance, ...]|
| get_node(nodeid: NodeId)| Node | |


## Examples

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
    
## Frontend 
Frontend is designed for debugging and testing of that Mapservice.
You can run ist with:

    from src.rest.app import app
    app.run(host="localhost", port=5000)


### Data Visualisation
There you can display nodes, links and crossings in an specific geohash. 
Furthermore you can calculate the shortest route between two points or 
you display all links in an certain radius.

### Used Libaries
1. Vue (https://vuejs.org/)
2. Leadlet (https://leafletjs.com/)
3. Bootstrap (https://getbootstrap.com/)
4. JQuery(for Bootstrap)

### Functions
1. Display Nodes of geohash
2. Display Links of geohash
3. Display Intersections/Crossings
4. Display Links in Linkdistance Radius
5. Route from two Points in Map

![Picture 1]

### REST-API
    /api/tiles/
    /api/tiles/stats
    /api/tiles/<geohash:str>/
    /api/tiles/<geohash:str>/nodes
    /api/tiles/<geohash:str>/nodes/<osmid>
    /api/tiles/<geohash:str>/nodes/intersections
    /api/tiles/<geohash:str>/links
    /route?start_lat=[Number]&start_lon=[Number]&end_lat=[Number]&end_lon=[Number]
    /linkdistance?lat=[Number]&lon=[Number]&radius=[Int]
    /geohashes?bbox=south,west,north,east
    /ways/<wayid>/links
    
    
    
## Creator
- Lukas F.
- Sebastian L.
- Kai P.  

Supervisor:
- Prof. Dr. Beggel