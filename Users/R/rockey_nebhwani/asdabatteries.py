import scraperwiki
import json
import re
import urlparse
import lxml.html

try:
    scraperwiki.sqlite.execute("""
        create table swdata
        (
        Deeplink
        )
    """)
except:
    print "Table probably already exists."


def scrape_products(url):
    html = scraperwiki.scrape(url)
    tree = lxml.html.fromstring(html)

    review = ''
    rating = ''
    price = ''
    availability = ''
    image = ''
    promotionName = ''
    brand = ''
    
    title = tree.find('.//h1')
    #brand = tree.cssselect('[itemprop="brand"]')[0].attrib['content']
    
    image = tree.cssselect('[itemprop="image"]')[0].attrib['content']
    #availability = tree.cssselect('[itemprop="availability"]')[0].attrib['href']
    #rating = tree.cssselect('[itemprop="ratingValue"]')[0].attrib['content']
    #price = tree.cssselect('[itemprop="price"]')[0].attrib['content']


    #brand = tree.find('.//meta[@itemprop="brand"]')
    #print brand.text
    #ratingElement = tree.cssselect('[itemprop="brand"]')
    

    for brandSchema in tree.cssselect('[itemprop="brand"]'):
        if brandSchema is not None:
            brand = brandSchema.attrib['content']

    for ratingSchema in tree.cssselect('[itemprop="ratingValue"]'):
        if ratingSchema is not None:
            rating = ratingSchema.attrib['content']

    for priceSchema in tree.cssselect('[itemprop="price"]'):
        if priceSchema is not None:
            price = priceSchema.attrib['content']

    for availabilitySchema in tree.cssselect('[itemprop="availability"]'):
        if availabilitySchema is not None:
            availability = availabilitySchema.attrib['href']
 

    for promoSchema in tree.cssselect('[class="promotionName clear"]'):
        if promoSchema is not None:
            promotionName = promoSchema.text
    
    url = url.encode('utf-8')


    data = {
        'name': title.text if title is not None else '',
        'Price': price if price is not None else '',
        'Deeplink': url,
        'Picture_link': image if image is not None else '',
        'rating': rating if rating is not None else '',
        'brand': brand if brand is not None else '',
        'availability': availability[18:28] if availability is not None else '',
        'promotionName': promotionName if promotionName is not None else ''
    }


    for row in tree.findall('.//table[@id="fullSpec"]//tr'):
            
            tds= row.cssselect("td")
            if (len(tds) == 2):
                #print "here"
                label = tds[0].text
                value = ''
                if label is not None:
                    label = label.encode('utf-8')
                    label = label.replace(':','')
                    value = tds[1].text_content()
                    if value is not '':
                        value = value.encode('utf-8')
                        value = value.split('&')[0].rstrip()
                    key = re.sub(r'[^a-zA-Z0-9_\- ]+', '-', label)
                    data[key] = value.strip('\n')
    print url
    scraperwiki.sqlite.save(unique_keys=["Deeplink"], data=data)
    

start = 0
#pageurl = 'http://www.amazon.com/s/ref=sr_nr_n_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A565108&bbn=541966&ie=UTF8&qid=1351233157&rnid=541966'
pageurl = 'http://direct.asda.com/on/demandware.store/Sites-ASDA-Site/default/Search-Show?q=asda&cgid=470'
while (start >= 0):

    html= scraperwiki.scrape(pageurl)
    tree = lxml.html.fromstring(html)

    for el in tree.cssselect('div.prodMiniTop a'):
        if el is not None:
            url = el.attrib['href']
            if not url:
                continue
            #parsed_url = urlparse.urlparse(url)
            scrape_products(url)
    pagnext = tree.find('.//li[@class="next"]//a')
    if pagnext is not None:
        pageurl = pagnext.get('href','')
        print pageurl
        start += 1
    else:
        start = -1  

