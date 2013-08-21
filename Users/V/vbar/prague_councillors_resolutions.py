import lxml.html
import scraperwiki
import urlparse

def get_total(page):
    total = 0
    for div in page.xpath("//div[@class='pg-count']"):
        for t in div.xpath("strong/text()"):
            cur = int(t)
            if not total: # count 0 also considered unsatisfactory...
                total = cur
            elif total != cur:
                raise Exception("total count switched from %s to %s" % (total, cur))

    # ...but sometimes there really isn't anything...
    return total

scraperwiki.sqlite.attach('prague_councillors_terms', 'src')
done_period = scraperwiki.sqlite.get_var('period')
input = None
if done_period:
    input = scraperwiki.sqlite.select("* from src.swdata where period_id>%s order by period_id" % done_period)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by period_id")

size = 500 # the maximum
for rd in input:
    period_id = rd['period_id']
    period_desc = rd['period_desc']
    print "starting period " + period_desc

    url = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html?size=%s&periodId=%s&test=value&resolutionNumber=&printNumber=&s=1&meeting=" % ( size, period_id )
    html = scraperwiki.scrape(url)
    page = lxml.html.fromstring(html)
    total = get_total(page)
    if total:
        start = 0
        while True:
            for tr in page.xpath("//table/tbody/tr"):
                tds = tr.xpath("td")
                if tds:
                    for href in tds[-1].xpath("a/@href"): # hopefully exactly one
                        data = { 'period_id': period_id,
                            'resolution': urlparse.urljoin(url, href) }
                        scraperwiki.sqlite.save(unique_keys=['resolution'], data=data)
        
            start += size
            if start >= total:
                break

            url = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html?size=%s&periodId=%s&test=value&resolutionNumber=&printNumber=&s=1&meeting=&start=%s"  % ( size, period_id, start )
            html = scraperwiki.scrape(url)
            page = lxml.html.fromstring(html)
    else:
        print "no resolutions for " + period_desc

    scraperwiki.sqlite.save_var('period', period_id)

