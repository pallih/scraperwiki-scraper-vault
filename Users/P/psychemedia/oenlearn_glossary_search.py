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
   

    var json_table = new google.visualization.ChartWrapper({'chartType': 'Table','containerId':'table_div_json','options': {allowHtml: true}});
    //i expected this limit on the view to work?
    //json_table.setColumns([0,1,2,3,4,5,6,7])
    var formatter = new google.visualization.PatternFormat('<a href="http://openlearn.open.ac.uk/mod/oucontent/search.php?id={0}&query={1}">{1}</a>');
    //can we escape the following so we can generate a restful search query around a phrase from a column? cf [escape(0)] maybe?
    formatter.format(json_data, [3,0]);


    formatter = new google.visualization.PatternFormat('<a href="http://openlearn.open.ac.uk/course/view.php?name={0}">{0}</a>');
    formatter.format(json_data, [2]); // Apply formatter and set the formatted value of the first column.

   
    var stringFilter = new google.visualization.ControlWrapper({
      'controlType': 'StringFilter',
      'containerId': 'control1',
      'options': {
        'filterColumnLabel': 'Term',
        'matchType': 'any'
      }
    })
    var stringFilter2 = new google.visualization.ControlWrapper({
      'controlType': 'StringFilter',
      'containerId': 'control2',
      'options': {
        'filterColumnLabel': 'Definition',
        'matchType': 'any'
      }
    });

  var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard')).bind(stringFilter, json_table).bind(stringFilter2, json_table).draw(json_data);


    }
  </script>
  <body>
<div id="dashboard">
    <div><span id="control1"></span> <span id="control2"></span></div>
    <div id="table_div_json"></div>
</div>
  </body>
</html>
"""


scraperwiki.sqlite.attach( 'openlearn_xml_processor' )
q = '* FROM "glossary"'
data = scraperwiki.sqlite.select(q)

description = {"ccu": ("string", "Unitcode"),"definition": ("string", "Definition"),"term": ("string", "Term"),'ccid':("string","Search this OpenLearn unit")}

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("term","definition","ccu","ccid" ),order_by="term")

# Putting the JS code and JSon string into the template
#print "Content-type: text/html"
#print
print page_template % vars()
