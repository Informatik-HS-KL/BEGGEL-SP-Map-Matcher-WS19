[Picture 1]: doc/images/webPage1.jpg  "Visualisation of Links and Nodes"
[Picture 2]: doc/images/webPage.jpg  "Visualisation of Routing"
[Picture 3]: doc/images/webPage3.jpg  "Visualisation of Link Distance"

# Map Service
MapService is a Python Library which encapsulates both the download of OpenStreetMap-Data 
(via [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)) and the convertion of 
this data into a own data model. Furthermore the MapService offers some advanced functionality,
such as routing or the determination of streets within a certain radius. Besides that the 
MapService offers a web frontend which visualizes most of the current functionality. This provides
an easier introduction into the work with the MapService.

## Requirements
1. Python 3.7 [(download)](https://www.python.org/downloads/)
2. shapely
3. geohash2
4. flask

## Installation Linux Ubuntu 18 LTS

    sudo apt-get install python3.7

    python3.7 -m pip install shapely
    python3.7 -m pip install geohash2
    python3.7 -m pip install flask

    git clone -b master https://github.com/Informatik-HS-KL/BEGGEL-SP-Map-Matcher-WS19.git

    cd BEGGEL-SP-Map-Matcher-WS19

    python3.7 main.py

## Installation Windows
1. Install Python 3.7 and Miniconda 

    Python:    https://www.python.org/downloads/
    
    Miniconda: https://docs.conda.io/en/latest/miniconda.html

2. Download and install packages with pip and conda commands:

        pip install geohash2
        pip install flask
        conda install shapely

3. Download projekt:

        git clone -b master https://github.com/Informatik-HS-KL/BEGGEL-SP-Map-Matcher-WS19.git

4. Run main.py with Conda Python Interpeter (default: user dir / miniconda)

### Installation Shapely
1. Install [Conda](https://docs.conda.io/en/latest/miniconda.html )
2. Execute <code>conda install shapely</code> in Anaconda Prompt

## Configurations

Set Your Own Config


    mapservice = MapService()
    mapservice.set_config('path/to/your/config.ini')
   
Default Configuation File you can see in Project: "src/config.ini"

In this configurations are 3 sections.
1. DEFAULT Section  
In this section are base parameters like overpass_url etc.
2. HIGHWAY_CARS Section  
In this section you can choose the loaded street types for vehicles.
By Default all street types will be loaded.  
More information about the street types you can find [here](https://wiki.openstreetmap.org/wiki/Key:highway#Special_road_types).  

 
## Models
The following paragraph discusses the data model of the MapService.

### NodeId
A NodeId-Object consists of a OSM-Node-Id and a geohash. It offers the following methods:

| Methods | Return | Description | 
| --- |--- | --- | 
| get_geohash() | str | Lvl 12, base32 Geohash like (u0v921ftzju8) | 
| get_osm_id() | int | |

### Node
A Node basically wraps the information of a OSM-Node. Besides that it offers some  
useful methods shown in the following table: 

| Methods | Return |Description |
| --- | --- | --- |
| get_parent_links() | list ||
| get_links() | list | Empty if Node is no start or end of link|
| get_id() | NodeId | |
| get_latlon() | tuple(lat, lon) | |
| get_lat() | float | |
| get_lon() | float| |
| get_tags() | dict| |
| get_osm_id() | int ||
| get_geohash() | str | Lvl 12, base32 Geohash |
| set_tag(dict) | None | | 
| to_geojson() | dict | Returns the geojson representation of the Node. |
| to_wkt() | str ||
| add_link(link: Link) | None ||
| add_parent_link(link: Link) |None|| 

### LinkId
A LinkId-Object consists of a OSM-Way-Id, a geohash and the NodeId of the start-node of the corresponding 
link. It offers the following methods:

| Methods | Return | Description | 
| --- |--- | --- | 
| get_start_node_id() | NodeId | |  
| get_osm_way_id() | int | |
| get_geohash() | str| Lvl 12, base32 Geohash | 


### Link
A Link is a part of a street which (if at all) has only intersections at the beginning and/or 
 the end. The tag-information of a Link is obtained from the corresponding OSM-Way.  
 Just like Nodes, Links offer some useful methods shown in the following table:

| Methods | Return | Description |
| --- | --- | --- |
| get_bbox() | BoundingBox |Returns a BoundingBox which covers the geometry of the Link. |
| get_start_node() | Node | | 
| get_end_node() | Node | | 
| get_links_at_start_node(user: LinkUser = None) | list | [Link, Link ,...]. Returns all outgoing links from the start-node (exclusive self). If the Linkuser is set, the outgoing Links will be filtered accordingly.   |
| get_links_at_end_node(user: LinkUser = None) | list | [Link, Link ,...]. Returns all outgoing links from the end-node (exclusive self). If the Linkuser is set, the outgoing Links will filtered accordingly.  |
| get_tags() | dict | |
| get_id() | LinkId | |
| get_way_osm_id() | int | Returns the OSM-Id of the correspondig OSM-Way.|
| set_tags() | None | dict of tags { "highway": "footway"} | 
| to_geojson() | dict | geojson like format (geometry type: LineString)| 
| to_wkt() | str | LINESTRING |
| get_length() | float | Returns the length of the link (in meter). |
| is_navigatable_from_start() | bool |Indicates, whether the specified user is permitted to use the link from the start-node to the end-node. |
| is_navigatable_to_start() | bool |Indicates, whether the specified user is permitted to use the link from the end-node to the start-node. | 
| get_link_segments() | list | [(lat,lon), ...]  Splits a link into segments, each consisting of two positions/coordinates.|
| get_geometry() | list | [(lat, lon), ...] Returns all Node positions in Link.| 
| get_node_ids()| list | [NodeId, ...] Returns all Nodes in Link.| 
| get_geohash() | str | Returns the geohash of the start-node of the Link. |


### BoundingBox

| Methods | Return | Description | 
| --- |--- | --- |
| contains_link(link: Link) | bool | Returns True if self and the BoundingBox of link overlap. |
| contains_node(node: Node) | bool | Returns True if Node is located in self. |
| contains_bbox(bbox: BoundingBox) | bool | Returns True if self contains other. Remark: In case of self == other, True is returned.| 
| overlap(bbox: BoundingBox) | bool | Returns True if self and bbox overlap. | 
| get_bbox_from_point(pos: tuple, radius: int) | BoundingBox | Returns a BoundingBox with pos as center. | 
| from_geohash(geohash: str)| BoundingBox| Returns a Bounding Box which covers the Tile with the specified geohash. | 

### LinkDistance
Sometimes you want to find links within a certain radius around a certain position. In this context it
is usually interesting to get further information about a link that was found. A LinkDistance-Object encapsulates all
these information and offers the following methods:

| Methods | Return | Description | 
| --- |--- | --- |
| get_distance()| float | Returns the calculated distance between the link and the point. |
| get_fraction()| float | Returns the fraction as percentage, where the Link matched. |
| get_link() | Link | |
| get_point() | tuple| | 
 
### LinkUser
The rules for using the links are defined in the subclasses of LinkUser.  
These subclasses must implement the methods can_navigate_from_start() and can_navigate_to_start() (shown in the table below).
Currently LinkUser has the three subclasses Pedestrian, Cyclist and Car.

| Methods | Return | Description | 
| --- |--- | --- |
| can_navigate_from_start(link: Link) | bool | Indicates whether link can be used from the start-node to the end-node by this link-user.|
| can_navigate_to_start(link: Link )| bool |  Indicates whether link can be used from the end-node to the start-node by this link-user.|

### Tile
The map service groups all Nodes and Links into Tiles.   
A Tile has a range of an [geohash](https://en.wikipedia.org/wiki/Geohash) (base32).

| Methods | Return | Description | 
| --- |--- | --- |
| get_geohash() | str | Level 5 Geohash 32 Bit|
| add_node(node) | None| Adds Node to Tile. Warning! Don't Change the Datamodel, when you don't know what you're doing. This Methods are used in OverpassWrapper to build the Graph.| 
| add_link(link) | None| Adds Link to Tile Warning! Don't Change the Datamodel, when you don't know what you're doing This Methods are used in OverpassWrapper to build the Graph.|
| get_node(nid: NodeId) | Node | Get Node Object from this Tile. Better use get_link from MapService|  
| get_link( linkid: LinkId) | Link | get Link Object from this Tile. Better use get_link from MapService|
| get_node_from_osm_id(osmid: int) | Node | return Node from osm_id from Overpass Api|
| get_nodes() | list | All Nodes from one Tile|
| get_nodes_with_keys() | dict | {NodeId: Node, ...}| 
| get_links() | list | All Nodes from one Tile|
| get_links_with_keys() | dict | {NodeId: Node, ...}|



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
    
    
    
## Creators
- Lukas Felzmann
- Sebastian Leilich
- Kai Plautz 

Supervisor:
- Prof. Dr. Beggel

## Licenses
Data from <a href="http://www.openstreetmap.org/">OpenStreetMap</a> - published under <a href="http://opendatacommons.org/licenses/odbl/">ODbL</a>.
