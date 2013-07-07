var accessed = document.getElementById('id_accessed');
if (accessed) accessed.value = new Date();

$(function() {
  $('form').submit(function() {
    base_url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=';
    var location;
    $.ajax({
      url: base_url + encodeURIComponent($('input#id_location').val()),
      async: false,
      success: function(response) {
        location = response.results[0].geometry.location;
      }
    });
    $('<input>').attr({'type': 'hidden', 'name': 'coords', 'value': [location.lat, location.lng]}).appendTo('form');
  });
});
