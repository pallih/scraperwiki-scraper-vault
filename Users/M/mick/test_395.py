import scraperwiki
import gviz_api

page_template = """
<html>
  <head>
  <title>Bar-Meter</title>
    <script src="http://www.google.com/jsapi" type="text/javascript"></script>
    <script>
      google.load("visualization", "1", {packages:["table","corechart"]});

      google.setOnLoadCallback(drawTable);
      function drawTable() {
        %(jscode)s
        var jscode_table = new google.visualization.Table(document.getElementById('table_div_jscode'));
        jscode_table.draw(jscode_data, {showRowNumber: true});

        %(jscode_chart)s
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(jscode_data_chart, {title: 'Bars per city'});
      }
    </script>
  </head>
  <body>
    <H1>Bars in Austrian cities</H1>
    <div id="table_div_jscode"></div>
    <div id="chart_div" style="width: 900px; height: 500px;"></div>
  </body>
</html>
"""


def main():
    scraperwiki.sqlite.attach("at_herold_branches")
    
    data = scraperwiki.sqlite.select(
        '''city, branch, count(*) as business from at_herold_branches.swdata
        where branch='was_bars'
        group by city, branch
        order by business desc'''
    )
    
    description = {"city": ("string", "City"),
                   "branch": ("string", "Branch"), 
                   "business": ("number", "Count")}
    
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Creating a JavaScript code string
    jscode = data_table.ToJSCode("jscode_data",
                               columns_order=("city", "branch", "business"))
    # Creating a JSon string
    #json = data_table.ToJSon(columns_order=("city", "branch", "business"),
    #                       order_by="city")
    
    data_chart = scraperwiki.sqlite.select(
        '''city, count(*) as business from at_herold_branches.swdata
        group by city'''
    )
    description_chart = {"city": ("string", "City"),
                   "business": ("number", "Count")}
    data_table_chart = gviz_api.DataTable(description_chart)
    data_table_chart.LoadData(data_chart)
    jscode_chart = data_table_chart.ToJSCode("jscode_data_chart",
                               columns_order=("city", "business"),
                               order_by="city")
    
    print page_template % vars()

main()
import scraperwiki
import gviz_api

page_template = """
<html>
  <head>
  <title>Bar-Meter</title>
    <script src="http://www.google.com/jsapi" type="text/javascript"></script>
    <script>
      google.load("visualization", "1", {packages:["table","corechart"]});

      google.setOnLoadCallback(drawTable);
      function drawTable() {
        %(jscode)s
        var jscode_table = new google.visualization.Table(document.getElementById('table_div_jscode'));
        jscode_table.draw(jscode_data, {showRowNumber: true});

        %(jscode_chart)s
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(jscode_data_chart, {title: 'Bars per city'});
      }
    </script>
  </head>
  <body>
    <H1>Bars in Austrian cities</H1>
    <div id="table_div_jscode"></div>
    <div id="chart_div" style="width: 900px; height: 500px;"></div>
  </body>
</html>
"""


def main():
    scraperwiki.sqlite.attach("at_herold_branches")
    
    data = scraperwiki.sqlite.select(
        '''city, branch, count(*) as business from at_herold_branches.swdata
        where branch='was_bars'
        group by city, branch
        order by business desc'''
    )
    
    description = {"city": ("string", "City"),
                   "branch": ("string", "Branch"), 
                   "business": ("number", "Count")}
    
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Creating a JavaScript code string
    jscode = data_table.ToJSCode("jscode_data",
                               columns_order=("city", "branch", "business"))
    # Creating a JSon string
    #json = data_table.ToJSon(columns_order=("city", "branch", "business"),
    #                       order_by="city")
    
    data_chart = scraperwiki.sqlite.select(
        '''city, count(*) as business from at_herold_branches.swdata
        group by city'''
    )
    description_chart = {"city": ("string", "City"),
                   "business": ("number", "Count")}
    data_table_chart = gviz_api.DataTable(description_chart)
    data_table_chart.LoadData(data_chart)
    jscode_chart = data_table_chart.ToJSCode("jscode_data_chart",
                               columns_order=("city", "business"),
                               order_by="city")
    
    print page_template % vars()

main()
