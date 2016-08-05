/* helper script to encode URL parameters */
var build_params = function(params) {
	var items = [];

	for (var param in params) {
		if (params.hasOwnProperty(param) ) {
			items.push(encodeURIComponent(param) + "=" + encodeURIComponent(params[param]));
		}
	}

	return items.join("&");
};

/* insert a script to extract data from the current tab */
var open_access_button = function() {
	chrome.tabs.executeScript(null, { file: "extract.js" }, function(result) {
		var url = "https://oabutton.herokuapp.com/add?" + build_params(result[0]);
		chrome.windows.create({ url: url, type: "detached_panel", width: 450, height: 700, focused: true });
	});
};

/* when the toolbar button is clicked */
chrome.browserAction.onClicked.addListener(open_access_button);
