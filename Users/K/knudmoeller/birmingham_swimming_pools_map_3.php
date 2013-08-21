<!-- 
    Knud Möller, 2011
    The code for this view is based on https://scraperwiki.com/views/corkcity-planning-map/.
-->
<html>
<head>
    <title>Birmingham Swimming Pools | Scraper Wiki</title>
    <script src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
    <script>
    var map;
    var infowindow;
    function makemap() {
        var cpos = new google.maps.LatLng(52.483381, -1.893489);
        var mapOptions = { "zoom": 12, "center": cpos, "mapTypeId": google.maps.MapTypeId.ROADMAP };
        map = new google.maps.Map(document.getElementById("mapdiv"), mapOptions);
        var infowindow = new google.maps.InfoWindow({
            content: ""
        });
    }
    $(window).ready(function() {
        makemap();
        infowindow = new google.maps.InfoWindow();
        var icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=X|0f0|f0f';
        var sourcename = "birmingham_swimming_pools";
        var apiurl = "http://api.scraperwiki.com/api/1.0/datastore/sqlite";
        var sqlselect = "select lat, long, name, address, website from swdata";
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
        
        var html = "<a href='"+data[4]+"' target='_blank'>"+data[2]+"</a><br /> ("+data[3]+")";
        google.maps.event.addListener(marker, 'click', function() {
            infowindow.setContent(html);
            infowindow.open(map,marker);
        });
    }
    </script>

</head>
<body style="background: #E6E6DC; color: #00628B;">
<div style="height:30px">&nbsp;</div>
<div id="mapdiv" style="width:430px;height:430px;margin:10px auto;border: 2px #81A594 solid; background: #FFFFFF;"></div>
</body>
</html>

