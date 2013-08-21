<html dir="ltr" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Canada Weather Stations</title>
    <style type="text/css" media="screen">p{padding:1px;}</style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
    <script type="text/javascript" src="http://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load('visualization', '1',
        {packages: ['corechart', 'annotatedtimeline']});
    </script>

</head>

<body>

<h2>Map of <span id="scrapername">...</span> <em id="message">...</em></h2>
<table>
    <tr id="colourlegend"><td>Months with data:</td></tr>
    <tr id="colourradio"><td>Show on Map</td></tr>
</table>
<p>Map-pin letter: O: records in last 3 years (approx); X: no records in last 3 years (approx).</p>
<table>
  <tr>
    <td><div id="map" style="width: 480px;height:400px"></div></td>
    <td><p id="showing">Click a pin and select <em>Chart</em> to see data here.</p>
        <div id="chart" style="width: 480px;height:360px"></div></td>
  </tr>
</table>

<script type="text/javascript" charset="utf-8">
// ####################################################################
// Start of javascript code.
// ####################################################################
    
var sourcescraper = 'canada-temperature-data';
$('#scrapername').html('<b>'+sourcescraper+'</b>'); 
    
// ####################################################################
// Set the dynamic icon for your point.  For more see: 
// http://code.google.com/apis/chart/docs/gallery/dynamic_icons.html
// ####################################################################
function mapicon(record)
{

    var letter = 'O';
    var now = new Date();
    var latest = +record.yearmax
    if(isNaN(latest)) {
        letter = '+'
    } else if(now - new Date(record.yearmax,6,1) > 1e11) {
        // If the 1st July in the record's most recent year is more than about 3 years ago, mark with X.
        // Note 1e11 milliseconds is "about 3 years"
        letter = 'X';
    }
    return iconfromcount(letter, record.monthcount, station_wmo(record))
}

// Given len, a length in months, return the category of it.
// The returned category is a small integer.
var length_categories = [0, 1, 120, 240, 480]
function categorise_length(len)
{
    var i, cat
    for(i=0; i<length_categories.length; ++i) {
        if(len >= length_categories[i]) {
            cat = i
        }
    }
    return cat
}

// Categorise a station record (a small integer, just like categorise_length).
function categorise(record)
{
    return categorise_length(record.monthcount)
}

function iconfromcount(letter, count, wmo)
{
    var icon, pin
    var col
    var cat = categorise_length(count)
    col = ['555', '800', 'c85', 'fa0', '0f0'][cat]
    if(wmo) {
        style = 'pin_star'
    } else {
        style = 'pin'
    }

    icon = 'http://chart.apis.google.com/chart?chst=d_map_xpin_letter&chld='+style+'|'+letter+'|'+col+'|000|CC3';
    return icon
}

// Tooltip title for each pin.
function tooltiptitle(record)
{
    return station_name(record)
}

// Popup text for each pin.
function popuptext(record)
{
    var wmo = station_wmo(record)
    if(wmo) {
        wmo = ' (WMO ' + wmo + ')'
    }
    return '<p>' + station_name(record) + ' ' + latlon(record) + '</p>' +
        '<p>id: ' + record.id + wmo + '</p>' +
        '<p><a href="' + record.source + '" target="_blank">CSV file</a></p>' +
        '<p><a href="javascript:loadstation(' + "'" + record.id + "'" + ')">Chart (' +
        record.yearmin + ' to ' + record.yearmax + ')</a></p>' +
        '';
}
// Return the lat/lon of a record as a string.
function latlon(record)
{
    var lat = +record.Latitude
    lat *= 100
    lat = Math.round(lat)
    lat = padzero(lat, 4)
    lat = lat.slice(0,3) + '.' + lat.slice(3)
    var lon = +record.Longitude
    lon *= 100
    lon = Math.round(lon)
    lon = padzero(lon, 5)
    lon = lon.slice(0,4) + '.' + lon.slice(4)
    return lat+lon
}

// pad the integer x so that it consists of at least
// n digits.  A string is returned that starts with
// '+' or '-' (for the sign) followed by n digits.
// (more if x requires it)
function padzero(x, n)
{
    x = +x
    var s = '+'
    if(x < 0) {
        s = '-'
        x = -x
    }
    var sx = '' + x
    var pad = ''
    while((pad + sx).length < n) {
        pad += '0'
    }
    return s + pad + sx
}

var map; 
var centreset = true; 
function makemap()
{
    var mapOptions = { "zoom": 3, "center": new google.maps.LatLng(65, -99), 
                    "mapTypeId": google.maps.MapTypeId.SATELLITE };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}

station = {}

// WMO Identifier for station.  or ''
function station_wmo(record)
{
    var wmo = record['WMO Identifier']
    if(!wmo) {
        return ''
    }
    return wmo
}
// Name of station. Several conventions.
function station_name(record)
{
    var name = record['Station Name'];
    if(!name) {
        name = record['Station_Name'];
    }
    if(!name) {
        return record.id
    }
    return name
}

function station_name_id(stationid)
{
    var meta = station[stationid]
    if(!meta) {
        return stationid
    }
    return station_name(meta)
}

// List of list.  There is one inner list per category, each one being
// a list of markers.
var markers = []
for(i=0; i<length_categories.length; ++i) {
  markers[i] = []
}

function refresh_category(c, visible)
{
    var m = null
    if(visible) {
        m = map
    }
    $.each(markers[c], function(_,marker) {marker.setMap(m)})
}      

// Note the station, both on the map, and internally
// (putting the record in the *station* global, and its
// associated marker in the markers global).
// Returns the number of stations noted (0 or 1).
function notestation(record)
{
    var marker, infowindow
    if (!(record['Latitude']))
        return 0; 
    if(0 && !('yearmax' in record)) {
        return 0
    }
    station[record.id] = record
    var pos = new google.maps.LatLng(record['Latitude'], record['Longitude']); 

    var title = tooltiptitle(record);
    var icon = mapicon(record);
    marker = new google.maps.Marker({position:pos,map:map,title:title,icon:icon});
    var cat = categorise(record)
    markers[cat].push(marker)

    var content = popuptext(record);

    infowindow = new google.maps.InfoWindow({ content: content });
    google.maps.event.addListener(marker, "click", function(){
                        infowindow.open(map, marker); });
    if (!centreset) {
        map.setCenter(pos)
        centreset = true
    }
    return 1
}

var stations = 0;
function gotback(r) 
{
    $("#message").html("Stations: " + r.length);
    for (i = 0; i < r.length; i++)
        stations += notestation(r[i]);
}

function loaddata() 
{
    var s = document.createElement('script');
    var url = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=" +
        sourcescraper +
        "&query=select%20*%20from%20meta%20left%20outer%20join%20series%20using%20(id)%20where%20series.element%20is%20null%20or%20series.element%20%3D%20'tmeanM'&callback=gotback"
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
}

// Each meteorological element gets an entry in this table;
// the entry is itself a table that maps from
// dates (strings, ISO 8601) to temperatures.
var rawdata = {}
// Collection of all the dates (strings, ISO 8601) used.
var alldate
function drawChart()
{
    var i, row, d, date;
    alldate.sort()
    for(i=0;i<alldate.length;++i) {
        date = alldate[i]
        d = new Date(date)
        row = [d, rawdata.tmeanM[date]]
        data.addRow(row)
    }
    // Create and draw the visualization.
    new google.visualization.AnnotatedTimeLine(
      document.getElementById('chart')).
        draw(data, {title:"Monthly Mean Temperature",
            width:480, height:360,
            legend:'top'});
}
// For chart.
function recorddata(r)
{
    var p
    // ISO 8601 date.  EG 2011-08.
    var iso

    // We expect each row, r, to have a 'year' property,
    // a 'element' property,
    // and 12 propties: 'M01' to 'M12'.
    for(p in r) {
        if(/M\d{2}/.test(p)) {
            iso = r.year + '-' + p.substring(1)
            rawdata[r.element][iso] = +r[p]
            alldate.push(iso)
        }
    } 
}
// Callback for station data.  Called with records of temperature data,
// when we get them.  See loadstation().  For chart.
function gotdata(r)
{
    var i
    for (i = 0; i < r.length; i++) {
        recorddata(r[i])
    }
    drawChart()
    var name = station_name_id(r[0].id)
    $("#showing").html(name)
}

// Loads monthly mean temperature (element="tmeanM") for a station.
// (For drawing the chart)
function loadstation(stationid)
{
    var s = document.createElement('script');
    cleardata()
    var url = "http://api.scraperwiki.com/api/1.0/datastore/search?format=json&name=" + sourcescraper +
        "&callback=gotdata&filter=id," + stationid + "|element,tmeanM"
    var url = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=" +
        sourcescraper +
            "&query=select%20id%2Cyear%2Celement%2CM01%2CM02%2CM03%2CM04%2CM05%2CM06%2CM07%2CM08%2CM09%2CM10%2CM11%2CM12%20from%20swdata%20where%20id%20%3D%20'" +
    stationid +
        "'%20order%20by%20year&callback=gotdata"
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
    var name = station_name_id(stationid)
    $("#showing").html(name + " (loading)")
}

function cleardata()
{
    alldate = []
    rawdata = {tmeanM:{}}
    // Create data table.
    data = new google.visualization.DataTable();
    data.addColumn('date', 'Date')
    data.addColumn('number', 'tmean')
}
cleardata()

var boxischecked = []
$.each(length_categories, function(i){boxischecked[i]=true})

// Rescan the check boxes, and refresh the map for those boxes which changed.
// Usually called from a button click event
function refresh_checked()
{
    var nowchecked = []
    $("#colourradio input:checkbox").each(function(i){nowchecked[i] = this.checked})
    //console.log("now", nowchecked)
    // Make a list of where nowchecked and boxischecked differ.
    var diff = []
    $.each(boxischecked, function(i,v){diff[i]=!v!=!nowchecked[i];boxischecked[i]=nowchecked[i]})
    //console.log("diff", diff)
    $.each(diff, function(i,v){if(v){refresh_category(i, nowchecked[i])}})
}

// A checkbox was clicked.
function boxchecked()
{
    refresh_checked()
}

// Fill in the HTML that displays the legend.
function colourlegend()
{
    var l = length_categories // a global
    var i, n, r
    for(i=0; i<l.length; ++i) {
        n = l[i]
        $("<td><img src='" + iconfromcount('*', n) + "' /> " + n +
          " or more</td>").appendTo($('#colourlegend'))
// <input type="checkbox" name="option1" value="Milk"> Milk
        r = 'box' + i
        $("<td><input type='checkbox' id='" + r + "' name='" +
            r + "' value='" + i + "' checked='radio'></input></td>").appendTo($('#colourradio'))
    }
    // http://docs.jquery.com/Tutorials:Getting_Started_with_jQuery
    $("#colourradio input").click(boxchecked)
}

$(function() { colourlegend(); makemap(); loaddata(); });

</script> 
</body> 
</html>
