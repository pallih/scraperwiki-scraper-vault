###############################################################################
# Simple BBC weather scraper - demonstrates basic use of BeautifulSoup,
# setting up records, and saving records to the data store
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import pygooglechart

# convert a dict of names and values into a horizontal bar chart
def HorizontalBarChart(d, title):
    width = 425
    height = 10*len(d) + 30
    xmax = max(d.values())
    chart = pygooglechart.StackedHorizontalBarChart(width, height, x_range=(0, xmax), colours=["556600"])
    chart.set_legend([title])
    chart.set_bar_width(10)
    data = []
    axis = d.keys()
    axis.sort()
    for key in axis:
        data.append(d[key])
    chart.set_axis_labels(pygooglechart.Axis.LEFT, axis)
    chart.set_axis_labels(pygooglechart.Axis.BOTTOM, map(str, range(0,xmax+1,int(xmax/10))))
    chart.add_data(data)
    return chart

# printable (and thus easier to scrape) version of BBC 5-day weather forecast
html = scraperwiki.scrape('http://news.bbc.co.uk/weather/forecast/8?printco=Forecast')
print html

soup = BeautifulSoup(html)

#extract all the <tr> tags from the document
days = soup.findAll('tr')

for day in days:
    # we only want <tr> tags with a 'day' class - go straight on to next one otherwise
    if day['class'].find('day') == -1:
            continue
    # set up our record
    record = {
        'day': None,
        'summary': None,
        'temp_max_c': None,
    }
    # now get all the <td> tags
    tds = day.findAll('td')
    # name of the day    
    for abbr in tds[0].findAll('abbr'):
        record['day'] = abbr.text
    # maximum temperature
    for span in tds[2].findAll('span'):
        try:
            if span['class'].find('temp max') != -1:
                record['temp_max_c'] = span.findAll('span',{'class':'cent'})[0].text[:-6]
        except:
            pass
    # and finally summary of the weather
    record['summary'] = day.findAll('div', {'class':'summary'})[0].findAll('strong')[0].text.lower()
    print record, '------------'
    # save record to the datastore - 'day' is our unique key
    scraperwiki.datastore.save(["day"], record)
    
#chart = HorizontalBarChart(record, "Temperature chart")
#scraperwiki.metadata.save("chart", chart.get_url())
    

