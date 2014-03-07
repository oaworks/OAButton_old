var page = require('webpage').create();
var url = 'URL_GOES_HERE';
page.settings.userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36';
page.open(url, function (status) {
    page.evaluate(function () {
        return document.title;
    }, function(result){

    }); 
    console.log(page.content);
    phantom.exit();
});
