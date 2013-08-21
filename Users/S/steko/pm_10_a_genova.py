# Blank Python

import scraperwiki

sourcescraper = 'inquinamento_atmosferico_a_genova'

scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select( '''* from inquinamento_atmosferico_a_genova.swdata order by date desc limit 30''' )

def date_to_tuple(datestring):
    y, m, d = datestring.split('-')
    m = int(m) - 1
    return "%s, %s, %s" % (y, m, d)

rws = ''
for d in data:
    if d['value'] is not None:
        rws += "[new Date(%s), %s, 50]," %(date_to_tuple(d['date']),d['value'])
rws = rws + "#"
rws = rws.replace("],#","]")


html = """<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('date', 'Data');
        data.addColumn('number', 'PM10');
        data.addColumn('number', 'Limite');
        data.addRows([%s]);

        var options = {
          width: 500, height: 300,
          title: 'PM10 a Genova, Corso Buenos Aires'
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_div"></div>
  </body>
</html>""" % (rws)

print html
