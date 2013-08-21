import scraperwiki
import lxml.html


html = scraperwiki.scrape('http://www.bvk.cz/odpovedi-faq/prumerna-spotreba-vody/')
html = html.replace('&#160;', '')
root = lxml.html.fromstring(html)

for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")

    if tds[0].text_content().isdigit() is False:
        continue
    consum = tds[1].text_content().replace(' ', '').replace(',','.')
    data = {
        'year' : int(tds[0].text_content()),
        'consumption' : float(consum),
    }
    scraperwiki.sqlite.save(unique_keys=['year'], data = data)
