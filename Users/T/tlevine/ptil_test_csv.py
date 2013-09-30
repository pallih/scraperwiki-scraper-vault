import csv
import requests
from lxml.html import fromstring

URL = "http://www.ptil.no/nyheter/rapport-etter-tilsyn-med-beredskap-paa-gjoea-article8365-24.html"
req = requests.get(URL)
html = req.content.replace('&nbsp;',' ').encode('utf-8')
x = fromstring(html)
uls = x.cssselect(".main_content ul")
assert len(uls) == 2


f = open('petrol.csv', 'wb')
writer = csv.DictWriter(f,['type','content','url'])

for li in uls[0].cssselect("li"):
    data = {
        "type": "avvik",
        "content": li.text.strip(),
        "url": URL
    }
    writer.writerow(data)

for li in uls[1].cssselect("li"):
    data = {
        "type": "forberdingspunkter",
        "content": li.text.strip(),
        "url": URL
    }
    writer.writerow(data)
import csv
import requests
from lxml.html import fromstring

URL = "http://www.ptil.no/nyheter/rapport-etter-tilsyn-med-beredskap-paa-gjoea-article8365-24.html"
req = requests.get(URL)
html = req.content.replace('&nbsp;',' ').encode('utf-8')
x = fromstring(html)
uls = x.cssselect(".main_content ul")
assert len(uls) == 2


f = open('petrol.csv', 'wb')
writer = csv.DictWriter(f,['type','content','url'])

for li in uls[0].cssselect("li"):
    data = {
        "type": "avvik",
        "content": li.text.strip(),
        "url": URL
    }
    writer.writerow(data)

for li in uls[1].cssselect("li"):
    data = {
        "type": "forberdingspunkter",
        "content": li.text.strip(),
        "url": URL
    }
    writer.writerow(data)
