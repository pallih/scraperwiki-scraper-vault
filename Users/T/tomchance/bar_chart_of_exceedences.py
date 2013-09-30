import scraperwiki.sqlite
import os, cgi
from pygooglechart import StackedVerticalBarChart, Axis

# Get data
GET = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
print GET
sourcescraper = 'marylebone_air_monitoring_station_values'
scraperwiki.sqlite.attach(sourcescraper, "src")
sdata = scraperwiki.sqlite.execute("select td from src.swdata WHERE no = 4")
rows = sdata.get("data")
pm10val = int(rows[0][0])

# Choose colour based on numbers
if (0 < pm10val < 20):
    colour = '00ff00'
elif (20 < pm10val < 30):
    colour = 'f07f00'
else:
    colour = 'ad0000'

# Draw the bar chart
chart = StackedVerticalBarChart(150, 200, y_range=(0, 50))
chart.set_colours([colour, 'ffffff', 'ffffff'])
chart.set_bar_width(40)
chart.add_data([0,pm10val,0])
chart.add_data([35,1,1])
chart.add_data([1,1,1])
chart.set_axis_labels(Axis.LEFT,[0,25,50])
chart.add_marker(1,0,'tLimit (35)','ad0000',11)
chart.add_marker(0,1,'fSo far (%s)' % (pm10val),colour,11)
chart.add_marker(0,2,'tSafe (0)','45bb00',11)
print '<img src="%s"></img>' % chart.get_url()
import scraperwiki.sqlite
import os, cgi
from pygooglechart import StackedVerticalBarChart, Axis

# Get data
GET = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
print GET
sourcescraper = 'marylebone_air_monitoring_station_values'
scraperwiki.sqlite.attach(sourcescraper, "src")
sdata = scraperwiki.sqlite.execute("select td from src.swdata WHERE no = 4")
rows = sdata.get("data")
pm10val = int(rows[0][0])

# Choose colour based on numbers
if (0 < pm10val < 20):
    colour = '00ff00'
elif (20 < pm10val < 30):
    colour = 'f07f00'
else:
    colour = 'ad0000'

# Draw the bar chart
chart = StackedVerticalBarChart(150, 200, y_range=(0, 50))
chart.set_colours([colour, 'ffffff', 'ffffff'])
chart.set_bar_width(40)
chart.add_data([0,pm10val,0])
chart.add_data([35,1,1])
chart.add_data([1,1,1])
chart.set_axis_labels(Axis.LEFT,[0,25,50])
chart.add_marker(1,0,'tLimit (35)','ad0000',11)
chart.add_marker(0,1,'fSo far (%s)' % (pm10val),colour,11)
chart.add_marker(0,2,'tSafe (0)','45bb00',11)
print '<img src="%s"></img>' % chart.get_url()
