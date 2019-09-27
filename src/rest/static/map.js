

function buildMap(startLocation){
    var mymap = L.map('mapid').setView(startLocation, 10);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox.streets'
    }).addTo(mymap);

    var marker = L.marker(startLocation).addTo(mymap);
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


function getUserInputs(){
    geoHash = document.getElementById("input-tile").value
    onlyCrossRoads = document.getElementById("input-only-crossroads").checked
    return { "geoHash": geoHash, "onlyCrossRoads": onlyCrossRoads};
}

window.onload = function() {
    function TileInfo(geoHash, nodeCount){
        this.props = {
            "nodeCount": { title: "Anzahl Nodes", val: nodeCount},
            "geoHash": { title: "Kachel", val: geoHash}
        }
    }

    TileInfo.prototype.render = function () {
        wrapper = document.createElement("div")
        wrapper.className = "tileinfo";
        for(var i in this.props){
            div = document.createElement("div");
            span = document.createElement("span");
            span.textContent = this.props[i].title + " "+ this.props[i].val;
            div.appendChild(span)
            wrapper.appendChild(div);
        }
        return wrapper;
    }


    function renderInfos(map, nodes, inputs) {
        // wrapper = document.getElementById("output");
        // var nodecount = document.createElement("span")
        // nodecount.textContent = "Nodes:"+ nodes.length;
        // wrapper.appendChild(nodecount)

        container = document.getElementById("output")
        container.appendChild(new TileInfo(inputs.geoHash, nodes.length).render());

    }

    console.log("Document loaded")
    var loc = [49.46112, 7.76316]
    map = buildMap(loc);


    function load(evt) {
        var xhr = new XMLHttpRequest();
        inputs = getUserInputs()
        root_url = "/api/tiles/"
        url = root_url + inputs.geoHash +'/nodes'
        if(inputs.onlyCrossRoads){
            url = root_url + inputs.geoHash +'/crossroads';
        }

        xhr.open('GET', url);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
            if (xhr.status === 200) {
                geoData = JSON.parse(xhr.responseText);
                renderNodes(map, geoData);
                renderInfos(map, geoData, inputs);
            }
        };
        xhr.send();
    }
    document.getElementById("form-tile-load").onsubmit = function (evt){ evt.preventDefault();load()}
    document.getElementById("btn-submit-tile").onclick = load


}