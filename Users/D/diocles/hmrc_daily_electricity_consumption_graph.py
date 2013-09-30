import scraperwiki

sourcescraper = 'hmrc_electricity_usage'
scraperwiki.sqlite.attach(sourcescraper, "src")

params = scraperwiki.utils.GET( )
start = params.get("start", "0000-00-00")
end = params.get("end", "9999-99-99")

totdata = scraperwiki.sqlite.execute("SELECT date(datetime) as date, sum(usage) FROM src.swdata WHERE datetime >= ? AND datetime < ? GROUP BY date ORDER BY date", (start, end)).get("data")

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
        data.addColumn('number', 'Daily Consumption (kWh)');
"""

print "data.addRows(%d);" % len(totdata)

output = ""

i = 0
for row in totdata:
    output += "data.setValue(%d, 0, '%s');data.setValue(%d, 1, %s);" % (i, row[0],i,row[1])
    i += 1

print output

print """
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, {width: 800, height: 600, title: 'HMRC Electricity Consumption'});
      }
    </script>
  </head>

  <body>
    <h1>HMRC Daily electricity consumption over time</h1>
    <p>More precisely, that of 100 Parliament Square, London.</p>
    <div id="chart_div"></div>
    <a href="http://scraperwiki.com/scrapers/hmrc_electricity_usage/">Source data</a>
  </body>
</html>
"""import scraperwiki

sourcescraper = 'hmrc_electricity_usage'
scraperwiki.sqlite.attach(sourcescraper, "src")

params = scraperwiki.utils.GET( )
start = params.get("start", "0000-00-00")
end = params.get("end", "9999-99-99")

totdata = scraperwiki.sqlite.execute("SELECT date(datetime) as date, sum(usage) FROM src.swdata WHERE datetime >= ? AND datetime < ? GROUP BY date ORDER BY date", (start, end)).get("data")

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
        data.addColumn('number', 'Daily Consumption (kWh)');
"""

print "data.addRows(%d);" % len(totdata)

output = ""

i = 0
for row in totdata:
    output += "data.setValue(%d, 0, '%s');data.setValue(%d, 1, %s);" % (i, row[0],i,row[1])
    i += 1

print output

print """
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, {width: 800, height: 600, title: 'HMRC Electricity Consumption'});
      }
    </script>
  </head>

  <body>
    <h1>HMRC Daily electricity consumption over time</h1>
    <p>More precisely, that of 100 Parliament Square, London.</p>
    <div id="chart_div"></div>
    <a href="http://scraperwiki.com/scrapers/hmrc_electricity_usage/">Source data</a>
  </body>
</html>
"""