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
      if(events[i].coords.lat && events[i].coords.lng) {
        bubble_content = '<h4>' + events[i].name;
        if (events[i].profession != '') {
          bubble_content += ' <em>(' + events[i].profession + ')</em>';
        }
        bubble_content += '</h4>';
        bubble_content += '<p>' + events[i].story + '</p>';
        bubble_content += '<a target="_blank" href="http://dx.doi.org/' + events[i].doi + '">doi</a>';
        bubble_content += ' | ';
        bubble_content += '<a target="_blank" href="' + events[i].url + '">url</a>';
        bubble_content += ' | ';
        bubble_content += events[i].calendar_date || '';

        var marker = new L.marker([events[i].coords.lat, events[i].coords.lng], { title: bubble_content, icon: oaIcon });
        marker.bindPopup(bubble_content);

        markers.addLayer(marker);
      }
    }
    map.addLayer(markers);