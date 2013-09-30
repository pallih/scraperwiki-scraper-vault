# Blank Python
import gviz_api
import scraperwiki
           

page_template = """
<html>
  <head>
  <title>Static example</title>
    <script src="http://www.google.com/jsapi" type="text/javascript"></script>
    <script>
      google.load("visualization", "1", {packages:["table"]});

      google.setOnLoadCallback(drawTable);
      function drawTable() {
        %(jscode)s
        var jscode_table = new google.visualization.Table(document.getElementById('table_div_jscode'));
        jscode_table.draw(jscode_data, {showRowNumber: true});

        var json_table = new google.visualization.Table(document.getElementById('table_div_json'));
        var json_data = new google.visualization.DataTable(%(json)s, 0.5);
        json_table.draw(json_data, {showRowNumber: true});
      }
    </script>
  </head>
  <body>
    <H1>Table created using ToJSCode</H1>
    <div id="table_div_jscode"></div>
    <H1>Table created using ToJSon</H1>
    <div id="table_div_json"></div>
  </body>
</html>
"""


# Creating the data
description = {"make": ("string", "Make"), "count": ("number", "Count")}

scraperwiki.sqlite.attach("dubizzle_used_cars")
sqldata = scraperwiki.sqlite.execute("select make, count(*) as count from car_stat group by make")
#print sqldata
data = []
for row in sqldata["data"]:
    data.append(dict(make=row[0], count=row[1]))


# Loading it into gviz_api.DataTable
data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

# Creating a JavaScript code string
jscode = data_table.ToJSCode("jscode_data",
                           columns_order=("make", "count"),
                           order_by="make")
# Creating a JSon string
json = data_table.ToJSon(columns_order=("make", "count"),
                       order_by="make")

# Putting the JS code and JSon string into the template
#print page_template % vars()




