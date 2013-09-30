import lxml.html
import re
import scraperwiki
import urlparse

scraperwiki.sqlite.attach('ostrava_councillors_terms', 'src')
done_ord = scraperwiki.sqlite.get_var('tord')
if done_ord:
    input = scraperwiki.sqlite.select("* from src.swdata where ord>=%s order by ord" % done_ord)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by ord")

for rd in input:
    ord = rd['ord']
    base_url = rd['term_url']
    html = scraperwiki.scrape(base_url)
    page = lxml.html.fromstring(html)

    # this should actually be done everywhere before using urljoin, but this scraper is
    # the first one that actually needs it...
    base_href = page.xpath("/html/head/base/@href")
    if base_href:
        base_url = base_href[0]

    for tr in page.xpath("//table/tbody/tr"):
        tds = tr.xpath("td")
        if len(tds) == 5:
            match = re.search(r'(\d+)[.]', tds[0].text_content())
            if match:
                meeting_no = int(match.group(1))    
                for a in tds[3].xpath("a"): # 0 or 1
                    if re.match(r'\s*Hlasov', a.text_content()):
                        href = a.xpath("@href")[0]
                        data = { 'meeting_url': urlparse.urljoin(base_url, href),
                            'ord': 100 * ord + meeting_no } # max meeting count is 42
                        scraperwiki.sqlite.save(unique_keys=['meeting_url'], data=data)

    scraperwiki.sqlite.save_var('tord', ord)

import lxml.html
import re
import scraperwiki
import urlparse

scraperwiki.sqlite.attach('ostrava_councillors_terms', 'src')
done_ord = scraperwiki.sqlite.get_var('tord')
if done_ord:
    input = scraperwiki.sqlite.select("* from src.swdata where ord>=%s order by ord" % done_ord)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by ord")

for rd in input:
    ord = rd['ord']
    base_url = rd['term_url']
    html = scraperwiki.scrape(base_url)
    page = lxml.html.fromstring(html)

    # this should actually be done everywhere before using urljoin, but this scraper is
    # the first one that actually needs it...
    base_href = page.xpath("/html/head/base/@href")
    if base_href:
        base_url = base_href[0]

    for tr in page.xpath("//table/tbody/tr"):
        tds = tr.xpath("td")
        if len(tds) == 5:
            match = re.search(r'(\d+)[.]', tds[0].text_content())
            if match:
                meeting_no = int(match.group(1))    
                for a in tds[3].xpath("a"): # 0 or 1
                    if re.match(r'\s*Hlasov', a.text_content()):
                        href = a.xpath("@href")[0]
                        data = { 'meeting_url': urlparse.urljoin(base_url, href),
                            'ord': 100 * ord + meeting_no } # max meeting count is 42
                        scraperwiki.sqlite.save(unique_keys=['meeting_url'], data=data)

    scraperwiki.sqlite.save_var('tord', ord)

