from urllib2 import urlopen
from lxml.html import fromstring
from scraperwiki.sqlite import save

# Load
html = urlopen('http://www.cityofmadison.com/cityHall/WeeklySchedule/').read()
x = fromstring(html)

# Select a table
base = x.base_url
print base

table = x.get_element_by_id('list')
trs = table.cssselect('tr')

# Select links
currentdate = None
for tr in trs[6:]:
    tds = tr.cssselect('td')
    if tds[0].attrib.get('colspan'):
        print 'Starting a new date'
        #child = tds[0].cssselect('br')
        currentdate = tds[0].text_content().strip()
        #print child[0].text
    else:
        meetingdate = currentdate + " " + tds[0].text
        location = tds[1][0].text.strip()
        agenda = tds[1][0].attrib.get("href").strip()
        if not agenda.startswith("http"):
            agenda = "http://www.cityofmadison.com" + agenda
        print meetingdate + " " + tds[2].text.strip() + " " + location + " " + agenda
        #links = tr.cssselect('a')
        #print [a.attrib['href'] for a in links]

