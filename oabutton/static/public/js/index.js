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

            var bookmarklet = $('#bookmarklet .content');
            var dialog = $('#bookmarklet-modal');

            // Set URL from service response
            $('.btn-primary', bookmarklet).attr('href', 
                "javascript:document.getElementsByTagName('body')[0]" +
                ".appendChild(document.createElement('script'))" +
                ".setAttribute('src','"+responseJSON['url']+"');"
            );

            // Show the new bookmarklet and instructions, roll up form
            $('#bookmarklet').show();
            $('#form-bookmarklet').slideUp();
            dialog.modal();

        } // -success
    }); // -ajaxForm

    // Move into DB or so
    var teamData = [
        {
            link: "http://twitter.com/Mcarthur_Joe",
            thumb_url: '/img/joe.jpg',
            name: "Joe",
            twitter: "Mcarthur_Joe"
        },{
            link: "http://twitter.com/davidecarroll",
            thumb_url: '/img/david.jpg',
            name: "David",
            twitter: "davidecarroll"
        },{
            link: "http://twitter.com/nicholascwng",
            thumb_url: 'https://secure.gravatar.com/avatar/9637895e310caf25237e89155157b2a7?s=200',
            name: "Nick",
            twitter: "nicholascwng"
        },{
            link: "http://twitter.com/andylolz",
            thumb_url: 'https://secure.gravatar.com/avatar/bbb9eb1af3b427f8259df33f6e8844aa?s=200',
            name: "Andy",
            twitter: "andylolz"
        },{
            link: "http://twitter.com/frathgeber",
            thumb_url: 'https://secure.gravatar.com/avatar/d178a6201be696c466c41c355c671707?s=200',
            name: "Florian",
            twitter: "frathgeber"
        },{
            thumb_url: '/img/elliot.jpg',
            name: "Elliot"
        }
    ]; //-teamdata

}); 
