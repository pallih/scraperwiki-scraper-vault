import scraperwiki.sqlite
from pygooglechart import StackedVerticalBarChart, Axis

# Get data
sourcescraper = 'annual_animal_deaths'
scraperwiki.sqlite.attach(sourcescraper, "src")
sdata = scraperwiki.sqlite.execute("select Year, Dates, State, Location, Mortality from src.swdata WHERE Mortality > 1000")


rows = sdata.get("data")
print rows
#    for row in rows:
#        pm10val = int(rows[4])
#        print pm10val 
pm10val = int(rows[0][4])

colour = 'ad0000'    


# Draw the bar chart
chart = StackedVerticalBarChart(150, 200, y_range=(0, 4000))
chart.set_colours([colour, 'ffffff', 'ffffff'])
chart.set_bar_width(40)
chart.add_data([0,pm10val,0])
chart.add_data([35,1,1])
chart.add_data([1,1,1])
chart.set_axis_labels(Axis.LEFT,[0,25,50])
chart.add_marker(1,0,'tLimit (35)','ad0000',11)
chart.add_marker(0,1,'fSo far (%s)' % (pm10val),colour,11)
chart.add_marker(0,2,'tSafe (0)','45bb00',11)
#print '<img src="%s"></img>' % chart.get_url()
