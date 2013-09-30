import lxml.html
import re
import scraperwiki
import urllib2
import urlparse

scraperwiki.sqlite.attach('ostrava_councillors_meetings', 'src')
done_ord = scraperwiki.sqlite.get_var('mord')
if done_ord:
    input = scraperwiki.sqlite.select("* from src.swdata where ord>%s order by ord" % done_ord)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by ord")

for rd in input:
    ord = rd['ord']
    base_url = rd['meeting_url']
    # scraperwiki.scrape apparently doesn't have a way to get the redirected URL
    rsp = urllib2.urlopen(base_url)
    base_url = rsp.geturl()
    html = rsp.read()
    page = lxml.html.fromstring(html)

    base_href = page.xpath("/html/head/base/@href")
    if base_href:
        base_url = base_href[0]

    for tr in page.xpath("//table/tr"):    
        tds = tr.xpath("td")
        if len(tds) == 6:
            cls = tds[0].xpath("@class")
            if len(cls) == 1 and cls[0] == "hvalue_c":
                match = re.match(r'\s*(\d+)\s*$', tds[0].text_content())
                if match:
                    vote_no = int(match.group(1))
                    raw_href = tds[3].xpath("a/@href")[0]
                    href = re.sub(r'\s+', '', raw_href)
                    data = { 'vote_no': 1000 * ord + vote_no, # global for Ostrava Councillors, increasing in time
                        'vote_url': urlparse.urljoin(base_url, href) }
                    scraperwiki.sqlite.save(unique_keys=['vote_no'], data=data)

    scraperwiki.sqlite.save_var('mord', ord)

import lxml.html
import re
import scraperwiki
import urllib2
import urlparse

scraperwiki.sqlite.attach('ostrava_councillors_meetings', 'src')
done_ord = scraperwiki.sqlite.get_var('mord')
if done_ord:
    input = scraperwiki.sqlite.select("* from src.swdata where ord>%s order by ord" % done_ord)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by ord")

for rd in input:
    ord = rd['ord']
    base_url = rd['meeting_url']
    # scraperwiki.scrape apparently doesn't have a way to get the redirected URL
    rsp = urllib2.urlopen(base_url)
    base_url = rsp.geturl()
    html = rsp.read()
    page = lxml.html.fromstring(html)

    base_href = page.xpath("/html/head/base/@href")
    if base_href:
        base_url = base_href[0]

    for tr in page.xpath("//table/tr"):    
        tds = tr.xpath("td")
        if len(tds) == 6:
            cls = tds[0].xpath("@class")
            if len(cls) == 1 and cls[0] == "hvalue_c":
                match = re.match(r'\s*(\d+)\s*$', tds[0].text_content())
                if match:
                    vote_no = int(match.group(1))
                    raw_href = tds[3].xpath("a/@href")[0]
                    href = re.sub(r'\s+', '', raw_href)
                    data = { 'vote_no': 1000 * ord + vote_no, # global for Ostrava Councillors, increasing in time
                        'vote_url': urlparse.urljoin(base_url, href) }
                    scraperwiki.sqlite.save(unique_keys=['vote_no'], data=data)

    scraperwiki.sqlite.save_var('mord', ord)

