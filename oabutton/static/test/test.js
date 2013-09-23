module("success.js", {
  setup: function() {
    this.doi = "10.1038/nrrheum.2013.47";
    this.metadata = {
      doi: this.doi,
      title: "Acute inflammatory arthritis: Monoarthritis risk stratification in Lyme disease",
      authors: "Robert T. Schoen",
      publication: "Nature Reviews Rheumatology",
      date: "2013-4-9",
    };
  },
});

test( "parseCrossRef", function() {
  var entry = {"title":"Acute inflammatory arthritis: Monoarthritis risk stratification in Lyme disease","link":{"href":"http://dx.doi.org/10.1038%2Fnrrheum.2013.47"},"id":"http://dx.doi.org/10.1038/nrrheum.2013.47","updated":"2013-09-23T06:07:17-04:00","content":{"div":{"p":[{"b":"Acute inflammatory arthritis: Monoarthritis risk stratification in Lyme disease"},"\n\tNature Reviews Rheumatology. \n\t<ahref=\"http://dx.doi.org/10.1038%2Fnrrheum.2013.47\">10.1038/nrrheum.2013.47</a>","\n\tAuthors:\n\t\n\t\n\tRobert T. Schoen\n\t\n\t\n\t\n      "],"xmlns":"http://www.w3.org/1999/xhtml"},"type":"xhtml"},"pam:message":{"pam:article":{"xhtml:head":{"xmlns:xhtml":"http://www.w3.org/1999/xhtml"},"dc:identifier":"10.1038/nrrheum.2013.47","dc:title":"Acute inflammatory arthritis: Monoarthritis risk stratification in Lyme disease","dc:publisher":"Nature Publishing Group","dc:isPartOf":"1759-4790","prism:alternateTitle":"Nature Reviews Rheumatology","dc:creator":"Robert T. Schoen","prism:publicationName":"Nature Reviews Rheumatology","prism:issn":"1759-4790","prism:eIssn":"1759-4804","prism:doi":"10.1038/nrrheum.2013.47","prism:publicationDate":"2013-4-9","prism:volume":"9","prism:startingPage":"261","prism:endingPage":"262","prism:url":"http://dx.doi.org/10.1038%2Fnrrheum.2013.47"},"xmlns:pam":"http://prismstandard.org/namespaces/pam/2.0/","xsi:schemaLocation":"http://prismstandard.org/namespaces/pam/2.0/ \n\t\t\t\t   http://www.prismstandard.org/schemas/pam/2.1/pam.xsd"}};

  var result = oabSuccess.parseCrossRef(entry, this.doi);

  deepEqual(result, this.metadata, "Parses data correctly");
});

test( "addScholarDOILink", function() {
  var $fixture = $('#qunit-fixture');
  $fixture.append('<ul id="oa_links"></ul>');

  oabSuccess.addScholarDOILink(this.metadata);

  var link = $("a", $fixture);
  equal(link.length, 1, "Only one link added");
  ok(link.attr('href').indexOf('scholar.google.com') > -1, "Link goes to Google Scholar");
  ok(link.attr('href').indexOf(encodeURIComponent(this.metadata.doi)) > -1, "Link href contains the DOI");
});

test( "addScholarTitleLink", function() {
  var $fixture = $('#qunit-fixture');
  $fixture.append('<ul id="oa_links"></ul>');

  oabSuccess.addScholarTitleLink(this.metadata);

  var link = $("a", $fixture);
  equal(link.length, 1, "Only one link added");
  ok(link.attr('href').indexOf('scholar.google.com') > -1, "Link goes to Google Scholar");
  ok(link.attr('href').indexOf(encodeURIComponent(this.metadata.title)) > -1, "Link href contains the DOI");
});
