<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Edinburgh Planning Applications Map</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    
    <style>
        #info-box {
            width: 220px;
            padding: 10px;
            background: #f2f2f2;
            -moz-border-radius: 5px;
            -webkit-border-radius: 5px;
            border-radius: 5px;
            float: left;
        }
        #key-overlay {

                min-width: 100px;  
                border: 1px solid #000; 
                background-color:#ddd; 
                padding:10px; position:absolute;
                right:50px; 
                bottom:30px; 
                border-radius:5px;

        }

        .key-text {
                font-family: "Arial", sans;
                font-weight:bold;
                display:inline-block;
                position:relative;
                margin:-10px 0 0 0;
                font-size:.9em 
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
    var letter = "?";


    if (record["status"] == "Status: Pending Consideration")
    {
        col = 'FF6600';
        letter = "P";
    } 

    else if (record["status"] == "Pending Consideration")
    {
        col = 'FF6600';
        letter = "P";
    } 

    else if (record["status"] == "Status: Application Approved")
    {
        col = '66FF33';
        letter = "A";
    }
 
    else if (record["status"] == "Proposal Does Not Constitute Development")
    {
        col = '66FF33';
        letter = "A";
    }

    else if (record["status"] == "Status: Proposal Does Not Constitute Development")
    {
        col = '66FF33';
        letter = "A";
    }


    else if (record["status"] == "Permission Not Required")
    {
        col = '66FF33';
        letter = "A";
    }

    else if(record["status"] == "Status: Application Granted")
    {
        col = '66FF33';
        letter = "A";
    }

    else if(record["status"] == "Status: Application Withdrawn")
    {
        col = 'FF0000';
        letter = "W";
    }

    else if(record["status"] == "Application Withdrawn")
    {
        col = 'FF0000';
        letter = "W";
    }

    else if(record["status"] == "Status: DELETED APPLICATION")
    {
        col = 'FF0000';
        letter = "D";
    }

    else if(record["status"] == "DELETED APPLICATION")
    {
        col = 'FF0000';
        letter = "D";
    }
    else if(record["status"] == "Status: Application Returned")
    {
        col = 'FF0000';
        letter = "D";
    }

    else if(record["status"] == "Status: Insufficient Fee")
    {
        col = '5C5C8A';
        letter = "I";
    }

    else if(record["status"] == "Status: Pending Decision")
    {
        col = 'FF6600';
        letter = "P";
    }
    else if(record["status"] == "Pending Decision")
    {
        col = 'FF6600';
        letter = "P";
    }
    else if(record["status"] == "Status: Vary Consent")
    {
        col = '66FF33';
        letter = "P";
    }

    else if(record["status"] == "Status: Permitted Development")
    {
        col = '66FF33';
        letter = "A";
    }
    //letter = record["Validated"].charAt(3);        
     
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
    return '<div class="info-box"><h1>'+record["proposal"]+'</h1><div class="meta"><div class="col"><p><b>Date: </b>'+record["date received"]+'<br /><b>Status: </b>'+record["status"]+'<br /><b>Ref. Code: </b>'+record["ref"]+'</p></div><div class="col"><p><b>Address: </b><br />'+record["address"]+'<br /></p></div></div><a href="https://citydev-portal.edinburgh.gov.uk/idoxpa-web/applicationDetails.do?activeTab=summary&keyVal='+record["detail"]+'&searchtype=HOURLY" title="More information about '+record["ref"]+'" class="read-more-button">Read more <span class="info-icon"></span></a></div>';
}

var map; 
var centreset = false; 
function makemap()
{
    var mapOptions = { "zoom": 12, "center": new google.maps.LatLng(55.9501755, -3.1875359), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
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
    url =  "http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=edinburgh_planning_applications&query=select%20*%20from%20swdata%20order%20by%20date_scraped%20desc%20limit%20300&callback=gotback"
    // alert(url);
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

$(function() { makemap(); loaddata(); });

</script> 

<div id = "key-overlay" >
    <span style="font-weight:bold;">Key</span>
    <br><br>
    <img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=A|66FF33|" /> <span class="key-text"> Application Approved </span> <br>
    <img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=P|FF6600|" /> <span class="key-text"> Application Pending </span><br>
    <img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=W|FF0000|" /> <span class="key-text"> Application Withdrawn </span><br>
    <img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=D|FF0000|" /> <span class="key-text"> Application Deleted </span><br>
    <img src="http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=R|FF0000|" /> <span class="key-text"> Application Refused </span><br>
    
</div>

</body> 
</html>