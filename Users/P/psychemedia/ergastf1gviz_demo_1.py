import cgi, os
qstring=os.getenv("QUERY_STRING")
try:
    get = dict(cgi.parse_qsl(qstring))
    year=get['year']
    race=get['race']
except:
    year='2012'
    race='2'


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

      //var json_table = new google.visualization.DataView(document.getElementById('table_div_json'));
      //json_table.draw(json_data, {showRowNumber: false});
   

    var json_table = new google.visualization.ChartWrapper({'chartType': 'Table','containerId':'table_div_json','options': {allowHtml: true,page:'enable',pageSize:24,'pagingButtonsConfiguration':'auto' }});

    //i expected this limit on the view to work?
    //json_table.setColumns([0,1,2,3,4,5,6,7])
    //var formatter = new google.visualization.PatternFormat('<a href="http://www.bbc.co.uk/iplayer/episode/{1}">{0}</a>');
    //formatter.format(json_data, [1,6]); // Apply formatter and set the formatted value of the first column.

    //formatter = new google.visualization.PatternFormat('<a href="{1}">{0}</a>');
    //formatter.format(json_data, [5,8]);

     var formatter = new google.visualization.NumberFormat({fractionDigits: 3});
     formatter.format(json_data,4);
    var stringFilter = new google.visualization.ControlWrapper({
      'controlType': 'StringFilter',
      'containerId': 'control1',
      'options': {
        'filterColumnLabel': 'Lap',
        'matchType': 'any'
      }
    });


  var categoryPicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'control2',
    'options': {
      'filterColumnLabel': 'Driver ID',
      'ui': {
      'labelStacking': 'vertical',
        'allowTyping': false,
        'allowMultiple': false
      }
    }
  });
  var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard')).bind([stringFilter,categoryPicker], [json_table]).draw(json_data);
 
    }
  </script>
  <body>
<div id="dashboard">
    <div id="control1"></div>
<div id="control2"></div>
<div id="linechart"></div>
    <div id="table_div_json"></div>
</div>
  </body>
</html>
"""


url='https://views.scraperwiki.com/run/ergastf1racelaps_2_gviz_converter/?year='+str(year)+'&race='+str(race)

import urllib,simplejson
json=simplejson.load(urllib.urlopen(url))

# Putting the JS code and JSon string into the template
#print "Content-type: text/html"
#print


print page_template % vars()
