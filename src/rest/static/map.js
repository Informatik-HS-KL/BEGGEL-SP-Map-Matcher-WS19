

function buildMap(startLocation){
    var mymap = L.map('mapid').setView(startLocation, 13);

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
    console.log("Document loaded")
    var loc = [49.46112, 7.76316]
    map = buildMap(loc);


    function load(evt) {
        var xhr = new XMLHttpRequest();
        inputs = getUserInputs()

        url = 'tiles/'+ inputs.geoHash +'/nodes'
        if(inputs.onlyCrossRoads){
            url = 'tiles/'+ inputs.geoHash +'/nodes/crossroads';
        }

        xhr.open('GET', url);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
            if (xhr.status === 200) {
                geoData = JSON.parse(xhr.responseText);
                renderNodes(map, geoData);
            }
        };
        xhr.send();
    }
    document.getElementById("form-tile-load").onsubmit = function (evt){ evt.preventDefault();load()}
    document.getElementById("btn-submit-tile").onclick = load


}