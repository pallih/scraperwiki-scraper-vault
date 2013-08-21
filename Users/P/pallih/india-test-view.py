# Blank Python
import scraperwiki
from pygooglechart import PieChart3D
from pygooglechart import PieChart2D
from hashlib import md5
import string
import cgi, os


scraperwiki.sqlite.attach( 'elections_in_uttar_pradesh_-_india' )

select_all = 'constituency FROM "uttar-pradesh-elections" LIMIT 10'

#all = scraperwiki.sqlite.select(select_all)


#for a in all:
 #   selection = '* FROM "uttar-pradesh-elections" WHERE "constituency" LIKE "' + a['constituency'] + '"'

#exit()

select = '* FROM "uttar-pradesh-elections" WHERE "constituency" LIKE "Alapur%"'


this = scraperwiki.sqlite.select(select)


print '''

<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Party');
        data.addColumn('number', 'Votes');
        data.addRows([
'''

for t in this:
    print '["'+t['party']+' - ' + t['candidate'] + '",'+t['votes']+'],' 

print '''
       ]);

        var options = {
          title:''' 
print '"Agra Cantt."'

print '''
        };
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>


    <div id="chart_div" style="width: 900px; height: 500px;"></div>
  </body>
</html>

'''


