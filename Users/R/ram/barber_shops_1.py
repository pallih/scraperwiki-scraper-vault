# Scrape Barber Shop Details

import scraperwiki
import lxml.html

counter = 1

# Get root node from url
def scrape_content(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

def scrape_shop(src):
    root = scrape_content(src)
    for shop in root.cssselect('div.claim'):
        global counter
        shp = dict()
        shp['id'] = counter
        shp['name'] = shop.cssselect('h2')[0].text_content()
        #shp['phone'] = 'no phone'
        #shp['website'] = 'no website'
        shp['addressRegion'] = 'blank'
        shp['url']= 'blank'
        shp['telephone'] = 'blank'
        shp['streetAddress'] = 'blank'
        shp['addressLocality'] = 'blank'
        shp['postalCode'] = 'blank'
        shp['error'] = 0
        try:
            #shp['phone'] = shop.cssselect('span.phone')[0].text_content()
            #shp['website'] = shop.cssselect('span.ws')[0].text_content()
            for span in shop.cssselect('div.info div:first-child span'):
                shp[span.attrib['itemprop']] = span.text_content()
        except IndexError:
            shp['error'] = 1
        print scraperwiki.sqlite.save(unique_keys=['id'], data=shp)
        counter += 1

src = 'http://www.manta.com/mb_34_B30F1_000/barber_shops'
scrape_shop(src)
