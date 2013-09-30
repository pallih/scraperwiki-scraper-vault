import scraperwiki
import lxml.html
import uuid
from datetime import datetime

# Blank Python

base_url = "http://www.dispostable.com"

def run_scraper():
    html = scraperwiki.scrape(base_url + '/inbox/filmbuff/')
    page = lxml.html.fromstring(html)
    trs = page.cssselect('table#messages tbody tr')
    for tr in trs:
        sender = tr.cssselect('td.c1')[0].text_content()
        subject = tr.cssselect('td.c2')[0].text_content()
        date = tr.cssselect('td.c3')[0].text_content()
        link = base_url + tr.cssselect('td.c2 a')[0].attrib['href']
        print link

    data = {
        "link": link,
        "sender": sender,
        "title": subject,
        "description": subject,
        "guid": link + "&uuid=" + str(uuid.uuid1()),
        "pubDate": datetime.strptime(date, '%d %b %Y, %H:%M'),
    }
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)        

run_scraper()
import scraperwiki
import lxml.html
import uuid
from datetime import datetime

# Blank Python

base_url = "http://www.dispostable.com"

def run_scraper():
    html = scraperwiki.scrape(base_url + '/inbox/filmbuff/')
    page = lxml.html.fromstring(html)
    trs = page.cssselect('table#messages tbody tr')
    for tr in trs:
        sender = tr.cssselect('td.c1')[0].text_content()
        subject = tr.cssselect('td.c2')[0].text_content()
        date = tr.cssselect('td.c3')[0].text_content()
        link = base_url + tr.cssselect('td.c2 a')[0].attrib['href']
        print link

    data = {
        "link": link,
        "sender": sender,
        "title": subject,
        "description": subject,
        "guid": link + "&uuid=" + str(uuid.uuid1()),
        "pubDate": datetime.strptime(date, '%d %b %Y, %H:%M'),
    }
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)        

run_scraper()
