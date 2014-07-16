$(function() {

  function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition, denyAccess);
    }
  }

  function showPosition(position) {
    rounded_lat = Math.round(position.coords.latitude * 10) / 10;
    rounded_long = Math.round(position.coords.longitude * 10) / 10;
    $('#id_coords').val([rounded_lat, rounded_long]);
    $('#id_location').attr({'placeholder': 'Detected from browser', 'required': 'false', 'readonly': 'readonly'});
  }

  function denyAccess(error) { 
    if (error.code == error.PERMISSION_DENIED)
        console.log("Geolocation denied");
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
            tool: "oabutton"
          },
          dataType: "xml",
          success: function(response) {
            if (response.getElementsByTagName('Count')[0].textContent === '0') {
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

  function parseCrossRef(item) {
    var description = {};

    if (item.title) {
      description['Title'] = item.title;
    }

    if (item.author) {
      if (!$.isArray(item.author)) {
        item.author = [item.author];
      }

      var authors = [];
      $.each(item.author, function(index, author) {
        var name = [author.given, author.family];
        authors.push(name.join(" "));
      });

      description['Authors'] = authors.join(", ");
    }

    if (item["container-title"]) {
      description['Journal'] = item["container-title"];
    }

    if (item.issued && item.issued["date-parts"]) {
      // TODO: zero-pad or reformat the date, using Moment.js?
      description['Date'] = item.issued["date-parts"][0].join("-");
    }

    description = $.map(description, function(value, key) {
      return key + ": " + value;
    });

    return description.join("\n");
  }

  function lookup() {
    var doi = $('#id_doi').val();

    if (doi) {
      $.ajax({
          url: '/api/xref_proxy/' + encodeURIComponent(doi),
          dataType: "json",
          success: function(response) {
            if (response && response.URL) {
              $('#id_description').val(parseCrossRef(response));
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

  function geocode(form) {
    // Geolocation is optional
    if ($('#id_location').val() == "")
      return false;

    // Geocode the location if provided
    return $.ajax({
      url: 'https://maps.googleapis.com/maps/api/geocode/json',
      data: {
        sensor: 'false',
        address: $('#id_location').val()
      },
      success: function(response) {
        if (response.results.length == 0) {
          alert("You location could not be identified, please try again!");
        } else {
          var location = response.results[0].geometry.location;
          $('#id_coords').val([location.lat, location.lng]);
          form.submit();
        }
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log(jqXHR, textStatus, errorThrown);
        // Unable to geocode; clear form and submit
        $('#id_location').val('');
        form.submit();
      }
    });
  }

  function onSubmit(event) {
    var form = $(this);

    // Do geocoding only if needed
    if (!$('#id_coords').val())
      if (geocode(form) !== false)
        event.preventDefault();
  }

  $('#id_accessed').val(new Date().toISOString());
  $('form').on("submit", onSubmit);
});
