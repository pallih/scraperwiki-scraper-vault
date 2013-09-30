import lxml.html
import re
import scraperwiki
import urlparse

def make_year(s):
    l = len(s)
    if l == 2:
        s = "20" + s
    elif l != 4:
        raise Exception("unknown year " + s)

    return int(s)

base_url = "http://www.ostrava.cz/cs/urad/mesto-a-jeho-organy/zastupitelstvo-mesta/usneseni-zastupitelstva"

html = scraperwiki.scrape(base_url)
page = lxml.html.fromstring(html)
for a in page.xpath("//a[starts-with(text(), 'Volebn')]"):
    href = a.xpath("@href")[0]
    match = re.search(r'volebni-obdobi-(\d+)-(\d+)$', href)
    if match:
        ord = make_year(match.group(1)) + 2 * make_year(match.group(2)) # any function ordering the terms will do
        term_url = urlparse.urljoin(base_url, href) # hrefs are already absolute here, but just in case...
        term_desc = a.text_content()
        data = { 'term_url': term_url, 'term_desc': term_desc, 'ord': ord }
        scraperwiki.sqlite.save(unique_keys=['term_url'], data=data)

import lxml.html
import re
import scraperwiki
import urlparse

def make_year(s):
    l = len(s)
    if l == 2:
        s = "20" + s
    elif l != 4:
        raise Exception("unknown year " + s)

    return int(s)

base_url = "http://www.ostrava.cz/cs/urad/mesto-a-jeho-organy/zastupitelstvo-mesta/usneseni-zastupitelstva"

html = scraperwiki.scrape(base_url)
page = lxml.html.fromstring(html)
for a in page.xpath("//a[starts-with(text(), 'Volebn')]"):
    href = a.xpath("@href")[0]
    match = re.search(r'volebni-obdobi-(\d+)-(\d+)$', href)
    if match:
        ord = make_year(match.group(1)) + 2 * make_year(match.group(2)) # any function ordering the terms will do
        term_url = urlparse.urljoin(base_url, href) # hrefs are already absolute here, but just in case...
        term_desc = a.text_content()
        data = { 'term_url': term_url, 'term_desc': term_desc, 'ord': ord }
        scraperwiki.sqlite.save(unique_keys=['term_url'], data=data)

