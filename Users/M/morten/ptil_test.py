import scraperwiki

import requests
from lxml.html import fromstring

URL = "http://www.ptil.no/nyheter/rapport-etter-tilsyn-med-beredskap-paa-gjoea-article8365-24.html"
req = requests.get(URL)
x = fromstring(req.content)
uls = x.cssselect(".main_content ul")
assert len(uls) == 2

for li in uls[0].cssselect("li"):
    data = {
        "type": "avvik",
        "content": li.text,
        "url": URL
    }
    scraperwiki.sqlite.save([], data)
    
for li in uls[1].cssselect("li"):
    data = {
        "type": "forberdingspunkter",
        "content": li.text,
        "url": URL
    }
    scraperwiki.sqlite.save([], data)import scraperwiki

import requests
from lxml.html import fromstring

URL = "http://www.ptil.no/nyheter/rapport-etter-tilsyn-med-beredskap-paa-gjoea-article8365-24.html"
req = requests.get(URL)
x = fromstring(req.content)
uls = x.cssselect(".main_content ul")
assert len(uls) == 2

for li in uls[0].cssselect("li"):
    data = {
        "type": "avvik",
        "content": li.text,
        "url": URL
    }
    scraperwiki.sqlite.save([], data)
    
for li in uls[1].cssselect("li"):
    data = {
        "type": "forberdingspunkter",
        "content": li.text,
        "url": URL
    }
    scraperwiki.sqlite.save([], data)