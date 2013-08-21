import scraperwiki
import gviz_api

page_template_1 = """
<html>
  <head>
  <title>Top 10 Banches</title>
    <script src="http://www.google.com/jsapi" type="text/javascript"></script>
    <script>
      google.load("visualization", "1", {packages:["corechart"]});
      google.load("visualization", "1", {packages:["table","corechart"]});

      google.setOnLoadCallback(drawTable);
      function drawTable() {
        """
page_template_2 ="""
      }
    </script>
  </head>
  <body>
    <H1>Top 10 Branches on Herold.at</H1>\n"""
page_template_3="""
  </body>
</html>
"""

def main():
    scraperwiki.sqlite.attach("at_herold_branches")

    description_chart = {"city": ("string", "City"),
        "business": ("number", "Number")}
    script=""
    divs=""    

    #Overview------------------------------------------------------
    data_chart = scraperwiki.sqlite.select(
        """city, count(*) as business from at_herold_branches.swdata
        group by city"""
    )
    data_table_chart = gviz_api.DataTable(description_chart)
    data_table_chart.LoadData(data_chart)
    jscode_chart = data_table_chart.ToJSCode("jscode_data_chart_overview",
                   columns_order=("city", "business"),
                   order_by="city")
    #charts[str(i)]=jscode_chart
    script_tmp = jscode_chart+"""
          var chart = new google.visualization.BarChart(document.getElementById('chart_div_overview'));
          chart.draw(jscode_data_chart_overview, {title: 'Entries per city', isStacked: true});\n"""
    script += script_tmp
    divs += '<div id="chart_div_overview" style="width: 900px; height: 500px;"></div>\n'


    branches = scraperwiki.sqlite.select(
        '''branch from at_herold_branches.swdata
        group by branch'''
    )
    
    #Per branch----------------------------------------------------
    i=0
    for b in branches:
        branch=b["branch"]
        data_chart = scraperwiki.sqlite.select(
            """city, count(*) as business from at_herold_branches.swdata
            where branch='"""+branch+"""'
            group by city"""
        )

        data_table_chart = gviz_api.DataTable(description_chart)
        data_table_chart.LoadData(data_chart)
        jscode_chart = data_table_chart.ToJSCode("jscode_data_chart_"+str(i),
                                   columns_order=("city", "business"),
                                   order_by="city")
        #charts[str(i)]=jscode_chart
        script_tmp = jscode_chart+"""
            var chart = new google.visualization.PieChart(document.getElementById('chart_div_"""+str(i)+"""'));
            chart.draw(jscode_data_chart_"""+str(i)+""", {title: '"""+branch+"""'});\n"""
        script += script_tmp
        divs += '<div id="chart_div_'+str(i)+'" style="width: 900px; height: 500px;"></div>\n'
        i+=1

    page_template=page_template_1+script+page_template_2+divs+page_template_3
    print page_template

main()