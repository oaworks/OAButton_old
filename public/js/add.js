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

function pmc() {
  var doi = $('#id_doi').val();

  if (doi) {
    $.ajax({
        url: 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
        data: {
          db: "pmc",
          retmax: 1,
          term: doi + "[DOI]",
          tool: "oabutton",
        },
        dataType: "xml",
        success: function(response) {
          if (response.getElementsByTagName('Count')[0].textContent == 0) {
            return;
          }

          var pmcid = response.getElementsByTagName('Id')[0].textContent;
          var url = "http://www.ncbi.nlm.nih.gov/pmc/articles/PMC" + pmcid + "/";
          $("#id_pmc").attr("href", url).show();
        }
    });
  }
}

pmc();

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
