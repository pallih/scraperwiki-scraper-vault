import scraperwiki

sourcescraper = 'hmrc_spending'
scraperwiki.sqlite.attach(sourcescraper, "src")

params = scraperwiki.utils.GET( )
start = params.get("start", "0000-00-00")
end = params.get("end", "9999-99-99")

totdata = scraperwiki.sqlite.execute("SELECT Supplier, sum(Amount) as Total FROM src.Refined WHERE Date >= ? AND Date < ? GROUP BY Supplier ORDER BY Total DESC",(start, end)).get("data")

print """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Supplier');
        data.addColumn('number', 'Total spent');
"""

print "data.addRows(%d);" % len(totdata)

i = 0
output = ""
for row in totdata:
    output += """data.setValue(%d, 0, "%s");data.setValue(%d, 1, %s);""" % (i, row[0],i,row[1])
    i += 1

print output

print """
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, {width: 1024, height: 768, title: 'HMRC Spending (£)'});
      }
    </script>
  </head>

  <body>
    <div id="chart_div"></div>
  </body>
</html>
"""import scraperwiki

sourcescraper = 'hmrc_spending'
scraperwiki.sqlite.attach(sourcescraper, "src")

params = scraperwiki.utils.GET( )
start = params.get("start", "0000-00-00")
end = params.get("end", "9999-99-99")

totdata = scraperwiki.sqlite.execute("SELECT Supplier, sum(Amount) as Total FROM src.Refined WHERE Date >= ? AND Date < ? GROUP BY Supplier ORDER BY Total DESC",(start, end)).get("data")

print """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Supplier');
        data.addColumn('number', 'Total spent');
"""

print "data.addRows(%d);" % len(totdata)

i = 0
output = ""
for row in totdata:
    output += """data.setValue(%d, 0, "%s");data.setValue(%d, 1, %s);""" % (i, row[0],i,row[1])
    i += 1

print output

print """
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, {width: 1024, height: 768, title: 'HMRC Spending (£)'});
      }
    </script>
  </head>

  <body>
    <div id="chart_div"></div>
  </body>
</html>
"""