<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="content-type"
      content="text/html; charset=utf-8"/>
    <title>
      PML Daily
    </title>
    <script type="text/javascript"
     src="http://www.google.com/jsapi">
    </script>
    <script type="text/javascript">
      google.load('visualization', '1',
        {packages: ['corechart', 'annotatedtimeline']});
    </script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>    <script type="text/javascript">
function scraperfromloc(loc) {
    var s
    s = loc.match(/[?&]scraper=([-\w]+)/)
    if(s) {
        return s[1]
    }
    return null
}
var sourcescraper
sourcescraper = 'cam-bot-temp'
sourcescraper = 'pml-weather'
var s = scraperfromloc(''+document.location)
if(s) {
    sourcescraper = s
}
var data
function ipl() {
    $("#message").html("started");
    loaddata()
}
function drawVisualization() {
    var i, row, d, date;
    alldate.sort()
    for(i=0;i<alldate.length;++i) {
        date = alldate[i]
        d = new Date(date)
        row = [d, rawdata.tminD[date], rawdata.tmaxD[date]]
        data.addRow(row)
    }
    // Create and draw the visualization.
    new google.visualization.AnnotatedTimeLine(
      document.getElementById('visualization')).
        draw(data, {title:"Daily Temperature",
            width:480, height:360,
                    legend:'top'});
}
// Each meteorological element gets an entry in this table;
// the entry is itself a table that maps from
// dates (strings, ISO 8601) to temperatures.
var rawdata = {}
// Collection of all the dates (strings, ISO 8601) used.
var alldate
function recorddata(r)
{
    var p

    if(rawdata[r.element] === undefined) {
        return
    }
    // Every property corresponding to an ISO 8601 date, has
    // a temperature as its value.
    for(p in r) {
        if(/\d{4}-\d{2}-\d{2}/.test(p)) {
            rawdata[r.element][p] = +r[p]
            alldate.push(p)
        }
    } 
}
var offset = 0;    
function cleardata()
{
    alldate = []
    rawdata = {tminD:{},tmaxD:{}}
    // Create data table.
    data = new google.visualization.DataTable();
    data.addColumn('date', 'Date')
    data.addColumn('number', 'tmin')
    data.addColumn('number', 'tmax')
    offset = 0
}
cleardata()

var olength = 330;
var olimit = 6000;
// Called with every new batch of records we get.
// r is the JSON object
function gotback(r)
{
    for (i = 0; i < r.length; i++)
        recorddata(r[i]);

    offset += r.length
    if ((r.length == olength) && (offset < olimit)) {
        $("#message").html("records=" + offset);
        loaddata();
    } else {
        $("#message").html("Total records=" + offset);
        drawVisualization()
        $("#header").html(sourcescraper)
    }
}
function loaddata()
{
    var s = document.createElement('script');
    url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+sourcescraper+"&limit="+olength+"&callback=gotback&offset=" + offset;
    s.setAttribute('src', url);
    s.setAttribute('type', 'text/javascript');
    document.getElementsByTagName('head')[0].appendChild(s);
    $("#header").html(sourcescraper + " (loading)")
}
function buttoncambottemp()
{
    sourcescraper="cam-bot-temp"
    $("#message").html("Loading Cambridge Botanic")
    cleardata()
    loaddata()
}
function buttonpmltemp()
{
    sourcescraper="pml-weather"
    $("#message").html("Loading Plymouth Marine")
    cleardata()
    loaddata()
}
function buttonknatemp()
{
    sourcescraper="weather-data-for-alice-holt-and-kielder"
    $("#message").html("Loading Kielder and Alice Holt")
    cleardata()
    loaddata()
}
    
google.setOnLoadCallback(ipl);
    </script>

  </head>
  <body style="font-family: Arial;border: 0 none;">
      <h2 id="header">Some Weather Station</h2>
    <div id="visualization"
     style="width: 480px; height: 360px;">
    </div>
      <form>
        <input type="button" value="Cambridge Botanic" name="button1" onclick="buttoncambottemp()" />
        <input type="button" value="Plymouth Marine" name="button2" onclick="buttonpmltemp()" />
        <input type="button" value="Kielder and Alice Holt" name="button3" onclick="buttonknatemp()" />
      </form>
      <p><span id="message">...</span></p>
  </body>
</html>
