import datetime
import lxml.html
import re
import scraperwiki
import urlparse

base_url = "http://verejna-sprava.kr-moravskoslezsky.cz/zast_vystupy.html"

def parse_date(s):
    match = re.match(r'\s*(\d+)[.]\D*(\d+)[.]\D*(\d+)', s)
    if match:
        return datetime.date(int(match.group(3)), int(match.group(2)), int(match.group(1)))
    else:
        return None

def extract_url(td):
    href = td.xpath("a/@href")
    if href:
        return urlparse.urljoin(base_url, href[0])
    else:
        return None
    
html = scraperwiki.scrape(base_url)
page = lxml.html.fromstring(html)
for tr in page.xpath("//table/tbody/tr"):
    tds = tr.xpath("td")
    date = parse_date(tds[0].text_content())
    if date:
        data = { 'date': date }
        names = [ 'programme', 'resolutions', 'minutes' ];
        for i in xrange(3):
            val = extract_url(tds[i + 1])
            if val:
                data[names[i]] = val

        if len(data) == 4:
            scraperwiki.sqlite.save(unique_keys=['date'], data=data)

import datetime
import lxml.html
import re
import scraperwiki
import urlparse

base_url = "http://verejna-sprava.kr-moravskoslezsky.cz/zast_vystupy.html"

def parse_date(s):
    match = re.match(r'\s*(\d+)[.]\D*(\d+)[.]\D*(\d+)', s)
    if match:
        return datetime.date(int(match.group(3)), int(match.group(2)), int(match.group(1)))
    else:
        return None

def extract_url(td):
    href = td.xpath("a/@href")
    if href:
        return urlparse.urljoin(base_url, href[0])
    else:
        return None
    
html = scraperwiki.scrape(base_url)
page = lxml.html.fromstring(html)
for tr in page.xpath("//table/tbody/tr"):
    tds = tr.xpath("td")
    date = parse_date(tds[0].text_content())
    if date:
        data = { 'date': date }
        names = [ 'programme', 'resolutions', 'minutes' ];
        for i in xrange(3):
            val = extract_url(tds[i + 1])
            if val:
                data[names[i]] = val

        if len(data) == 4:
            scraperwiki.sqlite.save(unique_keys=['date'], data=data)

