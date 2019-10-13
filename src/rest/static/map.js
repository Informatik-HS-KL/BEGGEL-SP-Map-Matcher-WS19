

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
            radius: 8
        }).addTo(map);
    });
}


function renderLinks(map, links){
    nodes.forEach(function (link) {
        var circle = L.circle(link["coordinates"], {
            color: 'red',
            fillColor: '#ff0911',
            fillOpacity: 0.5,
            radius: 8
        }).addTo(map);
    });
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
                    renderNodes(that.map, geoData)
                    that.tiles.push({text: that.geohash, count: geoData.length, id: that.geohash})
                }
            };
            xhr.send();

        }
    }
});

}
