import scraperwiki
import lxml.html
from datetime import datetime, date, time
import re

html = scraperwiki.scrape("http://www.lanuv.nrw.de/luft/immissionen/aktluftqual/eu_luft_akt.htm") 
root = lxml.html.fromstring(html) 

# fetch date and time of last update
h2s = root.cssselect("h2")
datetimestr = re.search('Messwerte am (?P<date>.+) um (?P<time>.+)\r Uhr', h2s[0].text_content()) # "Messwerte am 17.11.2012 um 15:00 Uhr (MEZ)"
timestamp = datetime.strptime('{0} {1}'.format(datetimestr.group('date'), datetimestr.group('time')), '%d.%m.%Y %H:%M')
print timestamp

# fetch data
for tbl in root.cssselect("table"):
    for trs in tbl.cssselect("tr"):
        tds = trs.cssselect("td")

        if len(tds) >= 5:
            data = {
                'name' : tds[0].text_content(),
                'date' : timestamp,
                'ozon' : tds[2].text_content(),
                'so2' : tds[3].text_content(), # doesn't match if td content is "<10"?
                'no2' : tds[4].text_content(),
                'pm10' : tds[5].text_content(),
            }

            if re.match(u'M\u00FCnster.+', data['name']): # filter only Münster stations
                print data
                scraperwiki.sqlite.save(unique_keys=['name', 'date'], data=data)
import scraperwiki
import lxml.html
from datetime import datetime, date, time
import re

html = scraperwiki.scrape("http://www.lanuv.nrw.de/luft/immissionen/aktluftqual/eu_luft_akt.htm") 
root = lxml.html.fromstring(html) 

# fetch date and time of last update
h2s = root.cssselect("h2")
datetimestr = re.search('Messwerte am (?P<date>.+) um (?P<time>.+)\r Uhr', h2s[0].text_content()) # "Messwerte am 17.11.2012 um 15:00 Uhr (MEZ)"
timestamp = datetime.strptime('{0} {1}'.format(datetimestr.group('date'), datetimestr.group('time')), '%d.%m.%Y %H:%M')
print timestamp

# fetch data
for tbl in root.cssselect("table"):
    for trs in tbl.cssselect("tr"):
        tds = trs.cssselect("td")

        if len(tds) >= 5:
            data = {
                'name' : tds[0].text_content(),
                'date' : timestamp,
                'ozon' : tds[2].text_content(),
                'so2' : tds[3].text_content(), # doesn't match if td content is "<10"?
                'no2' : tds[4].text_content(),
                'pm10' : tds[5].text_content(),
            }

            if re.match(u'M\u00FCnster.+', data['name']): # filter only Münster stations
                print data
                scraperwiki.sqlite.save(unique_keys=['name', 'date'], data=data)
