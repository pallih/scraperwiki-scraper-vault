import scraperwiki
import lxml.html
import re
from dateutil.relativedelta import *
from dateutil.parser import *
from datetime import *

# Blank Python

html = scraperwiki.scrape("http://www.xcracer.com/UK-Mountain-Bike-Event-Calendar.php")
root = lxml.html.fromstring(html)

for entry_div in root.cssselect("div.spacerblock"):
    #print entry_div.text_content()
    h3s = entry_div.cssselect("h3")
    bs = entry_div.cssselect("b")
    aas = entry_div.cssselect("a")

    title = h3s[0]
    event_date = bs[0]
    event_link = aas[0]

    event_dt = parse(event_date.text_content())

    element_text = lxml.html.tostring(entry_div)
    m = re.search('\|\s(.*?)<', element_text)
    location = m.group(1)

    data = {
        'title' : title.text_content(),
        'date' : event_dt.isoformat(),
        'location' : location,
        'link' : event_link.get("href")
    }

    print data
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)

#print htmlimport scraperwiki
import lxml.html
import re
from dateutil.relativedelta import *
from dateutil.parser import *
from datetime import *

# Blank Python

html = scraperwiki.scrape("http://www.xcracer.com/UK-Mountain-Bike-Event-Calendar.php")
root = lxml.html.fromstring(html)

for entry_div in root.cssselect("div.spacerblock"):
    #print entry_div.text_content()
    h3s = entry_div.cssselect("h3")
    bs = entry_div.cssselect("b")
    aas = entry_div.cssselect("a")

    title = h3s[0]
    event_date = bs[0]
    event_link = aas[0]

    event_dt = parse(event_date.text_content())

    element_text = lxml.html.tostring(entry_div)
    m = re.search('\|\s(.*?)<', element_text)
    location = m.group(1)

    data = {
        'title' : title.text_content(),
        'date' : event_dt.isoformat(),
        'location' : location,
        'link' : event_link.get("href")
    }

    print data
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)

#print html