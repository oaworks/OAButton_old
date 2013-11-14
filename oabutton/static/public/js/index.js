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
                        L.tileLayer('http://{s}.tile.cloudmade.com/cee9bfb83d854a2f89a4a2445aa9f595/997/256/{z}/{x}/{y}.png', {
                                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>'
                                }).addTo(map);    

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
                                bubble_content = '<h4>' + evt.user_name;
                                if (evt.user_profession != '') {
                                    bubble_content += ' <em>(' + evt.user_profession + ')</em>';
                                }
                                bubble_content += '</h4>';
                                bubble_content += '<p>' + evt.story + '</p>';
                                bubble_content += '<a target="_blank" href="http://dx.doi.org/' + evt.doi + '">doi</a>';
                                bubble_content += ' | ';
                                bubble_content += '<a target="_blank" href="' + evt.url + '">url</a>';
                                bubble_content += ' | ';
                                bubble_content += evt.accessed || '';

                                var marker = new L.marker([evt.coords.lat, evt.coords.lng], { title: bubble_content, icon: oaIcon });
                                marker.bindPopup(bubble_content);

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
    //
    // Scrollspy effects
    $('body').on('activate.bs.scrollspy', function (e) {
        console.log(e);
    });

    $('#map .underlay').fadeIn();

    var midpoint = $('.thumbnails').width() / 2;
    $('.thumbnails li').each(function() {
        if ($(this).position().left >= midpoint) {
            $(this).addClass("right");
        }
    });

    $('.thumbnails a.thumb').bind('touchstart', function(e){
        $(this).parent().addClass('hover');
        e.stopPropagation();
    }).bind('touchend', function(e){

    $(this).parent().parent().find('.hover').removeClass('hover');
        e.stopPropagation();
    });

    oabutton.renderMap();
}); 
