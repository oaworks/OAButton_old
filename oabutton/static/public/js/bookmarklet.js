(function() {
  // Detect a DOI for the article
  var detectDOI = function() {
    var nodes, node, childNode, matches, i, j;

    // match DOI: test on http://t.co/eIJciunBRJ
    var doi_re = /\b10\.\d{4,}(?:\.\d+)*\/\S+\b/;

    // look for meta[name=citation_doi][content]
    nodes = document.getElementsByTagName("meta");
    for (i = 0; i < nodes.length; i++) {
      node = nodes[i];

      if (node.getAttribute("name") == "citation_doi") {
        return node.getAttribute("content").replace(/^doi:/, "");
      }
    }

    // look in all text nodes for a DOI
    nodes = document.getElementsByTagName("*");
    for (i = 0; i < nodes.length; i++) {
      node = nodes[i];

      if (!node.hasChildNodes()) {
        continue;
      }

      if (node.nodeName == "SCRIPT") {
        continue;
      }

      for (j = 0; j < node.childNodes.length; j++) {
        childNode = node.childNodes[j];

        // only text nodes
        if (childNode.nodeType !== 3) {
          continue;
        }

        if (matches = doi_re.exec(childNode.nodeValue)) {
          return matches[0];
        }
      }
    }

    return null;
  };

  // Detect an email address for the corresponding author.
  var detectAuthorEmail = function() {
    var nodes, node, matches, i;

    // match email address in mailto link
    // from http://stackoverflow.com/a/201447/145899
    var mailto_re = /^mailto:(\S+@\S+\.\S+)/;

    // look for meta[name=citation_author_email][content]
    // test on http://dx.doi.org/10.1007/978-3-642-02879-3_7
    nodes = document.getElementsByTagName("meta");
    for (i = 0; i < nodes.length; i++) {
      node = nodes[i];

      if (node.getAttribute("name") == "citation_author_email") {
        return node.getAttribute("content");
      }
    }

    // look for links that start with "mailto:".
    // can't guarantee this is the author - might be an editor or support email.
    // test on http://dx.doi.org/10.1371/journal.pone.0052814
    nodes = document.getElementsByTagName("a");
    for (i = 0; i < nodes.length; i++) {
      node = nodes[i];

      if (matches = mailto_re.exec(node.getAttribute("href"))) {
        return matches[1].replace(/\?.*/, ""); // remove any query string
      }
    }

    return null;
  };

  // ascertain if the bookmarklet has already been called
  var exists = document.getElementById("OAButton");

  if(exists == null)
  {

		// get the base URL
		var loader = document.body.lastChild;
		var base = loader.getAttribute("src").match(/^https?:\/\/[^/]+/)[0];
		loader.parentNode.removeChild(loader);

		// build the iframe URL
		var url = base + "/api/add/?url=" + encodeURIComponent(window.location);
		var doi = detectDOI();
		if(doi) {
		  url += "&doi=" + encodeURIComponent(doi);
		}
    var email = detectAuthorEmail();
    if (email) {
      url += "&email=" + encodeURIComponent(email);
    }

		// build the control div
		var div = document.createElement("div");
		div.setAttribute("allowTransparency", "true");
		div.setAttribute("id", "OAButton");

		div.style.position = "fixed";
		div.style.zIndex = "2147483640";
		div.style.boxSizing = "border-box";
		div.style.MozBoxSizing = "border-box";
		div.style.padding = "15px";
		div.style.background = "white";
		div.style.height = "100%";
		div.style.width = "350px";
		div.style.top = "0";
		div.style.right = "0";
		div.style.overflow = "scroll";
		div.style.overflowX = "hidden";

		document.body.appendChild(div);

		// add the close button
		var closeButton = document.createElement("a");
		closeButton.setAttribute("href", "javascript:document.getElementById('OAButton').setAttribute('style', 'display:none')");
		closeButton.setAttribute("id", "closeButton");
		closeButton.appendChild(document.createTextNode("X"));
		closeButton.style.zIndex = "2147483641";
		closeButton.style.position = "relative";
		closeButton.style.top = "0";

		div.appendChild(closeButton);

		// add the iframe
		var iframe = document.createElement("iframe");
		iframe.setAttribute("allowTransparency", "true");
		iframe.setAttribute("src", url);

		iframe.style.position = "fixed";
		iframe.style.zIndex = "2147483640";
		iframe.style.boxSizing = "border-box";
		iframe.style.MozBoxSizing = "border-box";
		iframe.style.padding = "15px";
		iframe.style.borderLeft = "2px #555 dashed";
		iframe.style.background = "white";
		iframe.style.height = "100%";
		iframe.style.width = "350px";
		iframe.style.bottom = "0";
		iframe.style.right = "0";

		div.appendChild(iframe);
	} else {
		var div = exists;
		div.setAttribute("allowTransparency", "true");
		div.setAttribute("id", "OAButton");

		div.style.position = "fixed";
		div.style.zIndex = "2147483640";
		div.style.boxSizing = "border-box";
		div.style.MozBoxSizing = "border-box";
		div.style.padding = "15px";
		div.style.background = "white";
		div.style.height = "100%";
		div.style.width = "350px";
		div.style.top = "0";
		div.style.right = "0";
		div.style.overflow = "scroll";
		div.style.overflowX = "hidden";
		div.style.display = "block";

	}
})();

