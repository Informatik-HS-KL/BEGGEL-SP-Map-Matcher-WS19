[Picture 1]: doc/images/webPage.jpg  "Visualisation of Links and Nodes"
# Map Service
## Overview

### Functions

#### Get Link(s)
Links in BBox
Return a Dictionary with Links:

    mapService.get_links_in_bounding_box(BoundingBox(south: float, 
                                                     west:  float, 
                                                     north: float, 
                                                     east:  float))
   

Links with osm way id:
Return a Dictionary with Links:

    mapService.get_links(38936691)

Links around a Point

#### Get Node(s)
Node by Id

Nodes in BBox

#### Get Tile(s)
Tile with geohash

All Cached Tiles

### GUI
After the start you have the opportunity to Visual your Links and Nodes. 
We implement a test web page under [localhost](http://http://localhost:5000/). 
![Picture 1]

In the Visualisation you can choose if you want to see all Nodes or Links in a Geohash.
Set Nodes and Links are preserved.

### Requirements

1. Python: 3.7
2. ...

### Installation
Actual:
1. Copy/download code
2. run man

## Support
xxx