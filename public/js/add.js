$('#id_accessed').val(new Date());

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

function geocode() {
  return $.ajax({
    url: 'http://maps.googleapis.com/maps/api/geocode/json',
    data: {
      sensor: 'false',
      address: $('#id_location').val()
    },
    success: function(response) {
      var location = response.results[0].geometry.location;
      $('#id_coords').val([location.lat, location.lng]);
    }
  });
}

function onSubmit(event) {
  var form = $(this);

  // Do geocoding only if needed
  if (!$('#id_coords').val()) {
    event.preventDefault();
    geocode().then(function() {
      form.submit();
    });
  }
};

$('form').on("submit", onSubmit);
