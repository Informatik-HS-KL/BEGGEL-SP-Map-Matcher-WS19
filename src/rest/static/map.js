/*
Description: vue.js components for map an GUI Items to controll

@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
*/

accesstoken = "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw";
providerurl = "https://api.tiles.mapbox.com/";

function buildMap(startLocation){
    var mymap = L.map('mapid').setView(startLocation, 10);

    L.tileLayer(providerurl+'v4/{id}/{z}/{x}/{y}.png?access_token='+accesstoken, {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox.streets'
    }).addTo(mymap);

    return mymap;
}

function renderNodes(map, nodes){
    nodes.forEach(function (node) {
        var circle = L.circle(node["coordinates"], {
            color: 'red',
            fillColor: '#ff0911',
            fillOpacity: 0.5,
            radius: 5
        })
        circle.bindPopup(node["info"]["geohash"]+ " OSM:"+ node["info"]["osmid"])
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
    console.log("Ok")

}


window.onload = function(){


// Define a new component called button-counter
Vue.component('tile', {
    props:["text","id", "count"],
    data: function () { //must be function, because Vue
        return {
        }
    },
    template: '<div class="tile"> <span class="tile-text">{{ text }}</span> <span class="tile-nodecount">{{ count }}</span></div>'
})


var loc = [49.46112, 7.76316]
map = buildMap(loc);

var app = new Vue({
    el: '#app',
    data: {
        tiles:[],
        rootUrl: "/api/tiles/",
        currentUrl: "/nodes",
        geohash: "u0v97",
        message: "",
        map: map,
        cmd: "nodes",
    },

    methods: {

        loaddata: function(resource) {
            that = this;
            cmds = {
               nodes: "/api/tiles/" + that.geohash + "/nodes",
               links: "/api/tiles/" + that.geohash + "/links",
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
                        renderNodes(that.map, geoData)
                    }
                    if(that.cmd == "links"){
                        renderLinks(that.map, geoData)
                    }
                    that.tiles.push({text: that.geohash, count: geoData.length, id: that.geohash})
                }
            };
            xhr.send();

        }
    }
});


}
