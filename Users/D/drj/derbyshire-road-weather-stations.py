import scraperwiki
import lxml.html as html

# http://lxml.de/dev/cssselect.html
from lxml.cssselect import CSSSelector
import urllib2

url = "https://docs.google.com/spreadsheet/pub?key=0AitCLahXqqWGdDZCUVcweVFrb3RLOXVycjlKbTNtSXc&output=html"

raw = urllib2.urlopen(url).read()
doc = html.fromstring(raw)
# print html.tostring(doc)

station = []
for row in CSSSelector('tr')(doc):
    tds = list(row)
    if len(tds) < 3:
        continue
    if tds[2].text is None:
        continue
    tds = tds[1:] # remove mystery first element
    # print [x.text for x in tds]
    key = tds[0].text.lower().replace(' ', '')
    if not station:
        station = [{} for _ in tds[1:]]
    # print key
    for i,e in enumerate(tds[1:]):
        t = e.text.strip()
        station[i][key] = t

print station
scraperwiki.sqlite.save(['info'], station)import scraperwiki
import lxml.html as html

# http://lxml.de/dev/cssselect.html
from lxml.cssselect import CSSSelector
import urllib2

url = "https://docs.google.com/spreadsheet/pub?key=0AitCLahXqqWGdDZCUVcweVFrb3RLOXVycjlKbTNtSXc&output=html"

raw = urllib2.urlopen(url).read()
doc = html.fromstring(raw)
# print html.tostring(doc)

station = []
for row in CSSSelector('tr')(doc):
    tds = list(row)
    if len(tds) < 3:
        continue
    if tds[2].text is None:
        continue
    tds = tds[1:] # remove mystery first element
    # print [x.text for x in tds]
    key = tds[0].text.lower().replace(' ', '')
    if not station:
        station = [{} for _ in tds[1:]]
    # print key
    for i,e in enumerate(tds[1:]):
        t = e.text.strip()
        station[i][key] = t

print station
scraperwiki.sqlite.save(['info'], station)