# Blank Python
import scraperwiki
sourcescraper = 'filmpolitiets_spillanmeldelser'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select( ''' * from filmpolitiets_spillanmeldelser.swdata order by date desc, verdict desc''' )

# can I learn form this and do the same?
# https://scraperwiki.com/views/rcgp_latest_disease_rate_comparison/

def date_to_tuple(datestring):
    y, m, d = datestring.split('-')
    m = int(m) - 1
    return "%s, %s, %s" % (y, m, d)

rws = ''
for d in data:
    if d['verdict'] is not None:
        rws += "<li><a href='%s'>%s</a>, (<span class='rate'>%s</span>) <span class='date'>%s</span> <br />%s</li>" %(d['url'], d['title'],d['verdict'],d['date'], d['hook'])
#rws = rws + "#"
#rws = rws.replace("],#","]")



# Get the data our of the scraper
pie_data = scraperwiki.sqlite.select(' *, count(verdict) as antall from filmpolitiets_spillanmeldelser.swdata group by verdict') 

# Assemble the HTML to be inserted into the template
pie = ''
pie += 'data.addRows(' +str(len(pie_data)) + ');'
for counter, datum in enumerate(pie_data):
    pie += 'data.setValue(' + str(counter) + ', 0, "' + datum['verdict'] + '");\n'
    pie += 'data.setValue(' + str(counter) + ', 1, ' + str(datum['antall']) + ');\n'


html = """<html>
  <head>
    <meta charset="utf-8">
    <style>
    span.rate{color:blue;font-size:1.5em;}   
    span.date{color:gray;} 
    body {background-color:#E0E8ED;}
    </style>
    <title>NRK P3s spillanmeldelser etter terningkast</title>
    <script type="text/javascript" src="http://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load('visualization', '1', {packages: ['corechart']});
    </script>
    <script type="text/javascript">
        function drawVisualization() {
            // Create and populate the data table.
            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Terningkast');
            data.addColumn('number', 'antall');
            
            %s

        // Create and draw the visualization.
        new google.visualization.PieChart(document.getElementById('chart_div')).
            draw(data, {title:"NRK p3s Filmpolitiets spillanmeldelser etter terningkast"});
      }

      google.setOnLoadCallback(drawVisualization);
    
    </script>
  </head>
  <body>
<div id="chart_div" style="width: 450px; height: 500px; float:left;"></div>
<h2>Alle anmeldelsene etter dato:</h2>
    <div id="mystuff" style="width:400px;float:left;">
<ul>
    %s
</ul>
    </div>
<footer style="clear:both;">Laget av <a href="http://www.stavelin.com/blog">Eiriks</a></footer>
  </body>
</html>""" % (pie,rws)

print html

