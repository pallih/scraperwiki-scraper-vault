import lxml.html
import re
import scraperwiki
import urlparse

scraperwiki.sqlite.attach('moravian_representatives_meetings', 'src')
done_date = scraperwiki.sqlite.get_var('mdate', "2008-10-10") # earlier minutes don't have vote details
input = scraperwiki.sqlite.select("* from src.swdata where date(date)>date('%s') order by date(date)" % done_date)

old_date = None
for rd in input:
    date = rd['date']
    base_url = rd['minutes']
    html = scraperwiki.scrape(base_url)
    page = lxml.html.fromstring(html)
    for a in page.xpath("//a"):
        match = re.match(r'po.adov. hlasov.n\D+(\d+)', a.text_content())
        if match:
            data = { 'date': date,
                'vote_no': int(match.group(1)),
                'vote': urlparse.urljoin(base_url, a.xpath("@href")[0])
            }
            scraperwiki.sqlite.save(unique_keys=['date', 'vote_no'], data=data)

    if old_date:
        if old_date != date:
            scraperwiki.sqlite.save_var('mdate', old_date)
            old_date = date
    else:
        old_date = date


