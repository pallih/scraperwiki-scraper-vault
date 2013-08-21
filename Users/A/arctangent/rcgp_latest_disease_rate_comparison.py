# Views proof of concept
# Mad props to the Google Charts API peeps

import scraperwiki
scraperwiki.sqlite.attach('rcgp_latest_communicable_and_respiratory_diseases_')

# Get the data our of the scraper
data = scraperwiki.sqlite.select('* from rcgp_latest_communicable_and_respiratory_diseases_.swdata')

# Assemble the HTML to be inserted into the template
data_html = ''
data_html += 'data.addRows(' +str(len(data)) + ');'
for counter, datum in enumerate(data):
    data_html += 'data.setValue(' + str(counter) + ', 0, "' + datum['disease'] + '");\n'
    data_html += 'data.setValue(' + str(counter) + ', 1, ' + str(datum['rate']) + ');\n'


template_start = '''
<!--
You are free to copy and use this sample in accordance with the terms of the
Apache license (http://www.apache.org/licenses/LICENSE-2.0.html)
-->

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <title>
      Google Visualization API Sample
    </title>
    <script type="text/javascript" src="http://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load('visualization', '1', {packages: ['corechart']});
    </script>
    <script type="text/javascript">
      function drawVisualization() {
        // Create and populate the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Disease');
        data.addColumn('number', 'Rate per 100,000');
'''

template_end = '''

        // Create and draw the visualization.
        new google.visualization.PieChart(document.getElementById('visualization')).
            draw(data, {title:"Latest relative incidence of communicable and respiratory diseases per 100,000"});
      }
      

      google.setOnLoadCallback(drawVisualization);
    </script>
  </head>
  <body style="font-family: Arial;border: 0 none;">
    <div id="visualization" style="width: 600px; height: 400px;"></div>
  </body>
</html>
'''

print template_start + data_html + template_end