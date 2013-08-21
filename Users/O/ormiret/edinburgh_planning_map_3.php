<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Leith Planning Applications Map</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    
    <style>
        .info-box {
            width: 220px;
            padding: 10px;
            background: #f2f2f2;
            -moz-border-radius: 5px;
            -webkit-border-radius: 5px;
            border-radius: 5px;
            float: left;
        }
        
        h1, p, a {
            font-family: 'Helvetica Neue', Helvetica, arial, verdana, sans-serif;
            color: #333;
        }
        
        h1 {
            font-size: 14px;
            line-height: 17px;
            margin: 0 0 10px 0;
        }
        
        p {
            color: #555;
            font-size: 12px;
            line-height: 15px;
            margin: 0 0 15px 0;
        }
        
        .meta p {
            font-size: 11px;
            line-height: 14px;
            color: #999;
        }
        
        .meta {
            width: 230px;
            margin: 0 0 0 -10px;
            float: left;
        }
        
        .col {
            width: 105px;
            float: left;
            margin: 0 0 0 10px;
        }
        
        .read-more-button, .read-more-button:visited {
            float: left;
            color: #fff;
            font-size: 12px;
            line-height: 12px;
            font-weight: bold;
            text-decoration: none;
            background: #555;
            padding: 5px 5px 6px 5px;
            display: block;
            width: 70px;
            margin: 0 0 5px 0;
            text-align: center;
            -moz-border-radius: 5px;
            -webkit-border-radius: 5px;
            border-radius: 5px;
        }
        
        .read-more-button:hover { background: #54d8b4; }
    </style>
</head>

<body>

<div id="map" style="width:100%;height:100%;margin-top:30px"></div>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.  You should edit the functions below 
// so that your map expresses the particular contents of the data
// ####################################################################
    
var sourcescraper = 'edinburgh_planning_applications';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{
    col = 'D85454';
    if (record["status"] == "Application Approved")
    {
        col = '54B8B4';
    } 
    else if(record["status"] == "Application Refused")
    {
        col = 'D85454';
    }
    
    //letter = record["Validated"].charAt(3);        
    letter = "A"
     
    icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld='+letter+'|'+col+'|000';
    return icon
}

// ####################################################################
// Set the tooltip title value
// ####################################################################
function mapicontext(record)
{
    return "Ref No. "+record['ref']+", Date. "+record['date received'];
}

// ####################################################################
// Set the popup text for your pin, usually with the link
// ####################################################################
function mapicontent(record)
{
    return '<div class="info-box"><h1>'+record["proposal"]+'</h1><div class="meta"><div class="col"><p><b>Date: </b>'+record["date received"]+'<br /><b>Status: </b>'+record["status"]+'<br /><b>Ref. Code: </b>'+record["ref"]+'</p></div><div class="col"><p><b>Address: </b><br />'+record["address"]+'<br /></p></div></div><a href="http://citydev-portal.edinburgh.gov.uk/publicaccess/tdc/DcApplication/application_detailview.aspx?caseno='+record["detail"]+'&searchtype=HOURLY" title="More information about '+record["ref"]+'" class="read-more-button">Read more <span class="info-icon"></span></a></div>';
}

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 14, "center": new google.maps.LatLng(55.9646449, -3.1818169), 
                    "mapTypeId": google.maps.MapTypeId.HYBRID };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}
 
function recorddata(record)
{
    pos = new google.maps.LatLng(record['lat'], record['lng']); 

    text = mapicontext(record);
    icon = mapicon(record);
    content = mapicontent(record); 
    marker = new google.maps.Marker({position:pos,map:map,title:text, icon:icon});

    infowindow = new google.maps.InfoWindow({ content: content });
        (function(j) {
                google.maps.event.addListener(j.marker, "click", function(){
                                j.infowindow.open(map, j.marker); });
                 })({'marker':marker, 'infowindow':infowindow});
}

var olength = 200; 
var olimit = 100; 
var offset = 0;

function gotback(r) 
{
    // alert(r)

    for (i = 0; i < r.length; i++)
    {
        recorddata(r[i]); 
        // alert("Record "+ i);
    }

    offset += olength; 
    if ((r.length == olength) && (offset < olimit))
        loaddata(); 
}

function loaddata() 
{
    var s = document.createElement('script');
    // url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+sourcescraper+"&limit="+olength+"&callback=gotback&offset=" + offset;
    // url = "http://scraperwikiviews.com/run/edinburgh_planning_application_json_view/"
    url = "http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=edinburgh_planning_applications&query=select%20*%20from%20swdata%20order%20by%20date_scraped%20desc&callback=gotback"
    // alert(url);
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

</script> 
</body> 
</html>