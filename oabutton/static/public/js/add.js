$(function() {

  function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    }
  }

  function showPosition(position) {
    rounded_lat = Math.round(position.coords.latitude * 10) / 10;
    rounded_long = Math.round(position.coords.longitude * 10) / 10;
    $('#id_coords').val([rounded_lat, rounded_long]);
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
          url: 'https://data.crossref.org/' + encodeURIComponent(doi),
          headers: {
            Accept: "application/vnd.citationstyles.csl+json"
          },
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
