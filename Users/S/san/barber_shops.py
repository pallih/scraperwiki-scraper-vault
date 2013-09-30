# Scrape Barber Shop Details

import scraperwiki
import lxml.html



# Get root node from url
def scrape_content(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

def scrape_shop(src):
    global id
    root = scrape_content(src)
    print root.text_content()
    for shop in root.cssselect('div.claim'):
        shp = dict()
        shp['name'] = shop.cssselect('h2')[0].text_content()
        shp['phone'] = shop.cssselect('span.phone')[0].text_content()
        shp['website'] = shop.cssselect('span.ws')[0].text_content()
        for span in shop.cssselect('div.info div:first-child span'):
            shp[span.attrib['itemprop']] = span.text_content()
        #print '[' + scraperwiki.sqlite.save(unique_keys=['id'], data=shp) + ']'
        print shp
        id += 1
        break
id = 1
src = 'http://www.manta.com/mb_34_B30F1_000/barber_shops'
scrape_shop(src)
# Scrape Barber Shop Details

import scraperwiki
import lxml.html



# Get root node from url
def scrape_content(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

def scrape_shop(src):
    global id
    root = scrape_content(src)
    print root.text_content()
    for shop in root.cssselect('div.claim'):
        shp = dict()
        shp['name'] = shop.cssselect('h2')[0].text_content()
        shp['phone'] = shop.cssselect('span.phone')[0].text_content()
        shp['website'] = shop.cssselect('span.ws')[0].text_content()
        for span in shop.cssselect('div.info div:first-child span'):
            shp[span.attrib['itemprop']] = span.text_content()
        #print '[' + scraperwiki.sqlite.save(unique_keys=['id'], data=shp) + ']'
        print shp
        id += 1
        break
id = 1
src = 'http://www.manta.com/mb_34_B30F1_000/barber_shops'
scrape_shop(src)
