import scraperwiki

sourcescraper = 'hmrc_spending'
scraperwiki.sqlite.attach(sourcescraper, "src")

params = scraperwiki.utils.GET( )
start = params.get("start", "0000-00-00")
end = params.get("end", "9999-99-99")

totdata = scraperwiki.sqlite.execute("SELECT Date, sum(Amount) FROM src.Refined WHERE Date >= ? AND Date < ? GROUP BY Date ORDER BY Date", (start, end)).get("data")

print """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Date');
        data.addColumn('number', 'Daily Spend');
"""

print "data.addRows(%d);" % len(totdata)

i = 0
for row in totdata:
    print "data.setValue(%d, 0, '%s');data.setValue(%d, 1, %s);" % (i, row[0],i,row[1])
    i += 1

print """
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, {width: 800, height: 600, title: 'HMRC Spending'});
      }
    </script>
  </head>

  <body>
    <h1>HMRC Daily spend over time</h1>
    <div id="chart_div"></div>
    <a href="http://scraperwiki.com/views/hmrc_monthly_spending_graph/">View by Month</a>
    <a href="http://scraperwiki.com/scrapers/hmrc_spending/">Source data</a>
  </body>
</html>
"""import scraperwiki

sourcescraper = 'hmrc_spending'
scraperwiki.sqlite.attach(sourcescraper, "src")

params = scraperwiki.utils.GET( )
start = params.get("start", "0000-00-00")
end = params.get("end", "9999-99-99")

totdata = scraperwiki.sqlite.execute("SELECT Date, sum(Amount) FROM src.Refined WHERE Date >= ? AND Date < ? GROUP BY Date ORDER BY Date", (start, end)).get("data")

print """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Date');
        data.addColumn('number', 'Daily Spend');
"""

print "data.addRows(%d);" % len(totdata)

i = 0
for row in totdata:
    print "data.setValue(%d, 0, '%s');data.setValue(%d, 1, %s);" % (i, row[0],i,row[1])
    i += 1

print """
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, {width: 800, height: 600, title: 'HMRC Spending'});
      }
    </script>
  </head>

  <body>
    <h1>HMRC Daily spend over time</h1>
    <div id="chart_div"></div>
    <a href="http://scraperwiki.com/views/hmrc_monthly_spending_graph/">View by Month</a>
    <a href="http://scraperwiki.com/scrapers/hmrc_spending/">Source data</a>
  </body>
</html>
"""