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
  teardown: function() {
    $.mockjaxClear();
  },
});

test( "parseCrossRef", function() {
  var entry = {"title":"Acute inflammatory arthritis: Monoarthritis risk stratification in Lyme disease","link":{"href":"http://dx.doi.org/10.1038%2Fnrrheum.2013.47"},"id":"http://dx.doi.org/10.1038/nrrheum.2013.47","updated":"2013-09-23T06:07:17-04:00","content":{"div":{"p":[{"b":"Acute inflammatory arthritis: Monoarthritis risk stratification in Lyme disease"},"\n\tNature Reviews Rheumatology. \n\t<ahref=\"http://dx.doi.org/10.1038%2Fnrrheum.2013.47\">10.1038/nrrheum.2013.47</a>","\n\tAuthors:\n\t\n\t\n\tRobert T. Schoen\n\t\n\t\n\t\n      "],"xmlns":"http://www.w3.org/1999/xhtml"},"type":"xhtml"},"pam:message":{"pam:article":{"xhtml:head":{"xmlns:xhtml":"http://www.w3.org/1999/xhtml"},"dc:identifier":"10.1038/nrrheum.2013.47","dc:title":"Acute inflammatory arthritis: Monoarthritis risk stratification in Lyme disease","dc:publisher":"Nature Publishing Group","dc:isPartOf":"1759-4790","prism:alternateTitle":"Nature Reviews Rheumatology","dc:creator":"Robert T. Schoen","prism:publicationName":"Nature Reviews Rheumatology","prism:issn":"1759-4790","prism:eIssn":"1759-4804","prism:doi":"10.1038/nrrheum.2013.47","prism:publicationDate":"2013-4-9","prism:volume":"9","prism:startingPage":"261","prism:endingPage":"262","prism:url":"http://dx.doi.org/10.1038%2Fnrrheum.2013.47"},"xmlns:pam":"http://prismstandard.org/namespaces/pam/2.0/","xsi:schemaLocation":"http://prismstandard.org/namespaces/pam/2.0/ \n\t\t\t\t   http://www.prismstandard.org/schemas/pam/2.1/pam.xsd"}};

  var result = oabSuccess.parseCrossRef(entry, this.doi);

  deepEqual(result, this.metadata, "Parses data correctly");
});

test( "formatAuthorList", function() {
  one_author = ["A. N. Other"];
  two_authors = ["A. N. Other", "J. Smith"];
  three_authors = ["A. N. Other", "J. Smith", "F. Jones"];

  equal(oabSuccess.formatAuthorList(one_author),
	"A. N. Other", "Single author");
  equal(oabSuccess.formatAuthorList(two_authors),
	"A. N. Other & J. Smith", "Two authors");
  equal(oabSuccess.formatAuthorList(three_authors),
	"A. N. Other et. al.", "Three or more authors");
});

test( "parseAuthorList", function() {
  deepEqual(oabSuccess.parseAuthorList("A. N. Other"),
	["A. N. Other"], "Single author");
  deepEqual(oabSuccess.parseAuthorList("A. N. Other and J. Smith"),
	["A. N. Other", "J. Smith"],
	"Two authors with 'and'");
  deepEqual(oabSuccess.parseAuthorList("A. N. Other, J. Smith"),
	["A. N. Other", "J. Smith"],
	"Two authors with comma");
  deepEqual(oabSuccess.parseAuthorList("A. N. Other & J. Smith"),
	["A. N. Other", "J. Smith"],
	"Two authors with ampersand");
  deepEqual(oabSuccess.parseAuthorList("A. N. Other, F. Jones and J. Smith"),
	["A. N. Other", "F. Jones", "J. Smith"],
	"Three authors with comma and 'and'");
  deepEqual(oabSuccess.parseAuthorList("A. N. Other and F. Jones and J. Smith"),
	["A. N. Other", "F. Jones", "J. Smith"],
	"Three authors with 'and'");
  deepEqual(oabSuccess.parseAuthorList("A. N. Other, F. Jones, J. Smith"),
	["A. N. Other", "F. Jones", "J. Smith"],
	"Three authors with commas");
});

test( "addScholarDOILink", function() {
  var $fixture = $('#qunit-fixture');
  $fixture.append('<ul id="google_links"></ul>');

  oabSuccess.addScholarDOILink(this.metadata);

  var link = $("a", $fixture);
  equal(link.length, 1, "Only one link added");
  ok(link.attr('href').indexOf('scholar.google.com') > -1, "Link goes to Google Scholar");
  ok(link.attr('href').indexOf(encodeURIComponent(this.metadata.doi)) > -1, "Link href contains the DOI");
});

test( "addScholarTitleLink", function() {
  var $fixture = $('#qunit-fixture');
  $fixture.append('<ul id="google_links"></ul>');

  oabSuccess.addScholarTitleLink(this.metadata);

  var link = $("a", $fixture);
  equal(link.length, 1, "Only one link added");
  ok(link.attr('href').indexOf('scholar.google.com') > -1, "Link goes to Google Scholar");
  ok(link.attr('href').indexOf(encodeURIComponent(this.metadata.title)) > -1, "Link href contains the DOI");
});

asyncTest( "discoverCORELinks", function() {
  expect(6);

  var $fixture = $('#qunit-fixture');
  $fixture.append('<ul id="core_links"></ul>');

  $.mockjax({
    url: "/metadata/coresearch.json/*",
    responseText: {"ListRecords":[{"total_hits":5015},{"record":{"header":{"header:content":{"core:repositoryIdentifier":"143","identifier":"669636"},"header:attr":{"xmlns:core":"http:\/\/core.kmi.open.ac.uk\/api\/doc"}},"metadata":{"oai_dc:dc":{"oai_dc:ns":[{"xmlns:oai_dc":"http:\/\/www.openarchives.org\/OAI\/2.0\/oai_dc\/","xmlns:dc":"http:\/\/purl.org\/dc\/elements\/1.1\/"}],"dc:creator":"R Kudyar","dc:format":"application\/pdf","dc:source":"http:\/\/www.jkscience.org\/archive\/111\/18-RL-JACORD%20ARTHRITIS.pdf","dc:date":"2009","dc:identifier":"http:\/\/www.jkscience.org\/archive\/111\/18-RL-JACORD%20ARTHRITIS.pdf","dc:description":"A case of a patient with rheumatic valvulardisease who had comparable deformities of the handsand fingers and who fulfilled all of the criteriasuggested by Bywaters to describe Jaccoud's Arthritis is decribed here.","dc:title":"Jaccoud\u2019s Arthritis"}}}},{"record":{"header":{"header:content":{"core:repositoryIdentifier":"140","identifier":"60225"},"header:attr":{"xmlns:core":"http:\/\/core.kmi.open.ac.uk\/api\/doc"}},"metadata":{"oai_dc:dc":{"oai_dc:ns":[{"xmlns:oai_dc":"http:\/\/www.openarchives.org\/OAI\/2.0\/oai_dc\/","xmlns:dc":"http:\/\/purl.org\/dc\/elements\/1.1\/"}],"dc:creator":"Zai Liu, Guo Deng, Simon Foster and Andrej Tarkowski","dc:format":"application\/pdf","dc:source":"http:\/\/eprints.whiterose.ac.uk\/21\/1\/ar330.pdf","dc:date":"2001-09-17","dc:identifier":"http:\/\/eprints.whiterose.ac.uk\/21\/1\/ar330.pdf","dc:description":"Staphylococcus aureus is one of the most important pathogens in septic arthritis. To analyse the arthritogenic properties of staphylococcal peptidoglycan (PGN), highly purified PGN from S. aureus was intra-articularly injected into murine joints. The results demonstrate that PGN will trigger arthritis in a dose-dependent manner. A single injection of this compound leads to massive infiltration of predominantly macrophages and polymorphonuclear cells with occasional signs of cartilage and\/or bone destruction, lasting for at least 14 days. Further studies showed that this condition is mediated by the combined impact of acquired and innate immune systems. Our results indicate that PGN exerts a central role in joint inflammation triggered by S. aureus.","dc:title":"Staphylococcal peptidoglycans induce arthritis"}}}},{"record":{"header":{"header:content":{"core:repositoryIdentifier":"143","identifier":"5726004"},"header:attr":{"xmlns:core":"http:\/\/core.kmi.open.ac.uk\/api\/doc"}},"metadata":{"oai_dc:dc":{"oai_dc:ns":[{"xmlns:oai_dc":"http:\/\/www.openarchives.org\/OAI\/2.0\/oai_dc\/","xmlns:dc":"http:\/\/purl.org\/dc\/elements\/1.1\/"}],"dc:creator":"Karambin Mohammad Mehdi and Hashemian Hooman","dc:format":"application\/pdf","dc:source":"http:\/\/journals.tums.ac.ir\/PdfMed.aspx?pdf_med=\/upload_files\/pdf\/12751.pdf&manuscript_id=12751","dc:date":"2009","dc:identifier":"http:\/\/journals.tums.ac.ir\/PdfMed.aspx?pdf_med=\/upload_files\/pdf\/12751.pdf&manuscript_id=12751","dc:description":"To determine the rate of different types of arthritis in children. We prepared a retrospective descriptive study and included the whole 100 cases of arthritis referred to 17-Shahrivar Hospital, Rasht, Guilan during a 3 years period. Using their medical files, data including age, sex, season of admission, history of trauma, signs and symptoms, lab findings and duration of hospitalization were collected. SPSS 13.0 (statistical software) applied for statistical analysis. The most common age of involvement ranged 6-9 years. Septic arthritis, brucellosis, and rheumatoid fever were the most frequent causes of arthritis in our study. Fever and restricted range of motion had the highest rate among different signs and symptoms. Lab data demonstrated leukocytosis, positive CRP, and increased ESR among 74, 79.5, and 73 percent of our patients, respectively. According to the high prevalence of septic arthritis and the arthritis due to brucellosis and rheumatoid fever, it seems that mentioned diseases are still major problems in the issue of hygiene management.","dc:title":"Childhood Arthritis: Rate of Different Types"}}}}]},
  });

  oabSuccess.discoverCORELinks(this.metadata);
  metadata = this.metadata;

  setTimeout(function() {
    var $link = $("li a", $fixture);
    equal($link.length, 4, "Four links added"); // 3 + 1 "full search" link

    var $core_div = $('#core_links', $fixture);
    ok(/5015 matches/.test($core_div.text()), "Number of hits shown");

    $link = $("a:contains('Jaccoud\u2019s Arthritis')", $fixture);
    equal($link.length, 1, "Link with 'Jaccoud\u2019s Arthritis' added");
    equal($link.attr('href'), "http:\/\/www.jkscience.org\/archive\/111\/18-RL-JACORD%20ARTHRITIS.pdf",
    	  "Link points to correct PDF");

    $link = $("a:contains('See all results')", $fixture);
    equal($link.length, 1, "'See all results' link");
    equal($link.attr('href'),
    	  "http://core.kmi.open.ac.uk/search/" + encodeURIComponent("title:(" + metadata.title + ")"),
    	  "Link points to correct PDF");

    start();
  }, 500);
});

asyncTest( "discoverCORELinks empty result set", function() {
  expect(2);

  var $fixture = $('#qunit-fixture');
  $fixture.append('<ul id="core_links"></ul>');

  $.mockjax({
    url: "/metadata/coresearch.json/*",
    responseText: {"ListRecords":[{"total_hits":0}]}
  });

  oabSuccess.discoverCORELinks(this.metadata);

  setTimeout(function() {
    var $link = $("li a", $fixture);
    equal($link.length, 0, "No links added");

    var $core_div = $('#core_links', $fixture);
    ok(/No matches/.test($core_div.text()), "Useful error shown");

    start();
  }, 500);
});

