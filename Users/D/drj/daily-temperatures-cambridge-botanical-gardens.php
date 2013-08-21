<?php
# Blank PHP
$sourcescraper = 'foi_botanical_gardens'
?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="content-type" 
      content="text/html; charset=utf-8"/>
    <title>
      Cambridge Botanical Gardens
    </title>
    <script type="text/javascript" 
     src="http://www.google.com/jsapi">
    </script>
    <script type="text/javascript">
      google.load('visualization', '1', 
        {packages: ['corechart', 'annotatedtimeline']});
    </script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>    <script type="text/javascript">
var sourcescraper = 'foi_botanical_gardens'
        var data
    function ipl() {
        // Create data table.
        data = new google.visualization.DataTable();
        data.addColumn('date', 'Date')
        data.addColumn('number', 'tmin')
        data.addColumn('number', 'tmax')
        $("#message").html("started");
        loaddata()
    }
    function drawVisualization() {
        var i, row;
        rawdata.sort()
        for(i=0;i<rawdata.length;++i) {
            row = rawdata[i]
            data.addRow(row)
        }
        // Create and draw the visualization.
        new google.visualization.AnnotatedTimeLine(
          document.getElementById('visualization')).
            draw(data);
      }
var rawdata = []
    function recorddata(r)
    {
        rawdata.push([new Date(r.Date), +r.tmin, +r.tmax])
    }
var olength = 330;
var olimit = 6000;
var offset = 0;    
    // Called with every new batch of records we get.
    // r is the JSON object
    function gotback(r)
    {
        for (i = 0; i < r.length; i++)
            recorddata(r[i]);
    
        if ((r.length == olength) && (offset < olimit)) {
            $("#message").html("records=" + (offset + r.length));
            offset += olength;
            loaddata();
        } else {
            $("#message").html("Total records=" + (offset + r.length));
            drawVisualization()
        }
    }
    function loaddata()
    {
        var s = document.createElement('script');
        url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=json&name="+sourcescraper+"&limit="+olength+"&callback=gotback&offset=" + offset;
        s.setAttribute('src', url);
        s.setAttribute('type', 'text/javascript');
        document.getElementsByTagName('head')[0].appendChild(s);
    }
      google.setOnLoadCallback(ipl);
    </script>

  </head>
  <body style="font-family: Arial;border: 0 none;">
      <h2><a href="http://www.botanic.cam.ac.uk/Botanic/Page.aspx?p=27&ix=2830&pid=0&prcid=0&ppid=0">Cambridge Botanical Gardens</a></h2>
    <div id="visualization" 
     style="width: 400px; height: 300px;">
    </div>
<p><span id="message">...</span></p>
  </body>
</html>
