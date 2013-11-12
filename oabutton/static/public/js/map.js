var map = L.map('map', {
    center: [20, 0],
    maxZoom: 18,
    minZoom: 2,
    scrollWheelZoom: false,
    touchZoom: false,
    zoom: 2
});

L.tileLayer('http://{s}.tile.cloudmade.com/cee9bfb83d854a2f89a4a2445aa9f595/997/256/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>'
        }).addTo(map);    

var oaIcon = L.icon({
    iconUrl: 'static/img/noalogo.png',
    iconSize: [12, 19],
    iconAnchor: [6, 9],
    popupAnchor: [0, -12]
});

var markers = new L.MarkerClusterGroup();
for (var i = 0; i < events.length; i++) {
    var evt = events[i];
    if(evt.coords.lat && evt.coords.lng) {
        bubble_content = '<h4>' + evt.user_name;
        if (evt.user_profession != '') {
            bubble_content += ' <em>(' + evt.user_profession + ')</em>';
        }
        bubble_content += '</h4>';
        bubble_content += '<p>' + evt.description+ '</p>';
        bubble_content += '<a target="_blank" href="http://dx.doi.org/' + evt.doi + '">doi</a>';
        bubble_content += ' | ';
        bubble_content += '<a target="_blank" href="' + evt.url + '">url</a>';
        bubble_content += ' | ';
        bubble_content += evt.accessed || '';

        var marker = new L.marker([evt.coords.lat, evt.coords.lng], { title: bubble_content, icon: oaIcon });
        marker.bindPopup(bubble_content);

        markers.addLayer(marker);
    }
}
    map.addLayer(markers);
