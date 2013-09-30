import scraperwiki
import lxml.html
import time, datetime

now = time.gmtime(time.time())

courts = {'Minneapolis': 'http://www.mnd.uscourts.gov/calendars/mpls/index.html', 'St. Paul': 'http://www.mnd.uscourts.gov/calendars/stp/index.html', 'Duluth': 'http://www.mnd.uscourts.gov/calendars/dul/index.html', 'Fergus Falls & Bemidji': 'http://www.mnd.uscourts.gov/calendars/ff/index.html'}

def convertTime(t):
    """Converts times in format HH:MMPM from CST into seconds from epoch"""
    convertedTime = time.strptime(t + ' ' + str(now.tm_mon) + ' ' + str(now.tm_mday) + ' ' + str(now.tm_year), "%I:%M%p %m %d %Y")
    return time.mktime(convertedTime) + 5*60*60

for court, url in courts.iteritems():
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    # Find the correct table element, skip the first row
    for tr in root.cssselect("table[cellpadding=1] tr")[1:]:
        tds = tr.cssselect("td")
        start = tds[1].text_content().strip()
        end = tds[2].text_content().strip()
        description = tds[3].text_content().strip()
        convertedStart = convertTime(start)
        convertedEnd = convertTime(end)
        
        # We need a unique id so that the same case doesn't overwrite itself when later brought up
        uniqueId = str(time.time()) + ' -- ' + description
        data = {'Start': convertedStart, 'End': convertedEnd, 'Description': description, 'Court': court, 'UniqueId': uniqueId}
        scraperwiki.sqlite.save(unique_keys=['UniqueId'], data=data)

import scraperwiki
import lxml.html
import time, datetime

now = time.gmtime(time.time())

courts = {'Minneapolis': 'http://www.mnd.uscourts.gov/calendars/mpls/index.html', 'St. Paul': 'http://www.mnd.uscourts.gov/calendars/stp/index.html', 'Duluth': 'http://www.mnd.uscourts.gov/calendars/dul/index.html', 'Fergus Falls & Bemidji': 'http://www.mnd.uscourts.gov/calendars/ff/index.html'}

def convertTime(t):
    """Converts times in format HH:MMPM from CST into seconds from epoch"""
    convertedTime = time.strptime(t + ' ' + str(now.tm_mon) + ' ' + str(now.tm_mday) + ' ' + str(now.tm_year), "%I:%M%p %m %d %Y")
    return time.mktime(convertedTime) + 5*60*60

for court, url in courts.iteritems():
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    # Find the correct table element, skip the first row
    for tr in root.cssselect("table[cellpadding=1] tr")[1:]:
        tds = tr.cssselect("td")
        start = tds[1].text_content().strip()
        end = tds[2].text_content().strip()
        description = tds[3].text_content().strip()
        convertedStart = convertTime(start)
        convertedEnd = convertTime(end)
        
        # We need a unique id so that the same case doesn't overwrite itself when later brought up
        uniqueId = str(time.time()) + ' -- ' + description
        data = {'Start': convertedStart, 'End': convertedEnd, 'Description': description, 'Court': court, 'UniqueId': uniqueId}
        scraperwiki.sqlite.save(unique_keys=['UniqueId'], data=data)

