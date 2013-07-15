$(function() {
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

  // save details in localstorage
  function rememberDetails() {
    // test for localstorage support (from Modernizr)
    // fails if third-party data is not allowed (in an iframe)
    try {
        localStorage.setItem('test', 'test');
        localStorage.removeItem('test');
    } catch(e) {
        return;
    }

    var rememberMeInput = $('#id_remember'),
        rememberNodes = $('[data-remember]');

    var stored = localStorage.getItem('id_remember');

    // can't always store booleans in localstorage, so "false" (string) = "don't store"
    var remember = stored === null || stored === true || stored.toString() === 'true';

    if (remember) {
      rememberMeInput.prop('checked', true);
    }

    rememberMeInput.parent().show();

    // store/load details
    rememberNodes
      // save the details
      .on('change', function(){
        if (!remember) {
          return;
        }

        localStorage.setItem(this.getAttribute('id'), $(this).val());
      })
      // load the details
      .each(function() {
        $(this).val(localStorage.getItem(this.getAttribute('id')));
      });

    // when "remember me" is unchecked, delete stored details
    rememberMeInput.on('change', function() {
      remember = rememberMeInput.prop('checked');
      localStorage.setItem('id_remember', remember);

      if (remember) {
        // save the current values
        rememberNodes.trigger('change');
      } else {
        // remove the stored values
        rememberNodes.each(function() {
          localStorage.removeItem(this.getAttribute('id'));
        });
      }
    });
  }

  rememberDetails();

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
