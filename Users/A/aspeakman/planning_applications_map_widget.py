import scraperwiki

THIS_URL = "https://views.scraperwiki.com/run/planning_applications_map_widget/"
JSONP_URL = "https://views.scraperwiki.com/run/pa_api/"

try:
    query = scraperwiki.utils.GET()
except:
    query = {}

if query.get('wtype', '') == 'css':
    # supplies an embedded widget style sheet
    # this is implemented but not used for anything meaningful yet
    scraperwiki.utils.httpresponseheader("Content-Type", "text/css")
    print """
    #pa-widget-container
    {
    background-color:#b0c4de;
    }
    #pa-widget-block
    {
    background-color:#b0c4de;
    }
    """

else:
    query['fmt'] = 'jsonp'
    if not query.get('db'): # must specify a database
        query['db'] = 'London'
    if not query.get('dtype'): # adding this will ensure it won't ever return an authorities list (instead of the applications list)
        query['dtype'] = ''

    # note all other query parameters pass transparently through to the JSONP call -> which interfaces to the API
    DATA_QUERY = '{ ' # make a Javascript friendly formatted representation of the query parameters
    for k, v in query.items():
        DATA_QUERY = DATA_QUERY + k + ': "' + v.replace('"', '""') + '", '
    DATA_QUERY = DATA_QUERY[:-2] + ' }'
    #print DATA_QUERY
    scraperwiki.utils.httpresponseheader("Content-Type", "application/javascript")
    print """
    
    (function() { // main anonymous function contains everything
    
    // Localize jQuery and google variables
    var jQuery;
    var google;
    var widgetMap;
    var mapColours = [ 'ff0000', '00ff00', '0000ff', 'ffff00', '00ffff', 'ff00ff', 'cccc00', '00cccc', 'cc00cc' ];
    var match_in_date = /^(\d\d\d\d)-(\d\d)-(\d\d)$/;
    var match_at_date = /^(\d\d*)\/(\d\d*)\/(\d\d\d\d)$/;
    var infoWindow;
    var ukRegion;
    
    /******** Start by loading jQuery 1.4.2 if not present *********/
    if (window.jQuery === undefined || window.jQuery.fn.jquery !== '1.4.2') {
        var script_tag = document.createElement('script');
        script_tag.setAttribute("type","text/javascript");
        script_tag.setAttribute("src",
            "http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js");
        if (script_tag.readyState) {
          script_tag.onreadystatechange = function () { // For old versions of IE
              if (this.readyState == 'complete' || this.readyState == 'loaded') {
                  scriptLoadHandler();
              }
          };
        } else {
          script_tag.onload = scriptLoadHandler;
        }
        // Try to find the head, otherwise default to the documentElement
        (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(script_tag);
    } else {
        // The jQuery version on the window is the one we want to use
        jQuery = window.jQuery;
        googleInitLoader();
    }
    
    /******** Called once jQuery has loaded ******/
    function scriptLoadHandler() {
        // Restore $ and window.jQuery to their previous values and store the
        // new jQuery in our local jQuery variable
        jQuery = window.jQuery.noConflict(true);
        googleInitLoader();
    }

    /******** After jQuery load, use the same principles to get the google loader if Google maps version 3 is not present *********/
    function googleInitLoader() {
        if (window.google !== undefined && window.google.maps !== undefined && window.google.maps.version.charAt(0) === '3') {
            google = window.google; // maps v3 already loaded
            main();
        } else if (window.google !== undefined && window.google.load !== undefined) {
            mapsLoadHandler();
        } else {
            var script_tag = document.createElement('script');
            script_tag.setAttribute("type","text/javascript");
            script_tag.setAttribute("src","https://www.google.com/jsapi");
            if (script_tag.readyState) {
              script_tag.onreadystatechange = function () { // For old versions of IE
                  if (this.readyState == 'complete' || this.readyState == 'loaded') {
                      mapsLoadHandler();
                  }
              };
            } else {
              script_tag.onload = mapsLoadHandler;
            }
            // Try to find the head, otherwise default to the documentElement
            (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(script_tag);
        }
    }

    /******** do loading of google maps ********/
    function mapsLoadHandler() {
        google = window.google;
        google.load("maps", "3", { "other_params":"sensor=false", callback: function () { main(); }});
    }

    /******** Our main function ********/
    function main() {

        jQuery(document).ready(function($) {

            /******* Load internal CSS style sheet*******/
            var css_link = $("<link>", {
                rel: "stylesheet",
                type: "text/css",
                href: '"""+THIS_URL+"""?wtype=css'
            });
            css_link.appendTo('head');    

            allLoaded($); 

        });
    }
    
    // subroutine to do the main work of populating the map or list
    function allLoaded($) {

        if ($("#pa-widget-container").length > 0) {

            /** Create a default full UK wide map **/
            var mapTypeIds = [];
            for(var type in google.maps.MapTypeId) {
                mapTypeIds.push(google.maps.MapTypeId[type]);
            }
            mapTypeIds.push("OSM");
            var mapOptions = { "mapTypeId": google.maps.MapTypeId.ROADMAP,
                mapTypeControlOptions: { mapTypeIds: mapTypeIds },
                "zoom": 5, "center": new google.maps.LatLng(54.5, -2.8) };
            widgetMap = new google.maps.Map(document.getElementById("pa-widget-container"), mapOptions);
            infoWindow = new google.maps.InfoWindow(); // one window used for all popups
            ukRegion = new google.maps.LatLngBounds(new google.maps.LatLng(49.0, -10.0), new google.maps.LatLng(62.0, 3.0));
    
            /* handler for OSM map type */
            widgetMap.mapTypes.set("OSM", new google.maps.ImageMapType({
                getTileUrl: function(coord, zoom) {
                    return "http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";
                },
                tileSize: new google.maps.Size(256, 256),
                name: "OpenStreetMap",
                maxZoom: 18
            }));

        }
                    
        /******* Now load the map markers data via JSONP *******/
        var dataurl = '"""+JSONP_URL+"""';
        $.ajax({url:dataurl, dataType: "jsonp", data: """+DATA_QUERY+""", timeout: 30000,
            success:function(values) {
                if (values.applications === undefined) {
                    alert('No planning applications data found');
                }
                var planlist = values.applications.application;
                if (planlist.length > 0) {
                    var num_points = planlist.length;

                    if ($("#pa-widget-container").length > 0) {

                        var latlngbounds = new google.maps.LatLngBounds();
                        var total_lat = 0.0;
                        var total_lng = 0.0;
                        var added = 0;
                        for (var i = 0; i < num_points; i++) {
                            addMarker(planlist[i]); // pos atribute is set in addMarker
                            if (planlist[i].pos !== undefined && ukRegion.contains(planlist[i].pos)) { // only within UK
                                total_lat = total_lat + planlist[i].pos.lat();
                                total_lng = total_lng + planlist[i].pos.lng();
                                latlngbounds.extend(planlist[i].pos);
                                added += 1;
                            }
                        }
                        widgetMap.setCenter(new google.maps.LatLng(total_lat/added, total_lng/added)); // centroid  
                        //google.maps.event.addListenerOnce(widgetMap, 'zoom_changed', function(event) {
                        //        if (this.getZoom() < 8) { // don't zoom out beyond 8
                        //            this.setZoom(8);
                        //        }
                        //});
                        widgetMap.fitBounds(latlngbounds);

                    }

                    if ($("#pa-widget-block").length > 0) {

                        var tag = '<dl>';
                        var planinfo;
                        for (var i = 0; i < num_points; i++) {
                            planinfo = planlist[i];
                            tag += '<dt><strong>'+planinfo.address+'</strong></dt>'+
                                '<dd>'+planinfo.description+'<br />'+
                                'Planning authority: '+planinfo.authority_long_name+'<br />'+
                                'Reference: '+
                                '<a href="'+planinfo.info_url+'" target="_blank">'+
                                planinfo.reference+'</a>';
                            if (planinfo.received_date) {
                                tag += '<br />Date received: '+showDate(planinfo.received_date); }
                            else if (planinfo.validated_date) {
                                tag += '<br />Date validated: '+showDate(planinfo.validated_date); }
                            tag += '</dd>';
                        }
                        tag += '</dl>';

                        $('#pa-widget-block').html(tag);

                    }

                } else {
                    alert('Zero planning applications returned');
                }
            },
            error:function(object, status) {
                alert('Failed to retrieve any planning applications ('+status+')');
            }
        });

    }


    /******** helper functions ********/
    function addMarker(planinfo)
    {
        if (!planinfo['lat'] || !planinfo['lng']) return false;
        var lat = planinfo['lat'] + ((Math.random()*2-1)/11100);
        var lng = planinfo['lng'] + ((Math.random()*2-1)/7000);
        // adds a random value equiv to approx +-10m in case multiple markers are on one spot
        planinfo.pos = new google.maps.LatLng(lat, lng);
        var letter = planinfo.authority.substr(0,1);
        var index = String.charCodeAt(letter) % 9;
        var lt2 = letter+planinfo.authority.substr(3,1);
        var col = mapColours[index]; // add colour here based on authority first letter
        planinfo.icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+lt2+'|'+col+'|000000';
        planinfo.marker = new google.maps.Marker({position:planinfo.pos, map:widgetMap, title:planinfo.address, icon:planinfo.icon});
        google.maps.event.addListener(planinfo.marker, "click", function()
        {
            var msg = '';
            if (planinfo.received_date) msg = 'Date received: '+showDate(planinfo.received_date)+'<br />';
            else if (planinfo.validated_date) msg = 'Date validated: '+showDate(planinfo.validated_date)+'<br />';
            infoWindow.setContent('<div><strong>'+planinfo.address+'</strong></div>'+
                    '<div>'+planinfo.description+'</div>'+
                    '<div>Planning authority: '+planinfo.authority_long_name+'<br />'+
                    'Reference: '+
                    '<a href="'+planinfo.info_url+'" target="_blank">'+planinfo.reference+'</a><br />'+
                    msg+
                    'Postcode: '+
                    planinfo.postcode+'</div>'
            );
            infoWindow.open(widgetMap, planinfo.marker);
        });
        return true;
    }

    function showDate(in_date) { // outputs formatted date
        if (!in_date) return 'Empty date';
        if (checkDate(in_date)) return in_date+'(dmy)';
        var dt_bits =  match_in_date.exec(in_date);
        if (!dt_bits) {
            return 'Wrong date format';
        } else if (dt_bits.length == 4) {
            return dt_bits[3]+'/'+dt_bits[2]+'/'+dt_bits[1];
        } else {
            return 'Date not matched';
        }
    }

    function checkDate(at_date) { // checks date parameter is supplied in dd/mm/yyyy format
        var dt_match =  at_date.match(match_at_date);
        if (dt_match) {
            return true;
        } else {
            return false;
        }
    }
    
    })(); // We call our main anonymous function immediately
    
    """


import scraperwiki

THIS_URL = "https://views.scraperwiki.com/run/planning_applications_map_widget/"
JSONP_URL = "https://views.scraperwiki.com/run/pa_api/"

try:
    query = scraperwiki.utils.GET()
except:
    query = {}

if query.get('wtype', '') == 'css':
    # supplies an embedded widget style sheet
    # this is implemented but not used for anything meaningful yet
    scraperwiki.utils.httpresponseheader("Content-Type", "text/css")
    print """
    #pa-widget-container
    {
    background-color:#b0c4de;
    }
    #pa-widget-block
    {
    background-color:#b0c4de;
    }
    """

else:
    query['fmt'] = 'jsonp'
    if not query.get('db'): # must specify a database
        query['db'] = 'London'
    if not query.get('dtype'): # adding this will ensure it won't ever return an authorities list (instead of the applications list)
        query['dtype'] = ''

    # note all other query parameters pass transparently through to the JSONP call -> which interfaces to the API
    DATA_QUERY = '{ ' # make a Javascript friendly formatted representation of the query parameters
    for k, v in query.items():
        DATA_QUERY = DATA_QUERY + k + ': "' + v.replace('"', '""') + '", '
    DATA_QUERY = DATA_QUERY[:-2] + ' }'
    #print DATA_QUERY
    scraperwiki.utils.httpresponseheader("Content-Type", "application/javascript")
    print """
    
    (function() { // main anonymous function contains everything
    
    // Localize jQuery and google variables
    var jQuery;
    var google;
    var widgetMap;
    var mapColours = [ 'ff0000', '00ff00', '0000ff', 'ffff00', '00ffff', 'ff00ff', 'cccc00', '00cccc', 'cc00cc' ];
    var match_in_date = /^(\d\d\d\d)-(\d\d)-(\d\d)$/;
    var match_at_date = /^(\d\d*)\/(\d\d*)\/(\d\d\d\d)$/;
    var infoWindow;
    var ukRegion;
    
    /******** Start by loading jQuery 1.4.2 if not present *********/
    if (window.jQuery === undefined || window.jQuery.fn.jquery !== '1.4.2') {
        var script_tag = document.createElement('script');
        script_tag.setAttribute("type","text/javascript");
        script_tag.setAttribute("src",
            "http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js");
        if (script_tag.readyState) {
          script_tag.onreadystatechange = function () { // For old versions of IE
              if (this.readyState == 'complete' || this.readyState == 'loaded') {
                  scriptLoadHandler();
              }
          };
        } else {
          script_tag.onload = scriptLoadHandler;
        }
        // Try to find the head, otherwise default to the documentElement
        (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(script_tag);
    } else {
        // The jQuery version on the window is the one we want to use
        jQuery = window.jQuery;
        googleInitLoader();
    }
    
    /******** Called once jQuery has loaded ******/
    function scriptLoadHandler() {
        // Restore $ and window.jQuery to their previous values and store the
        // new jQuery in our local jQuery variable
        jQuery = window.jQuery.noConflict(true);
        googleInitLoader();
    }

    /******** After jQuery load, use the same principles to get the google loader if Google maps version 3 is not present *********/
    function googleInitLoader() {
        if (window.google !== undefined && window.google.maps !== undefined && window.google.maps.version.charAt(0) === '3') {
            google = window.google; // maps v3 already loaded
            main();
        } else if (window.google !== undefined && window.google.load !== undefined) {
            mapsLoadHandler();
        } else {
            var script_tag = document.createElement('script');
            script_tag.setAttribute("type","text/javascript");
            script_tag.setAttribute("src","https://www.google.com/jsapi");
            if (script_tag.readyState) {
              script_tag.onreadystatechange = function () { // For old versions of IE
                  if (this.readyState == 'complete' || this.readyState == 'loaded') {
                      mapsLoadHandler();
                  }
              };
            } else {
              script_tag.onload = mapsLoadHandler;
            }
            // Try to find the head, otherwise default to the documentElement
            (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(script_tag);
        }
    }

    /******** do loading of google maps ********/
    function mapsLoadHandler() {
        google = window.google;
        google.load("maps", "3", { "other_params":"sensor=false", callback: function () { main(); }});
    }

    /******** Our main function ********/
    function main() {

        jQuery(document).ready(function($) {

            /******* Load internal CSS style sheet*******/
            var css_link = $("<link>", {
                rel: "stylesheet",
                type: "text/css",
                href: '"""+THIS_URL+"""?wtype=css'
            });
            css_link.appendTo('head');    

            allLoaded($); 

        });
    }
    
    // subroutine to do the main work of populating the map or list
    function allLoaded($) {

        if ($("#pa-widget-container").length > 0) {

            /** Create a default full UK wide map **/
            var mapTypeIds = [];
            for(var type in google.maps.MapTypeId) {
                mapTypeIds.push(google.maps.MapTypeId[type]);
            }
            mapTypeIds.push("OSM");
            var mapOptions = { "mapTypeId": google.maps.MapTypeId.ROADMAP,
                mapTypeControlOptions: { mapTypeIds: mapTypeIds },
                "zoom": 5, "center": new google.maps.LatLng(54.5, -2.8) };
            widgetMap = new google.maps.Map(document.getElementById("pa-widget-container"), mapOptions);
            infoWindow = new google.maps.InfoWindow(); // one window used for all popups
            ukRegion = new google.maps.LatLngBounds(new google.maps.LatLng(49.0, -10.0), new google.maps.LatLng(62.0, 3.0));
    
            /* handler for OSM map type */
            widgetMap.mapTypes.set("OSM", new google.maps.ImageMapType({
                getTileUrl: function(coord, zoom) {
                    return "http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";
                },
                tileSize: new google.maps.Size(256, 256),
                name: "OpenStreetMap",
                maxZoom: 18
            }));

        }
                    
        /******* Now load the map markers data via JSONP *******/
        var dataurl = '"""+JSONP_URL+"""';
        $.ajax({url:dataurl, dataType: "jsonp", data: """+DATA_QUERY+""", timeout: 30000,
            success:function(values) {
                if (values.applications === undefined) {
                    alert('No planning applications data found');
                }
                var planlist = values.applications.application;
                if (planlist.length > 0) {
                    var num_points = planlist.length;

                    if ($("#pa-widget-container").length > 0) {

                        var latlngbounds = new google.maps.LatLngBounds();
                        var total_lat = 0.0;
                        var total_lng = 0.0;
                        var added = 0;
                        for (var i = 0; i < num_points; i++) {
                            addMarker(planlist[i]); // pos atribute is set in addMarker
                            if (planlist[i].pos !== undefined && ukRegion.contains(planlist[i].pos)) { // only within UK
                                total_lat = total_lat + planlist[i].pos.lat();
                                total_lng = total_lng + planlist[i].pos.lng();
                                latlngbounds.extend(planlist[i].pos);
                                added += 1;
                            }
                        }
                        widgetMap.setCenter(new google.maps.LatLng(total_lat/added, total_lng/added)); // centroid  
                        //google.maps.event.addListenerOnce(widgetMap, 'zoom_changed', function(event) {
                        //        if (this.getZoom() < 8) { // don't zoom out beyond 8
                        //            this.setZoom(8);
                        //        }
                        //});
                        widgetMap.fitBounds(latlngbounds);

                    }

                    if ($("#pa-widget-block").length > 0) {

                        var tag = '<dl>';
                        var planinfo;
                        for (var i = 0; i < num_points; i++) {
                            planinfo = planlist[i];
                            tag += '<dt><strong>'+planinfo.address+'</strong></dt>'+
                                '<dd>'+planinfo.description+'<br />'+
                                'Planning authority: '+planinfo.authority_long_name+'<br />'+
                                'Reference: '+
                                '<a href="'+planinfo.info_url+'" target="_blank">'+
                                planinfo.reference+'</a>';
                            if (planinfo.received_date) {
                                tag += '<br />Date received: '+showDate(planinfo.received_date); }
                            else if (planinfo.validated_date) {
                                tag += '<br />Date validated: '+showDate(planinfo.validated_date); }
                            tag += '</dd>';
                        }
                        tag += '</dl>';

                        $('#pa-widget-block').html(tag);

                    }

                } else {
                    alert('Zero planning applications returned');
                }
            },
            error:function(object, status) {
                alert('Failed to retrieve any planning applications ('+status+')');
            }
        });

    }


    /******** helper functions ********/
    function addMarker(planinfo)
    {
        if (!planinfo['lat'] || !planinfo['lng']) return false;
        var lat = planinfo['lat'] + ((Math.random()*2-1)/11100);
        var lng = planinfo['lng'] + ((Math.random()*2-1)/7000);
        // adds a random value equiv to approx +-10m in case multiple markers are on one spot
        planinfo.pos = new google.maps.LatLng(lat, lng);
        var letter = planinfo.authority.substr(0,1);
        var index = String.charCodeAt(letter) % 9;
        var lt2 = letter+planinfo.authority.substr(3,1);
        var col = mapColours[index]; // add colour here based on authority first letter
        planinfo.icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+lt2+'|'+col+'|000000';
        planinfo.marker = new google.maps.Marker({position:planinfo.pos, map:widgetMap, title:planinfo.address, icon:planinfo.icon});
        google.maps.event.addListener(planinfo.marker, "click", function()
        {
            var msg = '';
            if (planinfo.received_date) msg = 'Date received: '+showDate(planinfo.received_date)+'<br />';
            else if (planinfo.validated_date) msg = 'Date validated: '+showDate(planinfo.validated_date)+'<br />';
            infoWindow.setContent('<div><strong>'+planinfo.address+'</strong></div>'+
                    '<div>'+planinfo.description+'</div>'+
                    '<div>Planning authority: '+planinfo.authority_long_name+'<br />'+
                    'Reference: '+
                    '<a href="'+planinfo.info_url+'" target="_blank">'+planinfo.reference+'</a><br />'+
                    msg+
                    'Postcode: '+
                    planinfo.postcode+'</div>'
            );
            infoWindow.open(widgetMap, planinfo.marker);
        });
        return true;
    }

    function showDate(in_date) { // outputs formatted date
        if (!in_date) return 'Empty date';
        if (checkDate(in_date)) return in_date+'(dmy)';
        var dt_bits =  match_in_date.exec(in_date);
        if (!dt_bits) {
            return 'Wrong date format';
        } else if (dt_bits.length == 4) {
            return dt_bits[3]+'/'+dt_bits[2]+'/'+dt_bits[1];
        } else {
            return 'Date not matched';
        }
    }

    function checkDate(at_date) { // checks date parameter is supplied in dd/mm/yyyy format
        var dt_match =  at_date.match(match_at_date);
        if (dt_match) {
            return true;
        } else {
            return false;
        }
    }
    
    })(); // We call our main anonymous function immediately
    
    """


