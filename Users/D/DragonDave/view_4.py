# Blank Python
import cgi,os

# Set query_string to source=school_life_expectancy_in_years
query_string = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

try:
    sourcescraper=query_string['source']
except KeyError:
    sourcescraper="school_life_expectancy_in_years"

try:
    title=query_string['title']
except KeyError:
    title = "Title"

try:
    cat=query_string['cat']
except KeyError:
    cat = "country"

try:
    value=query_string['value']
except KeyError:
    value="years_in_school"

try:
    select=query_string['select']
except KeyError:
    select="* from school_life_expectancy_in_years.swdata"

import scraperwiki           
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(select)

data2=[]
for r in data:
    data2.append([r[cat].encode('ascii','ignore'),r[value]]) # encoding it as ASCII is a cheap and lazy hack.

print """
<head>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', '%s');
        data.addColumn('number', '%s');
        data.addRows(%s);
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, {width: 900, height: 600, title: '%s'});
      }
    </script>
</head>
<body>
<div id=chart_div></div>
""" % (cat,value,data2,title)

print query_string