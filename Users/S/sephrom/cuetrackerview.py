import scraperwiki, string
from pygooglechart import PieChart2D

scraperwiki.sqlite.attach("cuetrackernet", "src")
data = scraperwiki.sqlite.select('COUNT(id) AS amount, country, SUM(matchesPlayed) AS matchesPlayedSum, SUM(matchesWon) AS matchesWonSum FROM src.cuetracker GROUP BY country ORDER BY amount DESC')
gb = scraperwiki.sqlite.select('COUNT(id) AS amount, "GB" as country, SUM(matchesPlayed) AS matchesPlayedSum, SUM(matchesWon) AS matchesWonSum FROM src.cuetracker WHERE country IN ("England", "Scotland", "Wales", "Northern Ireland") ORDER BY amount DESC')


print """<script type='text/javascript' src='https://www.google.com/jsapi'></script>
       <script type='text/javascript'>
       google.load('visualization', '1', {'packages': ['geochart']});
       google.setOnLoadCallback(drawRegionsMap);

       function drawRegionsMap() {
         var data = google.visualization.arrayToDataTable([
           ['Country', 'Matches Won'],""";

print "['", gb[0]["country"], "',", gb[0]["matchesWonSum"], "],"

for i, d in enumerate(data):
    print "['", d["country"], "',", d["matchesWonSum"], "]"
    if (i < len(data)-1):
        print ","

print """]);
        var options = {};
        //options['region']='GB'
        var chart = new google.visualization.GeoChart(document.getElementById('chart_div'));
        chart.draw(data, options);
    };
    </script>""";

print '<style type="text/css">'
print 'table { border:1px solid #000; border-collapse:collapse} table tr th { padding:10px; background:#ccc; border-bottom:1px solid #000; } table tr td { padding:5px; border-bottom:1px solid #000; text-align:center } table tr.even { background:#eee; } .left { float:left } #chart_div { width:1024px; height:700px; margin-left:650px; }'
print '</style>'

rank = 1
chartData = []
labels = []

print "<h1>Matches won grouped by country (Season 2012/13)</h1>"
print "<div class='left'><table>"
print "<tr><th>Rank</th><th>Amount</th><th>Country</th><th>Matches Played</th><th>Matches Won</th>"

for d in data:
    print '<tr class="',"odd" if rank % 2 else "even",'">'
    print "<td>", rank , "</td>"
    print "<td>", d["amount"], "</td>"
    print "<td class='country'>", d["country"], "</td>"
    print "<td>", d["matchesPlayedSum"], "</td>"
    print "<td class='matcheswon'>", d["matchesWonSum"], "</td>"
    print "</tr>"

    rank += 1
    chartData.append(d["amount"])
    labels.append(str(d["country"]))

print "</table>"
print "<br /><br />"

chart = PieChart2D(480, 300)
chart.add_data(chartData)
chart.set_pie_labels(labels)

print "<img src='%s' />" % chart.get_url()
print "</div><br /><br />"
print "<div id='chart_div'></div>"
