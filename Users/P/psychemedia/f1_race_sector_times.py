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
        'filterColumnLabel': 'Driver',
        'matchType': 'any'
      }
    });

   var posFilter = new google.visualization.ControlWrapper({
      'controlType': 'StringFilter',
      'containerId': 'control3',
      'options': {
        'filterColumnLabel': 'Position',
        'matchType': 'any'
      }
    });

var categoryPicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'control2',
    'options': {
      'filterColumnLabel': 'Sector',
      'ui': {
      'labelStacking': 'vertical',
        'allowTyping': false,
        'allowMultiple': false
      }
    }
  });

  var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard')).bind([posFilter,stringFilter,categoryPicker], json_table).draw(json_data);


    }
  </script>
  <body>
<div id="dashboard">
    <div id="control1"></div><div id="control2"></div><div id="control3"></div>
    <div id="table_div_json"></div>
</div>
  </body>
</html>
"""


scraperwiki.sqlite.attach( 'f1_timing' )
q = '* FROM "race_sectors"'
data = scraperwiki.sqlite.select(q)

description = {"sector": ("string", "Sector"),"name": ("string", "Driver"),'pos':("string","Position"),"driverNum":("string","Car Number"),"sectortime":("string","Sector Time")}

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("sector","pos","name","driverNum","sectortime" ),order_by="sector")

# Putting the JS code and JSon string into the template
#print "Content-type: text/html"
#print
print page_template % vars()
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
        'filterColumnLabel': 'Driver',
        'matchType': 'any'
      }
    });

   var posFilter = new google.visualization.ControlWrapper({
      'controlType': 'StringFilter',
      'containerId': 'control3',
      'options': {
        'filterColumnLabel': 'Position',
        'matchType': 'any'
      }
    });

var categoryPicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'control2',
    'options': {
      'filterColumnLabel': 'Sector',
      'ui': {
      'labelStacking': 'vertical',
        'allowTyping': false,
        'allowMultiple': false
      }
    }
  });

  var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard')).bind([posFilter,stringFilter,categoryPicker], json_table).draw(json_data);


    }
  </script>
  <body>
<div id="dashboard">
    <div id="control1"></div><div id="control2"></div><div id="control3"></div>
    <div id="table_div_json"></div>
</div>
  </body>
</html>
"""


scraperwiki.sqlite.attach( 'f1_timing' )
q = '* FROM "race_sectors"'
data = scraperwiki.sqlite.select(q)

description = {"sector": ("string", "Sector"),"name": ("string", "Driver"),'pos':("string","Position"),"driverNum":("string","Car Number"),"sectortime":("string","Sector Time")}

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("sector","pos","name","driverNum","sectortime" ),order_by="sector")

# Putting the JS code and JSon string into the template
#print "Content-type: text/html"
#print
print page_template % vars()
