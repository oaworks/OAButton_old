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
          url: 'http://data.crossref.org/' + encodeURIComponent(doi),
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
            pmc_link.setAttribute("href", url);
            pmc_link.setAttribute("target", "_blank");
            pmc_link.innerHTML = "View on PubMedCentral";

            var li = document.createElement("li");
            li.appendChild(pmc_link);

            $("#oa_links").append(li);
          }
      });
    }
  }

  function addScholarDOILink(metadata) {
    var doi = metadata["doi"];

    if (doi) {
      var url = 'http://scholar.google.com/scholar?cluster=' + encodeURIComponent('http://dx.doi.org/' + doi);

      var sch_link = document.createElement("a");
      sch_link.setAttribute("href", url);
      sch_link.setAttribute("target", "_blank");
      sch_link.innerHTML = "Google Scholar search (DOI)";

      var li = document.createElement("li");
      li.appendChild(sch_link);

      $("#oa_links").append(li);
    }
  }

  function addScholarTitleLink(metadata) {
    var title = metadata["title"];

    if (title) {
      var url = 'http://scholar.google.com/scholar?as_occt=title&as_q=' + encodeURIComponent(title);

      var sch_link = document.createElement("a");
      sch_link.setAttribute("href", url);
      sch_link.setAttribute("target", "_blank");
      sch_link.innerHTML = "Google Scholar search (title)";

      var li = document.createElement("li");
      li.appendChild(sch_link);

      $("#oa_links").append(li);
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

	  $li = $('<li>Matches from CORE repository:</li>');
	  $li.append($list);
	  $("#oa_links").append($li);
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
