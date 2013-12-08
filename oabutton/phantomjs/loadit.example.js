var page = require('webpage').create();
var url = 'http://stke.sciencemag.org/cgi/content/abstract/sigtrans;6/302/ra100?view=abstract';
page.open(url, function (status) {
    page.evaluate(function () {
        return document.title;
    }, function(result){

    }); 
    console.log(page.content);
    phantom.exit();
});
