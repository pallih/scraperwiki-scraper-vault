<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Garages to Rent in Oxford</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>

<body>

<h2>Map of <span id="scrapername">...</span> <em id="message">...</em></h2>

    This map shows <a href="http://www.oxford.gov.uk/PageRender/decH/Garages_to_rent_occw.htm">Council Garages to Rent from Oxford City Council</a>. The green bubbles indicate sites with Garages available (according to the <a href="http://www.oxford.gov.uk/PageRender/decH/Garages_to_rent_occw.htm">OCC Website</a>) and the number in the bubble is how many Garages. 
    The data is scraped daily using <A href="http://www.scraperwiki.com">Scraper Wiki</a>. This was built by <a href="http://www.twitter.com/timdavies">Tim Davies</a> as a demonstration for <A href="http://www.opendataday.org/wiki/Oxford,_UK">Oxford Open Data Day</a> and the Open Data Cook Book.

    <div id="map" style="width:100%;height:800px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'oxford-garages-to-rent';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{

    letter = record['Number_of_garages_available_to_let_now_at_this_site'];
    if(letter > 0) { col='0F0' } else { col = 'F00'}     
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return "TOOLTIP " + record["Site_location"] 
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<a href="'+record['source']+'" target="_blank">'+record["Site_location"]+'</a><br/><img src="'+record['image']+'" width="150">';
}

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 12, "center": new google.maps.LatLng(55.500515, -4.128317), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(record)
{
    if (!(record['latlng_lat']))
        return; 
    pos = new google.maps.LatLng(record['latlng_lat'], record['latlng_lng']); 

    text = mapicontext(record);
    icon = mapicon(record);
    content = mapicontent(record); 

    marker = new google.maps.Marker({position:pos,map:map,title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
    (function(j) {
            google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
    if (!centreset)
        {  map.setCenter(pos); centreset = true }
}

var olength = 500; 
var olimit = 100; 
var offset = 0; 1    
function gotback(r) 
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]); 

    offset += olength; 
    if ((r.length == olength) && (offset < olimit))
        loaddata(); 
    else
        $("#message").html("Total records=" + (offset - olength + r.length)); 
}

function loaddata() 
{
    $("#message").html("Loading ..."); 
    var s = document.createElement('script');
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+sourcescraper+"&limit="+olength+"&callback=gotback&offset=" + offset;
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

</script> 
</body> 
</html>