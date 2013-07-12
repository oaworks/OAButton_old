var accessed = document.getElementById('id_accessed');
if (accessed) accessed.value = new Date();

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    $('#id_location').attr('required', 'true');
  }
}

function showPosition(position) {
  $('#id_coords').val([position.coords.latitude, position.coords.longitude]);
  $('#id_location').attr({'placeholder': 'Detected from browser', 'required': false, 'readonly': 'readonly'});
}

getLocation();

function addScholarLink() {
  var doi = $('#id_doi').val();

  if (doi) {
    var url = 'http://scholar.google.com/scholar?cluster=http://dx.doi.org/' + encodeURIComponent(doi);
    $('#id_scholar').attr('href', url).show();
  }
}

addScholarLink();

$(function() {
  $('form').submit(function() {
    // Do geocoding only if needed
    if ($('#id_coords').val() === "") {
      base_url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=';
      var location;
      $.ajax({
        url: base_url + encodeURIComponent($('input#id_location').val()),
        async: false,
        success: function(response) {
          location = response.results[0].geometry.location;
        }
      });
      $('#id_coords').val([location.lat, location.lng]);
    }
  });
});
