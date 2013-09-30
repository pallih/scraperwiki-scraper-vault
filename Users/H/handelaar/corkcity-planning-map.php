<html>
<head>
    <script src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/main.css" />
    <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
    <script>
    var map;
    var infowindow;
    function makemap() {
        var cpos = new google.maps.LatLng(51.900700113936,-8.472561836243);
        var mapOptions = { "zoom": 12, "center": cpos, "mapTypeId": google.maps.MapTypeId.ROADMAP };
        map = new google.maps.Map(document.getElementById("mapdiv"), mapOptions);
        var infowindow = new google.maps.InfoWindow({
            content: ""
        });
    }
    $(window).ready(function() {
        makemap();
        pos = new google.maps.LatLng(51.900700113936,-8.472561836243);
        infowindow = new google.maps.InfoWindow();
        var icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=X|0f0|f0f';
        //var marker = new google.maps.Marker({position:pos, map:map, icon:icon, animation: google.maps.Animation.DROP, title:"title message"});
        //google.maps.event.addListener(marker, "click", function() { alert(this.icon); });
        var sourcename = "ie_planningalerts_corkcity";
        var apiurl = "http://api.scraperwiki.com/api/1.0/datastore/sqlite";
        var sqlselect = "select latitude, longitude, appref, url, address from swdata order by appref";
        var icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=X|0f0|f0f';
        
        $.ajax({url:apiurl, dataType: "jsonp", data:{name:sourcename, query:sqlselect, format:"jsonlist"}, success:function(tdata) {
            var data = tdata.data;
            for (var i = 0; i < data.length; i++){
                buildMarker(data[i]);
            }
        }})
    });
    function buildMarker(data){
        var marker = new google.maps.Marker({position:new google.maps.LatLng(data[0], data[1]), map:map});
        
        var html = "<a href='"+data[3]+"'>"+data[2]+"</a><br />"+data[4]
        google.maps.event.addListener(marker, 'click', function() {
            infowindow.setContent(html);
            infowindow.open(map,marker);
        });
    }
    </script>

</head>
<body>
<h1>Planning Applications to Cork City Council</h1>
<h2>(Since approximately May 10th 2010)</h2>
<div id="mapdiv" style="width:800px;height:500px;margin:0px auto;"></div>
</body>
</html>


<html>
<head>
    <script src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/main.css" />
    <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
    <script>
    var map;
    var infowindow;
    function makemap() {
        var cpos = new google.maps.LatLng(51.900700113936,-8.472561836243);
        var mapOptions = { "zoom": 12, "center": cpos, "mapTypeId": google.maps.MapTypeId.ROADMAP };
        map = new google.maps.Map(document.getElementById("mapdiv"), mapOptions);
        var infowindow = new google.maps.InfoWindow({
            content: ""
        });
    }
    $(window).ready(function() {
        makemap();
        pos = new google.maps.LatLng(51.900700113936,-8.472561836243);
        infowindow = new google.maps.InfoWindow();
        var icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=X|0f0|f0f';
        //var marker = new google.maps.Marker({position:pos, map:map, icon:icon, animation: google.maps.Animation.DROP, title:"title message"});
        //google.maps.event.addListener(marker, "click", function() { alert(this.icon); });
        var sourcename = "ie_planningalerts_corkcity";
        var apiurl = "http://api.scraperwiki.com/api/1.0/datastore/sqlite";
        var sqlselect = "select latitude, longitude, appref, url, address from swdata order by appref";
        var icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=X|0f0|f0f';
        
        $.ajax({url:apiurl, dataType: "jsonp", data:{name:sourcename, query:sqlselect, format:"jsonlist"}, success:function(tdata) {
            var data = tdata.data;
            for (var i = 0; i < data.length; i++){
                buildMarker(data[i]);
            }
        }})
    });
    function buildMarker(data){
        var marker = new google.maps.Marker({position:new google.maps.LatLng(data[0], data[1]), map:map});
        
        var html = "<a href='"+data[3]+"'>"+data[2]+"</a><br />"+data[4]
        google.maps.event.addListener(marker, 'click', function() {
            infowindow.setContent(html);
            infowindow.open(map,marker);
        });
    }
    </script>

</head>
<body>
<h1>Planning Applications to Cork City Council</h1>
<h2>(Since approximately May 10th 2010)</h2>
<div id="mapdiv" style="width:800px;height:500px;margin:0px auto;"></div>
</body>
</html>


