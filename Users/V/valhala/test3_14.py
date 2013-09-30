import scraperwiki
import lxml.html
from urllib2 import HTTPError

def scrape_table(root):
    root = lxml.html.fromstring(html)
    data = []
    for tr in root.cssselect("div.well tr"):
        tds = tr.cssselect("td")
        data.append({
            'Min Sale Offer': tds[4].text_content(), 
            'Sale volume': tds[4].get('title'), 
            'Max Buy Offer': tds[5].text_content(), 
            'Buy volume': tds[5].get('title'), 
            'item' : tds[0].text_content(), 
            'margin' : tds[6].text_content(), 
            'level' : tds[1].text_content(), 
            'Rarity' : tds[2].text_content()
        })
    scraperwiki.sqlite.save(['item'], data)
    
url = 'http://www.gw2spidy.com/type/%d/-1/%d?sort_name=asc'
for site in range(0,21):
    try:
        html = scraperwiki.scrape( url % (site, 999999999) )
    except HTTPError:
        continue
    dom = lxml.html.fromstring(html)
    max_page = dom.cssselect('div.pagination')[0].cssselect('li.active a')[0].text
    for page in range(1, int(max_page) + 1):
        html = scraperwiki.scrape(url % (site, page))
        scrape_table(html)



import scraperwiki
import lxml.html
from urllib2 import HTTPError

def scrape_table(root):
    root = lxml.html.fromstring(html)
    data = []
    for tr in root.cssselect("div.well tr"):
        tds = tr.cssselect("td")
        data.append({
            'Min Sale Offer': tds[4].text_content(), 
            'Sale volume': tds[4].get('title'), 
            'Max Buy Offer': tds[5].text_content(), 
            'Buy volume': tds[5].get('title'), 
            'item' : tds[0].text_content(), 
            'margin' : tds[6].text_content(), 
            'level' : tds[1].text_content(), 
            'Rarity' : tds[2].text_content()
        })
    scraperwiki.sqlite.save(['item'], data)
    
url = 'http://www.gw2spidy.com/type/%d/-1/%d?sort_name=asc'
for site in range(0,21):
    try:
        html = scraperwiki.scrape( url % (site, 999999999) )
    except HTTPError:
        continue
    dom = lxml.html.fromstring(html)
    max_page = dom.cssselect('div.pagination')[0].cssselect('li.active a')[0].text
    for page in range(1, int(max_page) + 1):
        html = scraperwiki.scrape(url % (site, page))
        scrape_table(html)



