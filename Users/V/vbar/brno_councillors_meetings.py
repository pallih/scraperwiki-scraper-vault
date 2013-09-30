import datetime
import lxml.html
import re
import scraperwiki
import urlparse

base_url = "http://www.dokumenty.brno.cz/main/dokumenty/menu.php?dokument=3&rok=vse&detail=ne&platnost=1"
start_date = datetime.date(2007, 6, 26) # the first record w/ links to vote details

html = scraperwiki.scrape(base_url)
page = lxml.html.fromstring(html)
for a in page.xpath("//a"):
    match = re.match(r'Z.pis ze ZMB[^()]+\((\d\d)\.(\d\d).(\d{4})\)\s*$', a.text_content())
    if match:
        date = datetime.date(int(match.group(3)), int(match.group(2)), int(match.group(1)))
        if date >= start_date:
            data = { 'date': date, 'meeting': urlparse.urljoin(base_url, a.get("href")) }
            scraperwiki.sqlite.save(unique_keys=['date'], data=data)

import datetime
import lxml.html
import re
import scraperwiki
import urlparse

base_url = "http://www.dokumenty.brno.cz/main/dokumenty/menu.php?dokument=3&rok=vse&detail=ne&platnost=1"
start_date = datetime.date(2007, 6, 26) # the first record w/ links to vote details

html = scraperwiki.scrape(base_url)
page = lxml.html.fromstring(html)
for a in page.xpath("//a"):
    match = re.match(r'Z.pis ze ZMB[^()]+\((\d\d)\.(\d\d).(\d{4})\)\s*$', a.text_content())
    if match:
        date = datetime.date(int(match.group(3)), int(match.group(2)), int(match.group(1)))
        if date >= start_date:
            data = { 'date': date, 'meeting': urlparse.urljoin(base_url, a.get("href")) }
            scraperwiki.sqlite.save(unique_keys=['date'], data=data)

