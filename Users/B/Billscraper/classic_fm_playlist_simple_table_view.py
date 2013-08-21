# Blank Python
sourcescraper = 'classic_fm_playlist_scraper'

import scraperwiki
import gviz_api

#Example of:
## how to use the Google gviz Python library to cast Scraperwiki data into the Gviz format
## how to render the gviz data format using the Google Visualization library

#Based on the code example at:
#http://code.google.com/apis/chart/interactive/docs/dev/gviz_api_lib.html


page_template = """
<html>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script>
    google.load('visualization', '1.1', {packages:['controls']});

    google.setOnLoadCallback(drawTable);

    function drawTable() {

        var json_data = new google.visualization.DataTable(%(json)s, 0.6);
   

        var json_table = new google.visualization.ChartWrapper({'chartType': 'Table','containerId':'table_div_json','options': {allowHtml: true}});


        var stringFilter = new google.visualization.ControlWrapper({
          'controlType': 'StringFilter',
          'containerId': 'control1',
          'options': {
          'filterColumnLabel': 'Composer Name',
          'matchType': 'any'
      }
    });

  var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard')).bind(stringFilter, json_table).draw(json_data);


    }
  </script>
  <body>
<div id="dashboard">
    <div id="control1"></div>
    <div id="table_div_json"></div>
</div>
  </body>
</html>
"""

#POINT AT CORRECT SCRAPER
scraperwiki.sqlite.attach( sourcescraper)

#REST OF SELECT STATEMENT
q = "* FROM swdata where [Track date] <> '2013-01-14'"


#INITIATE SELECT STATEMENT
data = scraperwiki.sqlite.select(q)

#OUTLINE TABLE STRUCTURE
description = {"Record Label": ("string", "Record Label"),"Composer Name": ("string", "Composer Name"),"Conductor":("string","Conductor"),"Track Date": ("string", "Track Date"),"Catalog": ("string", "Catalog"),"Track Time": ("string", "Track Time"),"Track Name": ("string", "Track Name"),"Ensemble": ("string", "Ensemble"),"Soloists": ("string", "Soloists")} 

#CREATE TABLE
data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

#TURN TABLE INTO JSON
json = data_table.ToJSon(columns_order=("Track Date","Track Time","Track Name","Composer Name","Ensemble","Conductor","Soloists" ,"Record Label","Catalog"),order_by="Track Time")

print page_template % vars()

