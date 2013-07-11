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
