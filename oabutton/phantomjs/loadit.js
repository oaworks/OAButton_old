var page = require('webpage').create();
var url = 'URL_GOES_HERE';
page.open(url, function (status) {
    page.evaluate(function () {
        return document.title;
    }, function(result){

    }); 
    console.log(page.content);
    phantom.exit();
});
