import datetime
import lxml.html
import re
import scraperwiki

scraperwiki.sqlite.attach('brno_councillors_meetings', 'src')
input = scraperwiki.sqlite.select("* from src.swdata order by date")
for rd in input:
    match = re.match(r'(\d{4})-(\d\d)-(\d\d)$', rd['date'])
    if not match:
        raise Exception("invalid date " + rd['date'])

    date = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))    

    base_url = rd['meeting']

    html = scraperwiki.scrape(base_url)
    page = lxml.html.fromstring(html)
    frames = page.xpath("/html/frameset/frame[@name='dokument']")
    if len(frames) == 1:
        data = { 'date': date, 'url': frames[0].get("src") }
        scraperwiki.sqlite.save(unique_keys=['date'], data=data)
    else:
        raise Exception(base_url + " has unexpected frames")

import datetime
import lxml.html
import re
import scraperwiki

scraperwiki.sqlite.attach('brno_councillors_meetings', 'src')
input = scraperwiki.sqlite.select("* from src.swdata order by date")
for rd in input:
    match = re.match(r'(\d{4})-(\d\d)-(\d\d)$', rd['date'])
    if not match:
        raise Exception("invalid date " + rd['date'])

    date = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))    

    base_url = rd['meeting']

    html = scraperwiki.scrape(base_url)
    page = lxml.html.fromstring(html)
    frames = page.xpath("/html/frameset/frame[@name='dokument']")
    if len(frames) == 1:
        data = { 'date': date, 'url': frames[0].get("src") }
        scraperwiki.sqlite.save(unique_keys=['date'], data=data)
    else:
        raise Exception(base_url + " has unexpected frames")

