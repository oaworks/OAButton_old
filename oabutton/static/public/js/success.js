$(function() {

  function addPubMedCentralLink() {
    var doi = $('body').data('doi');

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
            // $("#id_pmc").attr("href", url).show();
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

  addPubMedCentralLink();

  function addScholarLink() {
    var doi = $('body').data('doi');

    if (doi) {
      var url = 'http://scholar.google.com/scholar?cluster=' + encodeURIComponent('http://dx.doi.org/' + doi);
      //$('#id_scholar').attr('href', url).show();
      var sch_link = document.createElement("a");
      sch_link.setAttribute("href", url);
      sch_link.setAttribute("target", "_blank");
      sch_link.innerHTML = "Search with Google Scholar";

      var li = document.createElement("li");
      li.appendChild(sch_link);

      $("#oa_links").append(li);
    }
  }

  addScholarLink();

});
