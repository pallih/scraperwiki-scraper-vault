import scraperwiki
from scraperwiki.sqlite import save
from lxml.html import fromstring, tostring
data = {
    "place": "dc",
    "date": "2012-03-30"
}

# Blank Python

save([], data)
from urllib2 import urlopen

page = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
headers = ['cie', '2', '3', '4', '5', '6', '7','8','9','10','11']
rawtext = page.read()

html=fromstring(rawtext)
tds = html.cssselect('td')
table = html.cssselect('table')[2]
trs = table.cssselect('tr')
for tr in trs:
    tds = tr.cssselect('td')
    values = [td.text_content() for td in tds]
    data = dict(zip(headers, values))
    links = tr.cssselect('a')
    if len(links)>0:
        print links[0].attrib['href']import scraperwiki
from scraperwiki.sqlite import save
from lxml.html import fromstring, tostring
data = {
    "place": "dc",
    "date": "2012-03-30"
}

# Blank Python

save([], data)
from urllib2 import urlopen

page = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
headers = ['cie', '2', '3', '4', '5', '6', '7','8','9','10','11']
rawtext = page.read()

html=fromstring(rawtext)
tds = html.cssselect('td')
table = html.cssselect('table')[2]
trs = table.cssselect('tr')
for tr in trs:
    tds = tr.cssselect('td')
    values = [td.text_content() for td in tds]
    data = dict(zip(headers, values))
    links = tr.cssselect('a')
    if len(links)>0:
        print links[0].attrib['href']