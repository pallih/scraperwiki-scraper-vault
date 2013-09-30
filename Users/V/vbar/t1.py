import datetime
import lxml.html
import scraperwiki

def parse_date(s):
    d, m, y = (int(x) for x in s.split('.'))
    return datetime.date(y, m, d)

offs = 0
cnt = True
id = 0
while cnt:
    page_url = "http://ud.praha4.cz/ost/ud/ud/brow.php?pagepos=" + str(offs) + "&SHOW2MAP_ALL=0&ORDER_BY=status_doc+ASC%2Cdate_start+DESC%2C+date_end+DESC%2C+label+ASC"
    raw_html = scraperwiki.scrape(page_url)
    page = lxml.html.fromstring(raw_html)

    cnt = False
    for tr in page.cssselect("table tr"):
        tds = tr.cssselect("td")
        if not tds or len(tds) != 7:
            continue

        cnt = True
        id += 1        
        data = { 'id' : id,
            'name': tds[0].text_content(),
            'type': tds[1].text_content(),
            'up_date': parse_date(tds[2].text_content()),
            'down_date': parse_date(tds[3].text_content()),
            'desc': tds[4].text_content(),
            'addr': tds[5].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

    offs += 25

import datetime
import lxml.html
import scraperwiki

def parse_date(s):
    d, m, y = (int(x) for x in s.split('.'))
    return datetime.date(y, m, d)

offs = 0
cnt = True
id = 0
while cnt:
    page_url = "http://ud.praha4.cz/ost/ud/ud/brow.php?pagepos=" + str(offs) + "&SHOW2MAP_ALL=0&ORDER_BY=status_doc+ASC%2Cdate_start+DESC%2C+date_end+DESC%2C+label+ASC"
    raw_html = scraperwiki.scrape(page_url)
    page = lxml.html.fromstring(raw_html)

    cnt = False
    for tr in page.cssselect("table tr"):
        tds = tr.cssselect("td")
        if not tds or len(tds) != 7:
            continue

        cnt = True
        id += 1        
        data = { 'id' : id,
            'name': tds[0].text_content(),
            'type': tds[1].text_content(),
            'up_date': parse_date(tds[2].text_content()),
            'down_date': parse_date(tds[3].text_content()),
            'desc': tds[4].text_content(),
            'addr': tds[5].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

    offs += 25

