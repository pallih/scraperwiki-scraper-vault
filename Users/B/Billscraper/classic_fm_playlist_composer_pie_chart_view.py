# Blank Python
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
          title: 'Composers',
          pieSliceTextStyle: {color: 'black', fontName: 'Verdana', fontSize: 8},
          legend: {textStyle: {fontSize: 8}}
        };

        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));

        chart.draw(json_data, options);
      }
    </script>
  </head>
  <body>
    <h3 style="font-family:Arial, Helvetica, sans-serif;font-size:16px">Most Played Composers on Classic FM: %(dateinfostring)s</h3>

    <div id="chart_div" style="width: 1500px; height: 800px;"></div>
  </body>
</html>
"""

#POINT AT CORRECT SCRAPER
scraperwiki.sqlite.attach( sourcescraper)

#REST OF SELECT STATEMENT
q = " [Composer Name], count(*) as Freq FROM swdata where [Track date] <> '2013-01-14' group by 1 order by 2 desc"


#INITIATE SELECT STATEMENT
data = scraperwiki.sqlite.select(q)

#OUTLINE TABLE STRUCTURE
description = {"Composer Name": ("string", "Composer Name"),"Freq": ("number", "Frequency")} 

#CREATE TABLE
data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

#TURN TABLE INTO JSON
json = data_table.ToJSon(columns_order=("Composer Name","Freq"),order_by=("Freq", "desc"))

#FIND START OF SCRAPED PERIOD
startdate = scraperwiki.sqlite.execute("SELECT MIN([Track Date]) FROM swdata")
enddate =  scraperwiki.sqlite.execute("SELECT MAX([Track Date]) FROM swdata")

startdate2 =  str("".join(startdate['data'][0]))
enddate2 =  str("".join(enddate['data'][0]))

dateinfostring = "between %s and %s " % (startdate2, enddate2)

 
print htmlpage % vars()
