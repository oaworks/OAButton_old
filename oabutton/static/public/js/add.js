$(function() {
  $('#id_accessed').val(new Date());

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


  function parseCrossRef(entry) {
    var description = [],
        item = entry["pam:message"]["pam:article"];

    if (item["dc:title"]) {
      description.push(item["dc:title"]);
    }

    if (item["dc:creator"]) {
      if (!$.isArray(item["dc:creator"])) {
        item["dc:creator"] = [item["dc:creator"]];
      }

      description.push(item["dc:creator"].join(", "));
    }

    if (item["prism:publicationName"]) {
      description.push(item["prism:publicationName"]);
    }

    if (item["prism:publicationDate"]) {
      // TODO: zero-pad or reformat the date, using Moment.js?
      description.push(item["prism:publicationDate"]);
    }

    return description.join("\n");
  }

  function lookup() {
    var doi = $('#id_doi').val();

    if (doi) {
      $.ajax({
          url: 'http://data.crossref.org/' + encodeURIComponent(doi),
          dataType: "json",
          success: function(response) {
            if (response.feed.entry) {
              var description = parseCrossRef(response.feed.entry);
              $('#id_description').val(description);
            }
          }
      });
    }
  }

  lookup();

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
  }

  $('form').on("submit", onSubmit);
});
