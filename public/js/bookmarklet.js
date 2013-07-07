function loadScript(url, callback)
{
    // adding the script tag to the head as suggested before
   var head = document.getElementsByTagName('head')[0];
   var script = document.createElement('script');
   script.type = 'text/javascript';
   script.src = url;

   // then bind the event to the callback function 
   // there are several events for cross browser compatibility
   script.onreadystatechange = callback;
   script.onload = callback;

   // fire the loading
   head.appendChild(script);
}

function removeScriptTag() {
    var scriptNode = document.getElementsByTagName("body")[0].lastChild;
    var src = scriptNode.getAttribute("src");
    try {
        scriptNode.parentNode.removeChild(scriptNode)
    } catch (e) {}
    return src
}

function applyCss(el, css) {
    var s = "";
    for (var p in css) s += p + ":" + css[p] + ";";
    el.style.cssText = el.style.cssText + s;
}

function ready() {
    doi_pattern = /\b(10[.][0-9]{4,}(?:[.][0-9]+)*\/(?:(?!["&\'<>])[[:graph:]])+)\b/;
    body = $('body');

    source = removeScriptTag();
    domain = source.match(/^https?:\/\/[^/]+/);
    iframe_css = {
        "position": "fixed",
        "z-index": 2147483640,
        "-moz-box-sizing": "border-box",
        "box-sizing": "border-box",
        "padding": "15px",
        "border": "0",
        "background": "white",
        "height": "100%",
        "width": "350px",
        "top": "0",
        "right": "0",
        "overflow": "hidden"
    };
    iframe_src = domain + "/add?url=" + window.location;
    iframe = $("<iframe>").attr({'allowTransparency': true, 'width': '350px', 'height': '100%', 'src': iframe_src}).css(iframe_css);
    body.append(iframe);
}

loadScript("//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js", ready);
