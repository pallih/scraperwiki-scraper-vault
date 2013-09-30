import scraperwiki

sourcescraper = 'hmrc_spending'
scraperwiki.sqlite.attach(sourcescraper, "src")

params = scraperwiki.utils.GET( )
start = params.get("start", "0000-00-00")
end = params.get("end", "9999-99-99")

totdata = scraperwiki.sqlite.execute("SELECT Supplier, strftime('%Y', Date) AS Year, strftime('%m',Date) AS Month, sum(Amount) AS Total FROM src.Refined WHERE Date >= ? AND Date < ? GROUP BY Supplier, Year, Month", (start, end)).get("data")

print """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["motionchart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Supplier');
        data.addColumn('date', 'Date');
        data.addColumn('number', 'Monthly Spend');
"""

print "data.addRows(["

output = ""

for row in totdata:
    output += '["%s",new Date(%s,%s,1), %s],' % (row[0], row[1], row[2], row[3])

print output

print """
]);

        var options = {};

        options['state'] = '{"orderedByY":false,"yZoomedDataMin":0.05,"xAxisOption":"_ALPHABETICAL","orderedByX":false,"showTrails":false,"iconType":"BUBBLE","uniColorForNonSelected":false,"iconKeySettings":[],"yLambda":0,"duration":{"multiplier":1,"timeUnit":"D"},"sizeOption":"2","xZoomedDataMin":0,"xLambda":1,"colorOption":"_UNIQUE_COLOR","xZoomedDataMax":318,"dimensions":{"iconDimensions":["dim0"]},"yZoomedDataMax":213822383.62,"nonSelectedAlpha":0.4,"playDuration":15000,"time":"2010-05-01","yAxisOption":"2","xZoomedIn":false,"yZoomedIn":false};'

        options['width'] = 800;
        options['height'] = 600;
        options['title'] = 'HMRC Spending';

        var chart = new google.visualization.MotionChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>

  <body>
    <h1>HMRC Monthly spend over time</h1>
    <div id="chart_div"></div>
    <a href="http://scraperwiki.com/views/hmrc_daily_spending_graph/">View by Day</a>
    <a href="http://scraperwiki.com/scrapers/hmrc_spending/">Source data</a>
  </body>
</html>
"""import scraperwiki

sourcescraper = 'hmrc_spending'
scraperwiki.sqlite.attach(sourcescraper, "src")

params = scraperwiki.utils.GET( )
start = params.get("start", "0000-00-00")
end = params.get("end", "9999-99-99")

totdata = scraperwiki.sqlite.execute("SELECT Supplier, strftime('%Y', Date) AS Year, strftime('%m',Date) AS Month, sum(Amount) AS Total FROM src.Refined WHERE Date >= ? AND Date < ? GROUP BY Supplier, Year, Month", (start, end)).get("data")

print """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["motionchart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Supplier');
        data.addColumn('date', 'Date');
        data.addColumn('number', 'Monthly Spend');
"""

print "data.addRows(["

output = ""

for row in totdata:
    output += '["%s",new Date(%s,%s,1), %s],' % (row[0], row[1], row[2], row[3])

print output

print """
]);

        var options = {};

        options['state'] = '{"orderedByY":false,"yZoomedDataMin":0.05,"xAxisOption":"_ALPHABETICAL","orderedByX":false,"showTrails":false,"iconType":"BUBBLE","uniColorForNonSelected":false,"iconKeySettings":[],"yLambda":0,"duration":{"multiplier":1,"timeUnit":"D"},"sizeOption":"2","xZoomedDataMin":0,"xLambda":1,"colorOption":"_UNIQUE_COLOR","xZoomedDataMax":318,"dimensions":{"iconDimensions":["dim0"]},"yZoomedDataMax":213822383.62,"nonSelectedAlpha":0.4,"playDuration":15000,"time":"2010-05-01","yAxisOption":"2","xZoomedIn":false,"yZoomedIn":false};'

        options['width'] = 800;
        options['height'] = 600;
        options['title'] = 'HMRC Spending';

        var chart = new google.visualization.MotionChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>

  <body>
    <h1>HMRC Monthly spend over time</h1>
    <div id="chart_div"></div>
    <a href="http://scraperwiki.com/views/hmrc_daily_spending_graph/">View by Day</a>
    <a href="http://scraperwiki.com/scrapers/hmrc_spending/">Source data</a>
  </body>
</html>
"""