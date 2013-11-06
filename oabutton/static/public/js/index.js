$(document).ready(function() {

    // Highlight some node. This ought to be moved to some common JS
    $.fn.animateHighlight = function(highlightColor, duration) {
        var highlightBg = highlightColor || "#FFFF9C";
        var animateMs = duration || 1500;
        var originalBg = this.css("backgroundColor");
        this.stop().css("background-color",
        highlightBg).animate({backgroundColor:
            originalBg}, animateMs);
    };

    // Bind submission form
    $('#form-bookmarklet').ajaxForm({ 
        target:     '#divToUpdate',
        dataType:   'json',
        url:        '/api/signin/',
        error:      function() {
            $('#id_email').animateHighlight("#dd0000", 1000);
        },
        success:    function(responseJSON, statusText, xhr, formElem) {

            var bookmarklet = $('#bookmarklet .content');
            var dialog = $('#bookmarklet-modal');

            // Set URL from service response
            $('.btn-primary', bookmarklet).attr('href', 
                "javascript:document.getElementsByTagName('body')[0]" +
                ".appendChild(document.createElement('script'))" +
                ".setAttribute('src','"+responseJSON['url']+"');"
            );

            // Open the modal dialog
            $('.modal-body', dialog).empty().append(bookmarklet.html());
            dialog.modal();

            // Show the new bookmarklet
            $('#bookmarklet').show();

            // Roll up the form
            $('#form-bookmarklet .form-body').slideUp();

        } // -success
    }); // -ajaxForm

}); 