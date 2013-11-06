// Highlight some node. This ought to be moved to some common JS
$.fn.animateHighlight = function(highlightColor, duration) {
    var highlightBg = highlightColor || "#FFFF9C";
    var animateMs = duration || 1500;
    var originalBg = this.css("backgroundColor");
    this.stop().css("background-color",
    highlightBg).animate({backgroundColor:
        originalBg}, animateMs);
};


// wait for the DOM to be loaded 
$(document).ready(function() { 
    // first hide the bookmarklet
    $('#bookmarklet').hide();

    // bind 'myForm' and provide a simple callback function 
    var options = { 
        target:     '#divToUpdate',
        dataType:   'json',
        url:        '/api/signin/',
        error:      function() {
            $('#id_email').animateHighlight("#dd0000", 1000);
        },
        success:    function(responseJSON, statusText, xhr, formElem) { 
            $('#bookmarklet-js').attr('href',
            "javascript:document.getElementsByTagName('body')[0].appendChild(document.createElement('script')).setAttribute('src','"+responseJSON['url']+"');");

            // Show the new bookmarklet
            $('#bookmarklet').show();

            var dialog = new BootstrapDialog({
                title : $('<h2>Drag this to your bookmark bar</h2>'),
                content: $("<a href=\"javascript:document.getElementsByTagName('body')[0].appendChild(document.createElement('script')).setAttribute('src','"+responseJSON['url']+"');\" class=\"btn btn-large\"><i class=\"icon-bookmark\"></i> Open Access Button </a>"),
                buttons :   [{
                    label : 'OK',
                    onclick :
                    function(dialog){
                        dialog.close();
                    }
                }]
            });
            dialog.open();

        } 
    }; 
    $('#form-bookmarklet').ajaxForm(options);
}); 