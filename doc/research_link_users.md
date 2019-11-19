# Researches to different kinds of link users

## Pedestrian
+ is permitted to use links, which satisfy **one** of the following criteria:
    + `highway == residential` && `foot != no`
	+ `highway=living_street` && `foot != no`   &#8594; **Remark:** `foot == no` does not appear very often in this constellation.
	+ `highway == pedestrian` 
	+ `highway == footway`
	+ `highway == bridleway` && `foot != no`
	+ `highway == path` && `foot != no`
	+ `highway == steps`
	+ (`sidewalk == both` || `sidewalk == left` || `sidewalk == right`)  && `foot != no`   &#8594; **Remark:** `foot == no` does not appear very often in this constellation.
	+ `foot == yes` 
	+ `foot == designated`	
	+ `foot == permissive`

+ relevant information to oneways for pedestrians:
    + The `oneway`-tag does not refer to pedestrians. Instead you have to look out for the `oneway:foot`-tag:
        + `oneway:foot == yes` &#8594; oneway from start- to end-node
        + `oneway:foot == -1` &#8594; oneway from end- to start-node
        + `oneway:foot == no`   
	

## Cyclist
+ is permitted to use links, which satisfy **one** of the following criteria:
    + `highway == residential` && `bicycle != no`
    + `bicycle == yes` || `bicycle == designated` || `bicycle == use_sidepath` || `bicycle == permissive` || `bicycle == destination`
    + `highway == cycleway`
    + `cycleway != None` && `cycleway != no`
    + `highway == bridleway` && `bicycle != no`
    + `highway == path` && `bicycle != no`
    + `bicycle_road == yes`
    + `cyclestreet == yes`
    + `highway == steps` && `ramp:bicycle == yes`
    + `cycleway:left/right/both != None`

+ relevant information to oneways for cyclists:
    + `oneway == yes` &#8594; oneway from start- to end-node
    + `oneway == -1` &#8594; oneway from end- to start-node
    + `oneway == no`
    + **Remark**: Exceptions can be expressed with the tag `oneway:bicycle`.
    
    
## Car
+ is permitted to use links, which satisfy **one** of the following criteria:
    + `highway == motorway`
    + `highway == trunk`
    + `highway == primary`      
    + `highway == secondary`		
    + `highway == tertiary`		
    + `highway == unclassified` && `motor_vehicle != no` && `motorcar != no`		
    + `highway == residential` && `motor_vehicle != no` && `motorcar != no`
    + `highway == motorway_link`
    + `highway == trunk_link`
    + `highway == primary_link`
    + `highway == secondary_link`
    + `highway == tertiary_link` 
    + `highway=living_street` && `motor_vehicle != no` && `motorcar != no`
    + `motor_vehicle == yes`
    + `motorcar == yes`
    + **Remark:** Maybe the following tags should be considered too:
        + `highway == service`
        + `highway == track`
        
+ relevant information to oneways for cars:
    + `highway == motorway` implies `oneway=yes`
    + `highway == trunk` implies `oneway=yes`   &#8594; **Remark:** `oneway=no` or `oneway=-1` do not appear very often in this constellation.
    + `oneway == yes` &#8594; oneway from start- to end-node
    + `oneway == -1` &#8594; oneway from end- to start-node
    + `oneway == no`
