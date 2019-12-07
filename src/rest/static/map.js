/*
Description: vue.js components for map an GUI Items to controll

@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
*/

VIEW_SET = 0;
accesstoken = "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw";
providerurl = "https://api.tiles.mapbox.com/";


function buildMap(startLocation){
    var mymap = L.map('mapid').setView(startLocation, 15);

    L.tileLayer(providerurl+'v4/{id}/{z}/{x}/{y}.png?access_token='+accesstoken, {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox.streets'
    }).addTo(mymap);

    return mymap;
}

function isPosSet(pos){
    if (pos == null){
        return false;
    }
    return !(pos.lat == "" || pos.lon == "");
}


function setView(map, coords) {
    if(VIEW_SET === 0){
        map.setView(coords, 15)
        VIEW_SET = 1;
    }
}
function renderNodes(map, nodes, color){
    nodes.forEach(function (node) {

        var circle = L.circle(node["geometry"]["coordinates"], {
            color: color,
            fillColor: color,
            fillOpacity: 0.2,
            radius: 5
        })
        if(node["properties"] != undefined) {
            circle.bindPopup(node["properties"]["geohash"] + " OSM:" + node["properties"]["osm_node_id"]);
            circle.props = node["properties"];
        }
        start = false;

        circle.on("click", function (e) {
            var props = e.target.props;

            if(!start){
                map.app.router.geohashStart = props.geohash;
                map.app.router.osmStart = props.osm_node_id;
                start = true;
            }
            else{
                map.app.router.geohashEnd = props.geohash;
                map.app.router.osmEnd = props.osm_node_id;
            }
        })
        circle.addTo(map);
    });
}

function renderLinks(map, links, color){

    var style = {
        "color": color,
        "weight": 5,
        "opacity": 0.2
    };

    links.forEach(function (link) {
        var leaflet_link = L.polyline(link.geometry.coordinates, {"style": style});
        var osmid = link["properties"].start_node.id
        var nodegeohash = link["properties"].start_node.geohash
        var wayid = link["properties"].osm_way_id

        leaflet_link.bindPopup(`Way: ${wayid}\nNodehash:${nodegeohash}\nNodeId:${osmid}`)
        leaflet_link.addTo(map);
    });
}

window.onload = function(){

// Define a new component called button-counter
Vue.component('tile', {
    props:["text","id", "count"],
    data: function () { //must be function, because Vue
        return {}
    },
    template: '<div class="tile"> <span class="tile-text">{{ text }}</span> <span class="tile-nodecount">{{ count }}</span></div>'
});

Vue.component('logitem', {
    props:["line1","line2", "line3", "link"],
    data: function () { //must be function, because Vue
        return {}
    },
    template: '<div class="logitem"> ' +
        '<span class="line">{{ line1 }}</span> ' +
        '<span class="line">{{ line2 }}</span>' +
        '<span class="line">{{ line3 }}</span>' +
        '<a v-if="link" href="link"></a>'+
        '</div>'
});


map = buildMap([49.46112, 7.76316]);

var app = new Vue({
    el: '#app',
    data: {
        logitems:[],
        linkdistance:{
            lat: "", // wird zur laufzeit von der Karte von einem klick event gefüllt
            lon: ""
        },
        rootUrl: "/api/tiles/",
        currentUrl: "/nodes",
        geohash: "u0v90",
        message: "",
        map: map,
        cmd: "nodes",
        showRouting: false,
        router: {
            start: null,
            end: null
        },
        routerX: {
            start:{
             lat: "",
             lon: ""
            },
            end:{
             lat: "",
             lon: ""
            },
        }
    },

    methods: {
        loaddata: function(resource) {
            that = this;
            cmds = {
               crossings: "/api/tiles/" + that.geohash + "/nodes/crossroads",
               nodes: "/api/tiles/" + that.geohash + "/nodes",
               links: "/api/tiles/" + that.geohash + "/links",
            }


            if(that.cmd == "route") {
                cmds.route =  "/api/route?start_lat=" + that.router.start.lat +
                "&start_lon=" + that.router.start.lon + "&end_lat=" + that.router.end.lat + "&end_lon=" + that.router.end.lon
            }

            url = cmds[that.cmd]
            console.log(url)

            var xhr = new XMLHttpRequest();
            xhr.open('GET', url);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onload = function () {
                if (xhr.status === 200) {
                    geoData = JSON.parse(xhr.responseText);

                    if(geoData.hasOwnProperty("exception")){
                        console.log(geoData);
                        return
                    }
                    that.message = geoData;
                    if(that.cmd == "nodes"){
                        setView(that.map, geoData[0].geometry.coordinates)
                        renderNodes(that.map, geoData, '#ff0911')
                        that.logitems.unshift({line1: that.cmd + ": "+ that.geohash, line2: geoData.length, line3: that.geohash + that.cmd})
                    }
                    if(that.cmd == "crossings"){
                        setView(that.map, geoData[0].geometry.coordinates)
                        renderNodes(that.map, geoData, '#1109ff')
                        that.logitems.unshift({line1: that.cmd + ": "+ that.geohash, line2: geoData.length, line3: that.geohash + that.cmd})

                    }

                    if(that.cmd == "links"){

                        renderLinks(that.map, geoData, "#ff7800")
                        that.logitems.unshift({line1: that.geohash, line2: geoData.length, line3: that.geohash, link: "#"})
                    }
                    if(that.cmd == "route"){
                        renderLinks(that.map, geoData, "#11ff11")
                        that.logitems.unshift({line1: "Route", line2: geoData.length, line3: geoData.length})
                    }
                }
            };
            xhr.send();
        },
        calcLinkDist: function (resource) {
            var that = this;
            url =  "/api/linkdistance?lat="+ that.linkdistance.lat +"&lon="+ that.linkdistance.lon;
            console.log(url)
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onload = function () {
                if (xhr.status === 200) {
                    geoData = JSON.parse(xhr.responseText);
                    links = geoData.map(x => x["link"])
                    renderLinks(map, links);
                    for(i = 0 ; i < geoData.length; i++){
                        l = geoData[i];
                        that.logitems.push({line1: "Link: "+ l["link"]['properties']["start_node"]["geohash"]+" Distance:"+ l.distance + "  Fraction"+ l.fraction})
                    }
                    console.log(geoData)
                }
            }
            xhr.send();
        },
        clearRoute: function (res) {
            map.removeLayer(this.router.start)
            map.removeLayer(this.router.end)
            this.router.start = null;
            this.router.end = null;
        }
    }
});

LAST_CIRCLE = null;
map.app = app;

map.on("click", function (evt) {

    var current_lat = evt.latlng.lat;
    var current_lon = evt.latlng.lng;
    var circle = L.circle(evt.latlng, {
        color: "yellow",
        fillColor: "yellow",
        fillOpacity: 0.5,
        radius: 4
    });

    if(map.app.cmd == "route") {
        if (!isPosSet(map.app.router.start)) {
            circle.addTo(map);
            //map.app.router.start.lat = current_lat;
            //map.app.router.start.lon = current_lon;
            circle.lat = current_lat;
            circle.lon = current_lon;

            map.app.router.start = circle;

        } else if (!isPosSet(map.app.router.end)) {
            circle.addTo(map);
            //map.app.router.end.lat = current_lat;
            //map.app.router.end.lon = current_lon;
            circle.lat = current_lat;
            circle.lon = current_lon;
            map.app.router.end = circle;

        }
    }

    if (map.app.cmd == "linkdistance") {
        if (LAST_CIRCLE != null) {
            map.removeLayer(LAST_CIRCLE);
        }
        LAST_CIRCLE = circle;
        circle.addTo(map)
        map.app.linkdistance.lat = current_lat;
        map.app.linkdistance.lon = current_lon;
    }

})

}
