import scraperwiki

#attach to my data source
scraperwiki.sqlite.attach('rates')

#get monthly average rates
data = scraperwiki.sqlite.select('substr(date,1,7) month, bank, avg(apy) apy from swdata group by month, bank order by month, bank')

#collect data for each month into map
m={}
banks=set()
for d in data:
    if d['month'] not in m: m[d['month']] = dict()
    banks.add(d['bank'])
    m[d['month']][d['bank']]=round(d['apy'],2)

#make a column for each bank
cols = '\n'.join(["data.addColumn('number','%s')"%bank for bank in sorted(banks)]) 

#make a row for each month
rws = ','.join([ "['%s'," % month + ', '.join([ `m[month][bank]` if bank in m[month] else "null" for bank in sorted(banks)]) +']' for month in sorted(m.keys())])

#html for the graph, using the google visualization api
print """<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Date');
        %s
        data.addRows([%s]);
        var options = {
          width: 1200, height: 700,
          title: 'Rates',
          hAxis: {title: 'Month'}
        };
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_div"></div>
  </body>
</html>""" % (cols,rws)

