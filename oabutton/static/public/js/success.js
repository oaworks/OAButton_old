// This is just for successful submission to generate the xref links
var oabSuccess = (function($) {

  function parseCrossRef(entry, doi) {
    var metadata = {'doi': doi},
        item = entry["pam:message"]["pam:article"];

    if (item["dc:title"]) {
      metadata["title"] = item["dc:title"];
    }

    if (item["dc:creator"]) {
      if (!$.isArray(item["dc:creator"])) {
        item["dc:creator"] = [item["dc:creator"]];
      }

      metadata["authors"] = item["dc:creator"].join(", ");
    }

    if (item["prism:publicationName"]) {
      metadata["publication"] = item["prism:publicationName"];
    }

    if (item["prism:publicationDate"]) {
      // TODO: zero-pad or reformat the date, using Moment.js?
      metadata["date"] = item["prism:publicationDate"];
    }

    return metadata;
  }

  function lookupCrossRef() {
    var doi = $('body').data('doi');

    if (doi) {
      $.ajax({
          url: '/api/xref_proxy_simple/' + encodeURIComponent(doi),
          dataType: "json",
          success: function(response) {
            if (response.feed.entry) {
              var metadata = parseCrossRef(response.feed.entry, doi);

              addPubMedCentralLink(metadata);
              addScholarDOILink(metadata);
              addScholarTitleLink(metadata);
              discoverCORELinks(metadata);
            }
          }
      });
    }
  }

  function addPubMedCentralLink(metadata) {
    var doi = metadata["doi"];

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
            var pmc_link = document.createElement("a");
            pmc_link.setAttribute("class", "likeabutton btn btn-primary btn-block")
            pmc_link.setAttribute("href", url);
            pmc_link.setAttribute("target", "_blank");
            pmc_link.innerHTML = "View on PubMedCentral";


            $("#pmc_links").append(pmc_link);
          }
      });
    }
  }

  function addScholarDOILink(metadata) {
    var doi = metadata["doi"];

    if (doi) {
      var url = 'http://scholar.google.com/scholar?cluster=' + encodeURIComponent('http://dx.doi.org/' + doi);

      var sch_link = document.createElement("a");
      sch_link.setAttribute("class", "btn btn-primary btn-block")
      sch_link.setAttribute("href", url);
      sch_link.setAttribute("target", "_blank");
      sch_link.innerHTML = "Search Google Scholar by DOI";

      $("#google_links").append(sch_link);
    }
  }

  function addScholarTitleLink(metadata) {
    var title = metadata["title"];

    if (title) {
      var url = 'http://scholar.google.com/scholar?as_occt=title&as_q=' + encodeURIComponent(title);

      var sch_link = document.createElement("a");
      sch_link.setAttribute("class", "btn btn-primary btn-block")
      sch_link.setAttribute("href", url);
      sch_link.setAttribute("target", "_blank");
      sch_link.innerHTML = "Search Google Scholar by title";

      $("#google_links").append(sch_link);
    }
  }

  function discoverCORELinks(metadata) {
    var title = metadata["title"];

    if (title) {
      $.ajax({
        url: "/metadata/coresearch.json/title:(" + encodeURIComponent(title) + ")",
        dataType: 'json',
        success: function(response) {
          var records = response.ListRecords;
	  var total_hits = records[0].total_hits;

	  if (total_hits > 0) {
            var $list = $('<ul></ul>');
            for (var i = 1; i < records.length; i++) {
              metadata = records[i]['record']['metadata']['oai_dc:dc'];
              $list.append('<li><a target="_blank" href="'
                           + metadata['dc:identifier']
                           + '">'
                           + metadata['dc:creator']
                           + ' (' + metadata['dc:date'] + '); '
                           + metadata['dc:title']
                           + '</a></li>');
            }

            $core_div  = $('<div id="core_results">' + total_hits + ' matches from the <a href="http://core.kmi.open.ac.uk/">CORE</a> repository:</div>');
            $core_div.append($list);
            $("#core_links").append($core_div);
	  } else { // no hits
	    var $core_div = $('<div id="core_results">No matches from the <a href="http://core.kmi.open.ac.uk/">CORE</a> repository.</div>');
	    $("#core_links").append($core_div);
	  }
        }
      });
    }
  }

  return {
    parseCrossRef: parseCrossRef,
    lookupCrossRef: lookupCrossRef,
    addScholarDOILink: addScholarDOILink,
    addScholarTitleLink: addScholarTitleLink,
    discoverCORELinks: discoverCORELinks,
  };

})(jQuery);


$(document).ready(function() {
  oabSuccess.lookupCrossRef();
});
