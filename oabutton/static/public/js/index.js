$(document).ready(function() {

    var oabutton = {
        renderMap : function () {
                        if (typeof L == 'undefined') return;

                        var map = L.map('map', {
                            center: [20, 0],
                            maxZoom: 18,
                            minZoom: 2,
                            scrollWheelZoom: false,
                            touchZoom: false,
                            zoom: 2
                        });
                        L.tileLayer('https://{s}.tiles.mapbox.com/v3/crankycoder.ieh8j164/{z}/{x}/{y}.png').addTo(map);

                        var oaIcon = L.icon({
                            iconUrl: 'static/img/noalogo.png',
                            iconSize: [12, 19],
                            iconAnchor: [6, 9],
                            popupAnchor: [0, -12]
                        });

                        var markers = new L.MarkerClusterGroup();
                        for (var i = 0; i < events.length; i++) {
                            var evt = events[i];
                            if(evt.coords.lat && evt.coords.lng) {
                                // TODO: use a template for the bubble content
                                var bubble = $('<h4/>', { text: evt.user_name });

                                if (evt.user_profession) {
                                    bubble.append(' '); // should be using CSS for spacing

                                    $('<em/>', {
                                        text: '(' + evt.user_profession + ')'
                                    }).appendTo(bubble);
                                }

                                $('<p/>', {
                                    text: evt.story
                                }).appendTo(bubble);

                                if (evt.doi) {
                                    $('<a/>', {
                                        target: '_blank',
                                        href: 'http://dx.doi.org/' + encodeURIComponent(evt.doi),
                                        text: 'doi'
                                    }).appendTo(bubble);
                                }

                                if (evt.doi && evt.url) {
                                    bubble.append(' | ');
                                }

                                if (evt.url) {
                                    $('<a/>', {
                                        target: '_blank',
                                        href: evt.url,
                                        text: 'url'
                                    }).appendTo(bubble);
                                }

                                if (evt.accessed) {
                                    $('<span/>', {
                                        text: ' | ' + evt.accessed
                                    }).appendTo(bubble);
                                }

                                var marker = new L.marker([evt.coords.lat, evt.coords.lng], { title: evt.url + " blocked", icon: oaIcon });
                                marker.bindPopup(bubble.html());

                                markers.addLayer(marker);
                            }
                        }
                        map.addLayer(markers);
                    }
    }

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
        success: function(responseJSON, statusText, xhr, formElem) {

            // Set URL from service response
            var bookmarklet = $('#bookmarklet .content');
            $('.btn-primary', bookmarklet).attr('href', 
                "javascript:document.getElementsByTagName('body')[0]" +
                ".appendChild(document.createElement('script'))" +
                ".setAttribute('src','"+responseJSON['url']+"');"
            );

            // Show the new bookmarklet and instructions, roll up form
            $('#bookmarklet').show().addClass('slidetop');
            $('#form-bookmarklet').slideUp();

            window.location = '#top';
            $('#help-bookmarklet').fadeIn();

        } // -success
    }); // -ajaxForm

    // Scrollspy effects (unused)
    //$('body').on('activate.bs.scrollspy', function (e) {
        //console.log(e);
    //});

    // Show the map underlay (later as effect)
    $('#map .underlay').fadeIn();

    // Stop video on close dialog
    $('#video-modal').on('hidden.bs.modal', function () { 
        $('iframe').each(function() { 
            this.contentWindow.postMessage(
                '{"event":"command","func":"pauseVideo","args":""}', '*'
            ); 
        });
    });

    // Use JQuery Placeholder plugin on older browsers (ex. IE 9)
    $('#form-bookmarklet input[type="text"]').placeholder();

    // Position the thumbnail hovers
    var midpoint = $('.thumbnails').width() / 2;
    $('.thumbnails li').each(function() {
        if ($(this).position().left >= midpoint) {
            $(this).addClass("right");
        }
    });

    // Tap as hover on touchscreens
    $('.thumbnails a.thumb').bind('touchstart', function(e){
        $(this).parent().addClass('hover');
        e.stopPropagation();
    }).bind('touchend', function(e){
        $(this).parent().parent().find('.hover').removeClass('hover');
        e.stopPropagation();
    }).css('visibility', 'visible'); // Avoids doubles while loading JS
    oabutton.renderMap();

    // Page links should all be new window
    $('a[href^="http"]').attr('target', '_blank');
}); 
