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
    var formatter = new google.visualization.PatternFormat('<img src="{0}"/>');
    formatter.format(json_data, [2]);

    var stringFilter = new google.visualization.ControlWrapper({
      'controlType': 'StringFilter',
      'containerId': 'control1',
      'options': {
        'filterColumnLabel': 'Representative',
        'matchType': 'any'
      }
    });

var categoryPicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'control2',
    'options': {
      'filterColumnLabel': 'Company Name',
      'ui': {
        'allowTyping': false,
        'allowMultiple': true,
        'selectedValuesLayout': 'belowStacked'
      }
    },
    // Define an initial state, i.e. a set of metrics to be initially selected.
    //'state': {'selectedValues':['Frozen Planet']}
  });

  var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard')).bind([categoryPicker,stringFilter], json_table).draw(json_data);


    }
  </script>
  <body>
<div id="dashboard">
    <div id="control1"></div><div id="control2"></div>
    <div id="table_div_json"></div>
</div>
  </body>
</html>
"""


scraperwiki.sqlite.attach( 'opencorporates_trademark_demo' )
q = '* FROM "trademarks" WHERE imgurl !=""'
data = scraperwiki.sqlite.select(q)

description = {"regnum": ("string", "Trademark No."),"marktext": ("string", "Mark Text"),"imgurl":("string","Logo"),"ocname":("string","Company Name"),"repname": ("string", "Representative")}

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("regnum","marktext","imgurl","ocname", "repname" ),order_by="marktext")

# Putting the JS code and JSon string into the template
#print "Content-type: text/html"
#print
print page_template % vars()









