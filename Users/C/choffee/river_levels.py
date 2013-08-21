import scraperwiki
import lxml.html
import re
import dateutil.parser

# York Rivers
StationIDS=[8081,8235,8234,8208]

river_re = re.compile('The river level at ([A-Za-z ]+) is ([0-9.]+) metres')
date_re = re.compile('This measurement was recorded at (\d\d:\d\d) on (\d\d/\d\d/\d\d\d\d).')

for station in StationIDS:
    html = scraperwiki.scrape("http://www.environment-agency.gov.uk/homeandleisure/floods/riverlevels/120701.aspx?stationId=%s" % station)
    root = lxml.html.fromstring(html)

    for div in root.cssselect(".bl > div:nth-child(2) > p:nth-child(1)"):
        print div.text
        match = river_re.search(div.text)
        name = match.group(1)
        level = match.group(2)
        print name,level
    for div in root.cssselect(".bl > div:nth-child(2) > p:nth-child(2)"):
        print div.text
        match = date_re.search(div.text)
        time = match.group(1)
        date = match.group(2)
        print time, date
        datetime = dateutil.parser.parse("%s %s" % (time, date),dayfirst=True )
        print datetime.date(), datetime.time()
    data = {
      'name':name,
      'level':level,
      'datetime':datetime
    }
    scraperwiki.sqlite.save(unique_keys=['name','datetime'], data=data)


