# Thought it would be interesting to superimpose pie chart on to a relevant image
# Potential Flaws:
#  -not tested in other browsers
#  -is rendering consistent?
#  -tooltips don't work as CD image is at front, could potentially reverse and do a different way

sourcescraper = 'classic_fm_playlist_scraper'

import scraperwiki
import gviz_api

htmlpage = """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var json_data = new google.visualization.DataTable(%(json)s, 0.6);
        var options = {
          title: 'Top Record Labels',
          pieSliceTextStyle: {color: 'black', fontName: 'Verdana', fontSize: 8},
          legend: {textStyle: {fontSize: 8}},
        };

        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));

        chart.draw(json_data, options);
      }
    </script>
    <style type='text/css'>
    .under
    {
    position:absolute;
    left:0px;
    top:0px;
    z-index:-1;
    }
    .over
    {
    position:absolute;
    left:315px;
    top:150px;
    opacity:0.8;
    z-index:1;
    }
    </style>
  </head>
  <body>
    <h3 style="font-family:Arial, Helvetica, sans-serif;font-size:16px">Most Played Record Labels on Classic FM: %(dateinfostring)s</h3>
    <img src='http://upload.wikimedia.org/wikipedia/commons/d/d0/Compact_disc.svg' class='over' />
    <div id='chart_div' style='width: 1500px; height: 800px;'  class='under'>test</div>
  </body>
</html>
"""

#POINT AT CORRECT SCRAPER
scraperwiki.sqlite.attach( sourcescraper)

#REST OF SELECT STATEMENT
q = " [Record Label], count(*) as Freq FROM swdata where [Track date] <> '2013-01-14' group by 1 order by 2 desc"


#INITIATE SELECT STATEMENT
data = scraperwiki.sqlite.select(q)

#OUTLINE TABLE STRUCTURE
description = {"Record Label": ("string", "Record Label"),"Freq": ("number", "Frequency")} 

#CREATE TABLE
data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

#TURN TABLE INTO JSON
json = data_table.ToJSon(columns_order=("Record Label","Freq"),order_by=("Freq", "desc"))

#FIND START OF SCRAPED PERIOD
startdate = scraperwiki.sqlite.execute("SELECT MIN([Track Date]) FROM swdata")
enddate =  scraperwiki.sqlite.execute("SELECT MAX([Track Date]) FROM swdata")

startdate2 =  str("".join(startdate['data'][0]))
enddate2 =  str("".join(enddate['data'][0]))

dateinfostring = "between %s and %s " % (startdate2, enddate2)

 
print htmlpage % vars()


