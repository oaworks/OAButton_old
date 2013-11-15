$(function() {

  function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } else {
      $('#id_location').attr('required', 'true');
    }
  }

  function showPosition(position) {
    rounded_lat = Math.round(position.coords.latitude * 10) / 10;
    rounded_long = Math.round(position.coords.longitude * 10) / 10;
    $('#id_coords').val([rounded_lat, rounded_long]);
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
       if (response.results.length == 0) {
           // Something went wrong with the reponse from google maps -
           // just hardcode a 0,0 co-ordinate here
           $('#id_coords').val([0, 0]);
       } else {
           var location = response.results[0].geometry.location;
           $('#id_coords').val([location.lat, location.lng]);
       }
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
  }

  $('#id_accessed').val(new Date().toISOString());
  $('form').on("submit", onSubmit);
});
