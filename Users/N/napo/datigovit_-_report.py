# Blank Python
import scraperwiki

sourcescraper = 'datigovit'
scraperwiki.sqlite.attach(sourcescraper)
datasets_distribution = scraperwiki.sqlite.select( '''manager,count(id) as total from datigovit.swdata group by manager order by total desc, manager desc''' )
total_datasets = scraperwiki.sqlite.select( '''count(id) as total from datigovit.swdata''' )[0]["total"]
tm =  scraperwiki.sqlite.select( '''count(distinct(manager)) as total from datigovit.swdata''')[0]["total"]
nolicense_datasets = scraperwiki.sqlite.select( '''count(id) as total from datigovit.swdata where license="no"''' )[0]["total"]
withlicense_datasets = total_datasets-nolicense_datasets
use_licenses = scraperwiki.sqlite.select( '''license,count(id) as total from datigovit.swdata group by license order by total desc, license desc''' )
tot_license = scraperwiki.sqlite.select( '''count(distinct(license)) as total from datigovit.swdata''')[0]["total"]
rws = ''
rwl = ''
for d in use_licenses:
    rwl += "['%s',    %s]," %(d['license'],d['total'])
rwl = rwl + "#"
rwl = rwl.replace("],#","]")

for d in datasets_distribution:
    rws += "['%s',    %s]," %(d['manager'],d['total'])
rws = rws + "#"
rws = rws.replace("],#","]")

print """
<html>
<head>
<title>report dati.gov.it</title>
<script type='text/javascript' src='https://www.google.com/jsapi'></script>
<script type="text/javascript">
      google.load("visualization", '1', {packages:['corechart']});
      google.load('visualization', '1', {packages:['table']});
      google.setOnLoadCallback(drawChart);
      google.setOnLoadCallback(drawTable);
      google.setOnLoadCallback(drawTableLicenses);
      google.setOnLoadCallback(drawChartLicense);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'owner');
        data.addColumn('number', 'num datasets');
        data.addRows([%s]);
        var options = {
          width: 640, height: 480,
          title: 'datasets distribution'
        };

        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }

      function drawTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'owner');
        data.addColumn('number', 'num datasets');
        data.addRows(%s); """ % (rws,(tm))
c = 0
for d in datasets_distribution:
        print "        data.setCell(%s, 0, '%s');" % (c,d['manager'])
        print "        data.setCell(%s, 1, %s);" % (c,d['total'])
        c +=1

print """
        var table = new google.visualization.Table(document.getElementById('table_div'));
        table.draw(data, {'page':'enable','pageSize':6,'showRowNumber':true,'width':'300px'});
      }
      function drawTableLicenses() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'license');
        data.addColumn('number', 'num datasets');
        data.addRows(%s); """ % (tot_license)
c = 0
for d in use_licenses:
        print "        data.setCell(%s, 0, '%s');" % (c,d['license'])
        print "        data.setCell(%s, 1, %s);" % (c,d['total'])
        c +=1
print """
        var table = new google.visualization.Table(document.getElementById('tablelicense_div'));
        table.draw(data, {'page':'enable','pageSize':10,'showRowNumber':true,'width':'300px'});
      }
      function drawChartLicense() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'license');
        data.addColumn('number', 'num datasets');
        data.addRows([%s]);
        var options = {
          width: 640, height: 480,
          title: 'datasets distribution'
        };

        var chart = new google.visualization.BarChart(document.getElementById('chartlicense_div'));
        chart.draw(data, options);
      }
</script>

</head>
<body style='font-family: arial, geneva, helvetica, verdana;font-size: 10px'>
<h1>report dati.gov.it</h1>
<h2>Totale datasets: %s</h2>
<h3>Dataset distribuiti per ente</h3>
<table>
<tr>
<td align="top">
<div id="table_div"></div>
</td>
<td>
<div id="chart_div"></div>
</td>
</tr>
</table>
<h3>Dataset distribuiti per licenza</h3>
<table>
<tr>
<td align="top">
<div id="tablelicense_div"></div>
</td>
<td>
<div id="chartlicense_div"></div>
</td>
</tr>
</table>

</body>
</html>""" % (rwl,total_datasets)




# Blank Python
import scraperwiki

sourcescraper = 'datigovit'
scraperwiki.sqlite.attach(sourcescraper)
datasets_distribution = scraperwiki.sqlite.select( '''manager,count(id) as total from datigovit.swdata group by manager order by total desc, manager desc''' )
total_datasets = scraperwiki.sqlite.select( '''count(id) as total from datigovit.swdata''' )[0]["total"]
tm =  scraperwiki.sqlite.select( '''count(distinct(manager)) as total from datigovit.swdata''')[0]["total"]
nolicense_datasets = scraperwiki.sqlite.select( '''count(id) as total from datigovit.swdata where license="no"''' )[0]["total"]
withlicense_datasets = total_datasets-nolicense_datasets
use_licenses = scraperwiki.sqlite.select( '''license,count(id) as total from datigovit.swdata group by license order by total desc, license desc''' )
tot_license = scraperwiki.sqlite.select( '''count(distinct(license)) as total from datigovit.swdata''')[0]["total"]
rws = ''
rwl = ''
for d in use_licenses:
    rwl += "['%s',    %s]," %(d['license'],d['total'])
rwl = rwl + "#"
rwl = rwl.replace("],#","]")

for d in datasets_distribution:
    rws += "['%s',    %s]," %(d['manager'],d['total'])
rws = rws + "#"
rws = rws.replace("],#","]")

print """
<html>
<head>
<title>report dati.gov.it</title>
<script type='text/javascript' src='https://www.google.com/jsapi'></script>
<script type="text/javascript">
      google.load("visualization", '1', {packages:['corechart']});
      google.load('visualization', '1', {packages:['table']});
      google.setOnLoadCallback(drawChart);
      google.setOnLoadCallback(drawTable);
      google.setOnLoadCallback(drawTableLicenses);
      google.setOnLoadCallback(drawChartLicense);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'owner');
        data.addColumn('number', 'num datasets');
        data.addRows([%s]);
        var options = {
          width: 640, height: 480,
          title: 'datasets distribution'
        };

        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }

      function drawTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'owner');
        data.addColumn('number', 'num datasets');
        data.addRows(%s); """ % (rws,(tm))
c = 0
for d in datasets_distribution:
        print "        data.setCell(%s, 0, '%s');" % (c,d['manager'])
        print "        data.setCell(%s, 1, %s);" % (c,d['total'])
        c +=1

print """
        var table = new google.visualization.Table(document.getElementById('table_div'));
        table.draw(data, {'page':'enable','pageSize':6,'showRowNumber':true,'width':'300px'});
      }
      function drawTableLicenses() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'license');
        data.addColumn('number', 'num datasets');
        data.addRows(%s); """ % (tot_license)
c = 0
for d in use_licenses:
        print "        data.setCell(%s, 0, '%s');" % (c,d['license'])
        print "        data.setCell(%s, 1, %s);" % (c,d['total'])
        c +=1
print """
        var table = new google.visualization.Table(document.getElementById('tablelicense_div'));
        table.draw(data, {'page':'enable','pageSize':10,'showRowNumber':true,'width':'300px'});
      }
      function drawChartLicense() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'license');
        data.addColumn('number', 'num datasets');
        data.addRows([%s]);
        var options = {
          width: 640, height: 480,
          title: 'datasets distribution'
        };

        var chart = new google.visualization.BarChart(document.getElementById('chartlicense_div'));
        chart.draw(data, options);
      }
</script>

</head>
<body style='font-family: arial, geneva, helvetica, verdana;font-size: 10px'>
<h1>report dati.gov.it</h1>
<h2>Totale datasets: %s</h2>
<h3>Dataset distribuiti per ente</h3>
<table>
<tr>
<td align="top">
<div id="table_div"></div>
</td>
<td>
<div id="chart_div"></div>
</td>
</tr>
</table>
<h3>Dataset distribuiti per licenza</h3>
<table>
<tr>
<td align="top">
<div id="tablelicense_div"></div>
</td>
<td>
<div id="chartlicense_div"></div>
</td>
</tr>
</table>

</body>
</html>""" % (rwl,total_datasets)




