# Blank Python

import scraperwiki
import lxml.html
import datetime

url = "http://news.bbc.co.uk/weather/forecast/4270?area=CH3"
html = scraperwiki.scrape(url) 
root = lxml.html.fromstring(html)
table = root.cssselect("table.five-day-forecast")

days = ['n5_DayA', 'n5_DayB', 'n5_DayC', 'n5_DayD', 'n5_DayE']

for index, day in enumerate(days):
    tr = table[0].cssselect("tr#%s" % day)[0]

    datepoint = datetime.date.today() + datetime.timedelta(days=index)
    weekday = tr.cssselect('abbr')[0].values()[0]
    summary = tr.cssselect('p.sum')[0].text_content()

    maxstring = tr.cssselect('span.max')[0].cssselect('span.cent')[0].text_content()
    maximum = int(maxstring.replace(u'\xb0C',''))


    minstring = tr.cssselect('span.min')[0].cssselect('span.cent')[0].text_content()
    minimum = int(minstring.replace(u'\xb0C',''))

    humpresvis = tr.cssselect('td.humpresvis')[0]

    humidity_text = humpresvis.cssselect("span.hum")[0].text_content()
    humidity = int(humidity_text.strip().replace('%', ''))

    pressure_text = humpresvis.cssselect("span.pres")[0].text_content()
    pressure = int(pressure_text.strip().replace('mb',''))

    visibility_text = humpresvis.cssselect("span.vis")[0].text_content()
    visibility = visibility_text.strip()

    data = {
        'time_logged' : datetime.datetime.now(),
        'datepoint' : datepoint,
        'weekday' : weekday,
        'summary' : summary,
        'maximum' : maximum,
        'minimum' : minimum,
        'humidity' : humidity,
        'pressure' : pressure,
        'visibility' : visibility,
        
        }
    scraperwiki.sqlite.save(unique_keys=['time_logged'], data=data)
    

root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    print data

