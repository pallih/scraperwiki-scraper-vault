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
    google.load('visualization', '1', {packages:['table']});

    google.setOnLoadCallback(drawTable);
    function drawTable() {

      var json_table = new google.visualization.Table(document.getElementById('table_div_json'));
      var json_data = new google.visualization.DataTable(%(json)s, 0.6);
      json_table.draw(json_data, {showRowNumber: true});
    }
  </script>
  <body>

    <div id="table_div_json"></div>
  </body>
</html>
"""


scraperwiki.sqlite.attach( 'openlearn-units' )
q = 'parentCourseCode,name,topic,unitcode FROM "swdata" LIMIT 20'
data = scraperwiki.sqlite.select(q)

description = {"parentCourseCode": ("string", "Parent Course"),"name": ("string", "Unit name"),"unitcode": ("string", "Unit Code"),"topic":("string","Topic")}

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("unitcode","name", "topic","parentCourseCode" ),order_by="unitcode")

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
    google.load('visualization', '1', {packages:['table']});

    google.setOnLoadCallback(drawTable);
    function drawTable() {

      var json_table = new google.visualization.Table(document.getElementById('table_div_json'));
      var json_data = new google.visualization.DataTable(%(json)s, 0.6);
      json_table.draw(json_data, {showRowNumber: true});
    }
  </script>
  <body>

    <div id="table_div_json"></div>
  </body>
</html>
"""


scraperwiki.sqlite.attach( 'openlearn-units' )
q = 'parentCourseCode,name,topic,unitcode FROM "swdata" LIMIT 20'
data = scraperwiki.sqlite.select(q)

description = {"parentCourseCode": ("string", "Parent Course"),"name": ("string", "Unit name"),"unitcode": ("string", "Unit Code"),"topic":("string","Topic")}

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("unitcode","name", "topic","parentCourseCode" ),order_by="unitcode")

# Putting the JS code and JSon string into the template
#print "Content-type: text/html"
#print
print page_template % vars()
