window.onload = function () {
    var map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM()
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([37.41, 8.82]),
            zoom: 4
        })
    });

    let planeSource = new ol.source.Vector()

    let planeLayer = new ol.layer.Vector({
        source: planeSource,
        style: function (feature) {
            return new ol.style.Style({
                text: new ol.style.Text({
                    font: 'bold 15px Arial, sans-serif',
                    fill: new ol.style.Fill({
                        color: 'white'
                    }),
                    text: map.getView().getZoom() >= 4 ? feature.get('name') : "",
                    textAlign: 'center',
                    offsetX: 5,
                    offsetY: -20,
                    stroke: new ol.style.Stroke({
                        color: 'black',
                        width: 3
                    })
                }),
                image: new ol.style.Icon({
                    src: "plane.png",
                    scale: 0.5,
                    rotation: feature.get("heading")
                }),
            });
        },
        declutter: false
    });

    map.addLayer(planeLayer);

    function drawplanes(planes) {
        let features = [];
        planeSource.clear();
        planes.forEach(plane => {
            if (plane.position !== null) {
                let point = new ol.Feature({
                    geometry: new ol.geom.Point(ol.proj.fromLonLat(plane.position.reverse())),
                    name: plane.callsign || plane.icao,
                    heading: plane.heading * Math.PI / 180 || 0
                });
                features.push(point);
            }
        });
        planeSource.addFeatures(features);
    }

    function updatetable(planes) {
        function card(plane) {
            let card = document.createElement("div")
            card.classList.add("card")
            card.innerHTML += "<p><b>Callsign:</b> " + (plane.callsign || "UNKNOWN") + "</p>"
            card.innerHTML += "<p><b>ICAO:</b> " + (plane.icao || "UNKNOWN") + "</p>"
            card.innerHTML += "<p><b>Speed:</b> " + (plane.speed || "...") + "km/h</p>"
            card.innerHTML += "<p><b>Altitude:</b> " + (plane.altitude || "...") + "m</p>"
            card.innerHTML += "<p><b>Cat:</b> " + (plane.category || "UNKNOWN") + "</p>"
            let now = Math.round(+new Date()/1000);
            card.innerHTML += "<p>Last seen: " + (now - plane.time) + " seconds ago</p>"
            return card
        }

        let sidebar = document.getElementById("sidebar")
        sidebar.innerHTML = ""

        planes.forEach(plane => {
            sidebar.appendChild(card(plane))
        })
    }

    function frame() {
        fetch("http://localhost:8080").then(r => r.json()).then(planes => {
            drawplanes(planes)
            updatetable(planes)
            window.setTimeout(frame, 500)
        })
    }

    frame()
}