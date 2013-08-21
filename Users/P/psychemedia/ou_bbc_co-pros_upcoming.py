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
    var formatter = new google.visualization.PatternFormat('<a href="http://www.bbc.co.uk/programmes/{1}">{0}</a>');
    formatter.format(json_data, [1,6]); // Apply formatter and set the formatted value of the first column.

    //http://static.bbci.co.uk/programmeimages/272x153/episode/ http://static.bbc.co.uk/programmeimages/304x171/clip/
    formatter = new google.visualization.PatternFormat('<a href="http://www.bbc.co.uk/programmes/{0}"><img src="http://static.bbci.co.uk/programmeimages/272x153/episode/{0}.jpg" /></a>');
    formatter.format(json_data, [6]); // Apply formatter and set the formatted value of the first column.


    formatter = new google.visualization.PatternFormat('<a href="{1}">{0}</a>');
    formatter.format(json_data, [10,9]);

    formatter = new google.visualization.PatternFormat('<a href="http://www.bbc.co.uk/programmes/{1}">{0}</a>');
    formatter.format(json_data, [0,7]);

var categoryPicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'control2',
    'options': {
      'filterColumnLabel': 'Series',
      'ui': {
        'allowTyping': false,
        'allowMultiple': true,
        'selectedValuesLayout': 'belowStacked'
      }
    },
    // Define an initial state, i.e. a set of metrics to be initially selected.
    'state': {'selectedValues':[]}
  });

    var stringFilter = new google.visualization.ControlWrapper({
      'controlType': 'StringFilter',
      'containerId': 'control1',
      'options': {
        'filterColumnLabel': 'About',
        'matchType': 'any'
      }
    });

var view = new google.visualization.DataView(json_data);
    view.setColumns([0,6,1,2,3,4,5,8,10])

  var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard')).bind([categoryPicker], json_table).draw(view);
 
    }
  </script>
  <body><h1>Open University/BBC Co-Productions Upcoming Broadcasts</h1>
<div id="dashboard">
    <div><span id="control1"></span> <span id="control2"></span></div>
    <div id="table_div_json"></div>
</div>
  </body>
</html>
"""


scraperwiki.sqlite.attach( 'ou_bbc_co-pros_on_iplayer' )
q = '* FROM "upcomingOUBBC" WHERE strftime("%s",`startTime`)>strftime("%s","now")'
data = scraperwiki.sqlite.select(q)



description = {"seriesTitle": ("string", "Series"),"progID": ("string", "Episode"),"short_synopsis":("string","About"),"title": ("string", "Episode Page"), "startTime":("string","Start time"),"date": ("string", "Date"),"seriesID":("string","Series ID"),"service":("string","Channel"),"ouTitle":("string","OU title"),"content": ("string", "OU description"),"link_uri": ("string", "OU URI"),"link_title": ("string", "OU Link")}
#, "ouTitle":("string","OU title"),"ouURI": ("string", "OU URI"),"ouContent": ("string", "OU description"),"ouLinkTitle": ("string", "OU Link")

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("seriesTitle","title","short_synopsis","service","date","startTime","progID","seriesID","content","link_uri","link_title"),order_by="startTime")

# Putting the JS code and JSon string into the template
#print "Content-type: text/html"
#print


print page_template % vars()
