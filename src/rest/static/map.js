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
            fillOpacity: 0.5,
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

function renderLinks(map, links){
    var style = {
        "color": "#ff7800",
        "weight": 5,
        "opacity": 0.65
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


var map = buildMap([49.46112, 7.76316]);
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
            geohashStart: "",
            geohashEnd:"",
            osmStart:"",
            osmEnd:""
        }
    },

    methods: {
        loaddata: function(resource) {
            that = this;
            cmds = {
               crossings: "/api/tiles/" + that.geohash + "/nodes/crossroads",
               nodes: "/api/tiles/" + that.geohash + "/nodes",
               links: "/api/tiles/" + that.geohash + "/links",
               route:  "/api/route?geofrom="+ that.router.geohashStart+
                   "&geoto="+ that.router.geohashEnd+"&osmfrom="+ that.router.osmStart+"&osmto="+that.router.osmEnd,
            }
            url = cmds[that.cmd]
            console.log(url)

            var xhr = new XMLHttpRequest();
            xhr.open('GET', url);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onload = function () {
                if (xhr.status === 200) {
                    geoData = JSON.parse(xhr.responseText);
                    that.message = geoData
                    if(that.cmd == "nodes"){
                        setView(that.map, geoData[0].geometry.coordinates)
                        renderNodes(that.map, geoData, '#ff0911')
                        that.logitems.push({line1: that.cmd + ": "+ that.geohash, line2: geoData.length, line3: that.geohash + that.cmd})
                    }
                    if(that.cmd == "crossings"){
                        setView(that.map, geoData[0].geometry.coordinates)
                        renderNodes(that.map, geoData, '#1109ff')
                        that.logitems.push({line1: that.cmd + ": "+ that.geohash, line2: geoData.length, line3: that.geohash + that.cmd})
                    }

                    if(that.cmd == "links"){

                        renderLinks(that.map, geoData)
                        that.logitems.push({line1: that.geohash, line2: geoData.length, line3: that.geohash, link: "#"})
                    }
                    if(that.cmd == "route"){
                        renderNodes(that.map, geoData, "#11ff06")
                        that.logitems.push({line1: "Route", line2: geoData.length, line3: geoData.length})
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
        }
    }
});

map.app = app;
map.on("click", function (evt) {
    console.log(evt.latlng.lng)
    map.app.linkdistance.lat = evt.latlng.lat;
    map.app.linkdistance.lon = evt.latlng.lng;
    var circle = L.circle(evt.latlng, {
            color: "yellow",
            fillColor: "yellow",
            fillOpacity: 0.5,
            radius: 4
    })
    circle.addTo(map);
})

}
