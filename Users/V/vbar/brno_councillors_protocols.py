import lxml.html
import re
import scraperwiki
import urlparse

scraperwiki.sqlite.attach('brno_councillors_minutes', 'src')
done_date = scraperwiki.sqlite.get_var('date')
if done_date:
    input = scraperwiki.sqlite.select("* from src.swdata where date>%s order by date" % done_date)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by date")

for rd in input:
    date = rd['date']
    base_url = rd['url']
    html = scraperwiki.scrape(base_url)
    page = lxml.html.fromstring(html)
    anchors = page.xpath("//a")
    found = False
    for a in anchors:
        if re.match(r'protokol\s+o\s+hlasov', a.text_content().lower()):
            data = { 'date': date,
                'protocol': urlparse.urljoin(base_url, a.get("href")) }
            scraperwiki.sqlite.save(unique_keys=['protocol'], data=data)
            found = True

    if anchors and not found: # some minutes really don't have any links
        raise Exception("no protocols in " + base_url)

    scraperwiki.sqlite.save_var('date', date)

