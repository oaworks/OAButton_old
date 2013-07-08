(function() {
  var detectDOI = function() {
    var nodes, node, childNode, matches, i, j;

    // match DOI: test on http://t.co/eIJciunBRJ
    var re = /10\.\d{4,}(?:\.\d+)*\/\S+/;

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

      for (j = 0; j < node.childNodes.length; j++) {
        childNode = node.childNodes[j];

        // only text nodes
        if (childNode.nodeType !== 3) {
          continue;
        }

        if (matches = re.exec(childNode.nodeValue)) {
          return matches[0];
        }
      }
    }

    return null;
  };

  // get the base URL
  var loader = document.body.lastChild;
  var base = loader.getAttribute("src").match(/^https?:\/\/[^/]+/)[0];
  loader.parentNode.removeChild(loader);

  // build the iframe URL
  var url = base + "/add?url=" + encodeURIComponent(window.location);
  var doi = detectDOI();
  if(doi !== null) {
    url += "&doi=" + encodeURIComponent(doi);
  }

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
  iframe.style.top = "0";
  iframe.style.right = "0";
  iframe.style.overflow = "hidden";

  document.body.appendChild(iframe);
})();

