<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
</head>

<body>

<h2>Map of oil wells from data sourced from <a href="https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell">here</a></h2>

<p>Early version of new oil well map using vast numbers of undocumented features.  
Have a look but don't be discouraged if you don't understand it, because we need to make this more user friendly.
    <b>Click on year to load all the wells positions in that year.</b>
Wanted: some fancy-schmancy interface where I can animate these things over time to track the rigs 
as they float from place to place.</p>

<p>The raw pages are downloaded by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_scrapedownload/">northsea_oilwell_scrapedownload</a>. 
The pages are parsed into proper database format by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_parse/">northsea_oilwell_parse</a>.
The data is served out to this front end script by ajax from the viewer: <a href="http://scraperwiki.com/views/northsea_oilwell_server/">northsea_oilwell_server</a>.</p>



<b class="cyear" style="color:blue">1980</b>
<b class="cyear" style="color:blue">1981</b>
<b class="cyear" style="color:blue">1982</b>
<b class="cyear" style="color:blue">1983</b>
<b class="cyear" style="color:blue">1984</b>
<b class="cyear" style="color:blue">1985</b>
<b class="cyear" style="color:blue">1986</b>
<b class="cyear" style="color:blue">1987</b>
<b class="cyear" style="color:blue">1988</b>
<b class="cyear" style="color:blue">1989</b>
<b class="cyear" style="color:blue">1990</b>
<span id="message"></span>

<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
    
var sourcescraper = 'northsea_oilwell_parse';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    

var map; 
function makemap()
{
    var mapOptions = { "zoom": 6, "center": new google.maps.LatLng(55.500515, -4.128317), 
                       "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function putpin(lat, lng, status)
{
    var pos = new google.maps.LatLng(lat, lng); 
    var letter = "N"; 
    var col="f00"; 
    if (status == "Abandoned")
        letter = "A"; 
    if (status == "Completed")
        col = "0f0"; 
    var icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'; 
    var marker = new google.maps.Marker({position:pos, map:map, icon:icon});
}

var nwdata = [ ]; 
function slowupdate()
{
    if (nwdata.length == 0)
        return; 
    var nwd = nwdata.shift(); 
    putpin(nwd[0], nwd[1], nwd[2]); 
    setTimeout(slowupdate, 100); 
}


var apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite"; 
var sourcename = "north_sea_oil_wells";

$(function() 
{ 
    makemap(); 
    $(".cyear").click(function() 
    {
        $(this).css("background", "#aaa"); 
        $("#message").text("loading"); 
        var year = $(this).text(); 
        var sqlselect = "select tophole_lat, tophole_lng, `Completion Status` from wellpages where substr(`Spud Date`,0,5)='"+year+"' order by `Spud Date`";
        $.ajax({url:apiurl, dataType: "jsonp", data:{name:sourcename, query:sqlselect, format:"jsonlist"}, success:function(tdata)
        {
            nwdata = tdata.data; 
console.log(nwdata);
            $("#message").text("loaded "+nwdata.length+" records"); 
            slowupdate(); 
        }})
    }); 
});

</script> 
</body> 
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
</head>

<body>

<h2>Map of oil wells from data sourced from <a href="https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell">here</a></h2>

<p>Early version of new oil well map using vast numbers of undocumented features.  
Have a look but don't be discouraged if you don't understand it, because we need to make this more user friendly.
    <b>Click on year to load all the wells positions in that year.</b>
Wanted: some fancy-schmancy interface where I can animate these things over time to track the rigs 
as they float from place to place.</p>

<p>The raw pages are downloaded by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_scrapedownload/">northsea_oilwell_scrapedownload</a>. 
The pages are parsed into proper database format by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_parse/">northsea_oilwell_parse</a>.
The data is served out to this front end script by ajax from the viewer: <a href="http://scraperwiki.com/views/northsea_oilwell_server/">northsea_oilwell_server</a>.</p>



<b class="cyear" style="color:blue">1980</b>
<b class="cyear" style="color:blue">1981</b>
<b class="cyear" style="color:blue">1982</b>
<b class="cyear" style="color:blue">1983</b>
<b class="cyear" style="color:blue">1984</b>
<b class="cyear" style="color:blue">1985</b>
<b class="cyear" style="color:blue">1986</b>
<b class="cyear" style="color:blue">1987</b>
<b class="cyear" style="color:blue">1988</b>
<b class="cyear" style="color:blue">1989</b>
<b class="cyear" style="color:blue">1990</b>
<span id="message"></span>

<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
    
var sourcescraper = 'northsea_oilwell_parse';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    

var map; 
function makemap()
{
    var mapOptions = { "zoom": 6, "center": new google.maps.LatLng(55.500515, -4.128317), 
                       "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function putpin(lat, lng, status)
{
    var pos = new google.maps.LatLng(lat, lng); 
    var letter = "N"; 
    var col="f00"; 
    if (status == "Abandoned")
        letter = "A"; 
    if (status == "Completed")
        col = "0f0"; 
    var icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'; 
    var marker = new google.maps.Marker({position:pos, map:map, icon:icon});
}

var nwdata = [ ]; 
function slowupdate()
{
    if (nwdata.length == 0)
        return; 
    var nwd = nwdata.shift(); 
    putpin(nwd[0], nwd[1], nwd[2]); 
    setTimeout(slowupdate, 100); 
}


var apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite"; 
var sourcename = "north_sea_oil_wells";

$(function() 
{ 
    makemap(); 
    $(".cyear").click(function() 
    {
        $(this).css("background", "#aaa"); 
        $("#message").text("loading"); 
        var year = $(this).text(); 
        var sqlselect = "select tophole_lat, tophole_lng, `Completion Status` from wellpages where substr(`Spud Date`,0,5)='"+year+"' order by `Spud Date`";
        $.ajax({url:apiurl, dataType: "jsonp", data:{name:sourcename, query:sqlselect, format:"jsonlist"}, success:function(tdata)
        {
            nwdata = tdata.data; 
console.log(nwdata);
            $("#message").text("loaded "+nwdata.length+" records"); 
            slowupdate(); 
        }})
    }); 
});

</script> 
</body> 
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
</head>

<body>

<h2>Map of oil wells from data sourced from <a href="https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell">here</a></h2>

<p>Early version of new oil well map using vast numbers of undocumented features.  
Have a look but don't be discouraged if you don't understand it, because we need to make this more user friendly.
    <b>Click on year to load all the wells positions in that year.</b>
Wanted: some fancy-schmancy interface where I can animate these things over time to track the rigs 
as they float from place to place.</p>

<p>The raw pages are downloaded by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_scrapedownload/">northsea_oilwell_scrapedownload</a>. 
The pages are parsed into proper database format by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_parse/">northsea_oilwell_parse</a>.
The data is served out to this front end script by ajax from the viewer: <a href="http://scraperwiki.com/views/northsea_oilwell_server/">northsea_oilwell_server</a>.</p>



<b class="cyear" style="color:blue">1980</b>
<b class="cyear" style="color:blue">1981</b>
<b class="cyear" style="color:blue">1982</b>
<b class="cyear" style="color:blue">1983</b>
<b class="cyear" style="color:blue">1984</b>
<b class="cyear" style="color:blue">1985</b>
<b class="cyear" style="color:blue">1986</b>
<b class="cyear" style="color:blue">1987</b>
<b class="cyear" style="color:blue">1988</b>
<b class="cyear" style="color:blue">1989</b>
<b class="cyear" style="color:blue">1990</b>
<span id="message"></span>

<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
    
var sourcescraper = 'northsea_oilwell_parse';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    

var map; 
function makemap()
{
    var mapOptions = { "zoom": 6, "center": new google.maps.LatLng(55.500515, -4.128317), 
                       "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function putpin(lat, lng, status)
{
    var pos = new google.maps.LatLng(lat, lng); 
    var letter = "N"; 
    var col="f00"; 
    if (status == "Abandoned")
        letter = "A"; 
    if (status == "Completed")
        col = "0f0"; 
    var icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'; 
    var marker = new google.maps.Marker({position:pos, map:map, icon:icon});
}

var nwdata = [ ]; 
function slowupdate()
{
    if (nwdata.length == 0)
        return; 
    var nwd = nwdata.shift(); 
    putpin(nwd[0], nwd[1], nwd[2]); 
    setTimeout(slowupdate, 100); 
}


var apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite"; 
var sourcename = "north_sea_oil_wells";

$(function() 
{ 
    makemap(); 
    $(".cyear").click(function() 
    {
        $(this).css("background", "#aaa"); 
        $("#message").text("loading"); 
        var year = $(this).text(); 
        var sqlselect = "select tophole_lat, tophole_lng, `Completion Status` from wellpages where substr(`Spud Date`,0,5)='"+year+"' order by `Spud Date`";
        $.ajax({url:apiurl, dataType: "jsonp", data:{name:sourcename, query:sqlselect, format:"jsonlist"}, success:function(tdata)
        {
            nwdata = tdata.data; 
console.log(nwdata);
            $("#message").text("loaded "+nwdata.length+" records"); 
            slowupdate(); 
        }})
    }); 
});

</script> 
</body> 
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
</head>

<body>

<h2>Map of oil wells from data sourced from <a href="https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell">here</a></h2>

<p>Early version of new oil well map using vast numbers of undocumented features.  
Have a look but don't be discouraged if you don't understand it, because we need to make this more user friendly.
    <b>Click on year to load all the wells positions in that year.</b>
Wanted: some fancy-schmancy interface where I can animate these things over time to track the rigs 
as they float from place to place.</p>

<p>The raw pages are downloaded by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_scrapedownload/">northsea_oilwell_scrapedownload</a>. 
The pages are parsed into proper database format by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_parse/">northsea_oilwell_parse</a>.
The data is served out to this front end script by ajax from the viewer: <a href="http://scraperwiki.com/views/northsea_oilwell_server/">northsea_oilwell_server</a>.</p>



<b class="cyear" style="color:blue">1980</b>
<b class="cyear" style="color:blue">1981</b>
<b class="cyear" style="color:blue">1982</b>
<b class="cyear" style="color:blue">1983</b>
<b class="cyear" style="color:blue">1984</b>
<b class="cyear" style="color:blue">1985</b>
<b class="cyear" style="color:blue">1986</b>
<b class="cyear" style="color:blue">1987</b>
<b class="cyear" style="color:blue">1988</b>
<b class="cyear" style="color:blue">1989</b>
<b class="cyear" style="color:blue">1990</b>
<span id="message"></span>

<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
    
var sourcescraper = 'northsea_oilwell_parse';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    

var map; 
function makemap()
{
    var mapOptions = { "zoom": 6, "center": new google.maps.LatLng(55.500515, -4.128317), 
                       "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function putpin(lat, lng, status)
{
    var pos = new google.maps.LatLng(lat, lng); 
    var letter = "N"; 
    var col="f00"; 
    if (status == "Abandoned")
        letter = "A"; 
    if (status == "Completed")
        col = "0f0"; 
    var icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'; 
    var marker = new google.maps.Marker({position:pos, map:map, icon:icon});
}

var nwdata = [ ]; 
function slowupdate()
{
    if (nwdata.length == 0)
        return; 
    var nwd = nwdata.shift(); 
    putpin(nwd[0], nwd[1], nwd[2]); 
    setTimeout(slowupdate, 100); 
}


var apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite"; 
var sourcename = "north_sea_oil_wells";

$(function() 
{ 
    makemap(); 
    $(".cyear").click(function() 
    {
        $(this).css("background", "#aaa"); 
        $("#message").text("loading"); 
        var year = $(this).text(); 
        var sqlselect = "select tophole_lat, tophole_lng, `Completion Status` from wellpages where substr(`Spud Date`,0,5)='"+year+"' order by `Spud Date`";
        $.ajax({url:apiurl, dataType: "jsonp", data:{name:sourcename, query:sqlselect, format:"jsonlist"}, success:function(tdata)
        {
            nwdata = tdata.data; 
console.log(nwdata);
            $("#message").text("loaded "+nwdata.length+" records"); 
            slowupdate(); 
        }})
    }); 
});

</script> 
</body> 
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
</head>

<body>

<h2>Map of oil wells from data sourced from <a href="https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell">here</a></h2>

<p>Early version of new oil well map using vast numbers of undocumented features.  
Have a look but don't be discouraged if you don't understand it, because we need to make this more user friendly.
    <b>Click on year to load all the wells positions in that year.</b>
Wanted: some fancy-schmancy interface where I can animate these things over time to track the rigs 
as they float from place to place.</p>

<p>The raw pages are downloaded by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_scrapedownload/">northsea_oilwell_scrapedownload</a>. 
The pages are parsed into proper database format by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_parse/">northsea_oilwell_parse</a>.
The data is served out to this front end script by ajax from the viewer: <a href="http://scraperwiki.com/views/northsea_oilwell_server/">northsea_oilwell_server</a>.</p>



<b class="cyear" style="color:blue">1980</b>
<b class="cyear" style="color:blue">1981</b>
<b class="cyear" style="color:blue">1982</b>
<b class="cyear" style="color:blue">1983</b>
<b class="cyear" style="color:blue">1984</b>
<b class="cyear" style="color:blue">1985</b>
<b class="cyear" style="color:blue">1986</b>
<b class="cyear" style="color:blue">1987</b>
<b class="cyear" style="color:blue">1988</b>
<b class="cyear" style="color:blue">1989</b>
<b class="cyear" style="color:blue">1990</b>
<span id="message"></span>

<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
    
var sourcescraper = 'northsea_oilwell_parse';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    

var map; 
function makemap()
{
    var mapOptions = { "zoom": 6, "center": new google.maps.LatLng(55.500515, -4.128317), 
                       "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function putpin(lat, lng, status)
{
    var pos = new google.maps.LatLng(lat, lng); 
    var letter = "N"; 
    var col="f00"; 
    if (status == "Abandoned")
        letter = "A"; 
    if (status == "Completed")
        col = "0f0"; 
    var icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'; 
    var marker = new google.maps.Marker({position:pos, map:map, icon:icon});
}

var nwdata = [ ]; 
function slowupdate()
{
    if (nwdata.length == 0)
        return; 
    var nwd = nwdata.shift(); 
    putpin(nwd[0], nwd[1], nwd[2]); 
    setTimeout(slowupdate, 100); 
}


var apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite"; 
var sourcename = "north_sea_oil_wells";

$(function() 
{ 
    makemap(); 
    $(".cyear").click(function() 
    {
        $(this).css("background", "#aaa"); 
        $("#message").text("loading"); 
        var year = $(this).text(); 
        var sqlselect = "select tophole_lat, tophole_lng, `Completion Status` from wellpages where substr(`Spud Date`,0,5)='"+year+"' order by `Spud Date`";
        $.ajax({url:apiurl, dataType: "jsonp", data:{name:sourcename, query:sqlselect, format:"jsonlist"}, success:function(tdata)
        {
            nwdata = tdata.data; 
console.log(nwdata);
            $("#message").text("loaded "+nwdata.length+" records"); 
            slowupdate(); 
        }})
    }); 
});

</script> 
</body> 
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
</head>

<body>

<h2>Map of oil wells from data sourced from <a href="https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell">here</a></h2>

<p>Early version of new oil well map using vast numbers of undocumented features.  
Have a look but don't be discouraged if you don't understand it, because we need to make this more user friendly.
    <b>Click on year to load all the wells positions in that year.</b>
Wanted: some fancy-schmancy interface where I can animate these things over time to track the rigs 
as they float from place to place.</p>

<p>The raw pages are downloaded by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_scrapedownload/">northsea_oilwell_scrapedownload</a>. 
The pages are parsed into proper database format by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_parse/">northsea_oilwell_parse</a>.
The data is served out to this front end script by ajax from the viewer: <a href="http://scraperwiki.com/views/northsea_oilwell_server/">northsea_oilwell_server</a>.</p>



<b class="cyear" style="color:blue">1980</b>
<b class="cyear" style="color:blue">1981</b>
<b class="cyear" style="color:blue">1982</b>
<b class="cyear" style="color:blue">1983</b>
<b class="cyear" style="color:blue">1984</b>
<b class="cyear" style="color:blue">1985</b>
<b class="cyear" style="color:blue">1986</b>
<b class="cyear" style="color:blue">1987</b>
<b class="cyear" style="color:blue">1988</b>
<b class="cyear" style="color:blue">1989</b>
<b class="cyear" style="color:blue">1990</b>
<span id="message"></span>

<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
    
var sourcescraper = 'northsea_oilwell_parse';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    

var map; 
function makemap()
{
    var mapOptions = { "zoom": 6, "center": new google.maps.LatLng(55.500515, -4.128317), 
                       "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function putpin(lat, lng, status)
{
    var pos = new google.maps.LatLng(lat, lng); 
    var letter = "N"; 
    var col="f00"; 
    if (status == "Abandoned")
        letter = "A"; 
    if (status == "Completed")
        col = "0f0"; 
    var icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'; 
    var marker = new google.maps.Marker({position:pos, map:map, icon:icon});
}

var nwdata = [ ]; 
function slowupdate()
{
    if (nwdata.length == 0)
        return; 
    var nwd = nwdata.shift(); 
    putpin(nwd[0], nwd[1], nwd[2]); 
    setTimeout(slowupdate, 100); 
}


var apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite"; 
var sourcename = "north_sea_oil_wells";

$(function() 
{ 
    makemap(); 
    $(".cyear").click(function() 
    {
        $(this).css("background", "#aaa"); 
        $("#message").text("loading"); 
        var year = $(this).text(); 
        var sqlselect = "select tophole_lat, tophole_lng, `Completion Status` from wellpages where substr(`Spud Date`,0,5)='"+year+"' order by `Spud Date`";
        $.ajax({url:apiurl, dataType: "jsonp", data:{name:sourcename, query:sqlselect, format:"jsonlist"}, success:function(tdata)
        {
            nwdata = tdata.data; 
console.log(nwdata);
            $("#message").text("loaded "+nwdata.length+" records"); 
            slowupdate(); 
        }})
    }); 
});

</script> 
</body> 
</html><html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>General Map Thing</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
</head>

<body>

<h2>Map of oil wells from data sourced from <a href="https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell">here</a></h2>

<p>Early version of new oil well map using vast numbers of undocumented features.  
Have a look but don't be discouraged if you don't understand it, because we need to make this more user friendly.
    <b>Click on year to load all the wells positions in that year.</b>
Wanted: some fancy-schmancy interface where I can animate these things over time to track the rigs 
as they float from place to place.</p>

<p>The raw pages are downloaded by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_scrapedownload/">northsea_oilwell_scrapedownload</a>. 
The pages are parsed into proper database format by the scraper: <a href="http://scraperwiki.com/scrapers/northsea_oilwell_parse/">northsea_oilwell_parse</a>.
The data is served out to this front end script by ajax from the viewer: <a href="http://scraperwiki.com/views/northsea_oilwell_server/">northsea_oilwell_server</a>.</p>



<b class="cyear" style="color:blue">1980</b>
<b class="cyear" style="color:blue">1981</b>
<b class="cyear" style="color:blue">1982</b>
<b class="cyear" style="color:blue">1983</b>
<b class="cyear" style="color:blue">1984</b>
<b class="cyear" style="color:blue">1985</b>
<b class="cyear" style="color:blue">1986</b>
<b class="cyear" style="color:blue">1987</b>
<b class="cyear" style="color:blue">1988</b>
<b class="cyear" style="color:blue">1989</b>
<b class="cyear" style="color:blue">1990</b>
<span id="message"></span>

<div id="map" style="width:100%;height:400px"></div>

<script type="text/javascript" charset="utf-8">
    
var sourcescraper = 'northsea_oilwell_parse';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    

var map; 
function makemap()
{
    var mapOptions = { "zoom": 6, "center": new google.maps.LatLng(55.500515, -4.128317), 
                       "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function putpin(lat, lng, status)
{
    var pos = new google.maps.LatLng(lat, lng); 
    var letter = "N"; 
    var col="f00"; 
    if (status == "Abandoned")
        letter = "A"; 
    if (status == "Completed")
        col = "0f0"; 
    var icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000'; 
    var marker = new google.maps.Marker({position:pos, map:map, icon:icon});
}

var nwdata = [ ]; 
function slowupdate()
{
    if (nwdata.length == 0)
        return; 
    var nwd = nwdata.shift(); 
    putpin(nwd[0], nwd[1], nwd[2]); 
    setTimeout(slowupdate, 100); 
}


var apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite"; 
var sourcename = "north_sea_oil_wells";

$(function() 
{ 
    makemap(); 
    $(".cyear").click(function() 
    {
        $(this).css("background", "#aaa"); 
        $("#message").text("loading"); 
        var year = $(this).text(); 
        var sqlselect = "select tophole_lat, tophole_lng, `Completion Status` from wellpages where substr(`Spud Date`,0,5)='"+year+"' order by `Spud Date`";
        $.ajax({url:apiurl, dataType: "jsonp", data:{name:sourcename, query:sqlselect, format:"jsonlist"}, success:function(tdata)
        {
            nwdata = tdata.data; 
console.log(nwdata);
            $("#message").text("loaded "+nwdata.length+" records"); 
            slowupdate(); 
        }})
    }); 
});

</script> 
</body> 
</html>