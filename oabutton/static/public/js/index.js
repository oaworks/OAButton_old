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
    // $('#bookmarklet').hide();

    // bind 'myForm' and provide a simple callback function 
    var options = { 
        target:     '#divToUpdate',
        dataType:   'json',
        url:        '/api/signin/',
        error:      function(ctx) {
            var errors = JSON.parse(ctx.responseText).errors;

            if ('email' in errors) {
                $('#id_email').animateHighlight("#dd0000", 1000);
            }

            if ('name' in errors) {
                $('#id_name').animateHighlight("#dd0000", 1000);
            }

            if ('confirm_public' in errors) {
                $('label.confirm-label').animateHighlight("#dd0000", 1000);
            }
        },
        success:    function(responseJSON, statusText, xhr, formElem) { 
            $('#bookmarklet-js').attr('href',
            "javascript:document.getElementsByTagName('body')[0].appendChild(document.createElement('script')).setAttribute('src','"+responseJSON['url']+"');");

            // Show the new bookmarklet
            $('#bookmarklet').show();
        } 
    }; 
    $('#form-bookmarklet').ajaxForm(options);
}); 
