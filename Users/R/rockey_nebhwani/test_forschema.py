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
    wasPrice = ''
    availability = ''
    image = ''
    imageWithBadge = ''
    promotionName = ''
    brand = ''
    ean = ''
    mpn = ''
    breadcrumb = ''
    productID = ''
    longDescription =''
    accessoriesString = 'Bike Accessories'
    
    title = tree.find('.//h1')

    #title = '"' + title.text + '"'
    #brand = tree.cssselect('[itemprop="brand"]')[0].attrib['content']
    

    for imageSchema in tree.cssselect('[itemprop="image"]'):
        if imageSchema is not None:
            image = imageSchema.attrib['content']

    for imageWithBadgeSchema in tree.cssselect('[id="productImageSmall"]'):
        if imageWithBadgeSchema is not None:
            imageWithBadge = imageWithBadgeSchema.attrib['src']

    #image = tree.cssselect('[itemprop="image"]')[0].attrib['content']
    #availability = tree.cssselect('[itemprop="availability"]')[0].attrib['href']
    #rating = tree.cssselect('[itemprop="ratingValue"]')[0].attrib['content']
    #price = tree.cssselect('[itemprop="price"]')[0].attrib['content']


    #brand = tree.find('.//meta[@itemprop="brand"]')
    #print brand.text
    #ratingElement = tree.cssselect('[itemprop="brand"]')
    

    for brandSchema in tree.cssselect('[itemprop="brand"]'):
        if brandSchema is not None:
            brand = brandSchema.attrib['content']

    for EANSchema in tree.cssselect('[itemprop="gtin13"]'):
        if EANSchema is not None:
            ean = EANSchema.attrib['content']

    for MPNSchema in tree.cssselect('[itemprop="mpn"]'):
        if MPNSchema is not None:
            mpn = MPNSchema.attrib['content']

        for ratingSchema in tree.cssselect('meta[itemprop="ratingValue"]'):
            if ratingSchema is not None:
                rating = ratingSchema.attrib['content']
            print rating

    for priceSchema in tree.cssselect('[itemprop="price"]'):
        if priceSchema is not None:
            price = priceSchema.attrib['content']

    for wasPriceSchema in tree.cssselect('[class="wasPrice"]'):
        if wasPriceSchema is not None:
            wasPrice = wasPriceSchema.text_content

    for availabilitySchema in tree.cssselect('[itemprop="availability"]'):
        if availabilitySchema is not None:
            availability = availabilitySchema.attrib['href']
 
    for promoSchema in tree.cssselect('[class="promotionName clear"]'):
        if promoSchema is not None:
            promotionName = promoSchema.text

    for productID in tree.cssselect('[name="pid"]'):
        if productID is not None:
            productID = productID.attrib['value']

    for breadcrumbSchema in tree.findall('.//ol[@id="navBreadcrumbs"]'):
    #for breadcrumbSchema in tree.findall('.//ol[@id="navBreadcrumbs"]'):
        if breadcrumbSchema is not None:
            breadcrumb = breadcrumbSchema.text_content().strip()

    if accessoriesString in breadcrumb:
       return

    for longDescription in tree.cssselect("div#descriptionsContent"):
        if longDescription is not None:
            longDescription = longDescription.text_content()
    
    url = url.encode('utf-8') + '?cm_vc=BIKEZONE'

    data = {
        'name': title.text if title is not None else '',
        'productID': productID if productID is not None else '',
        'Price': price if price is not None else '',
        'wasPrice': wasPrice if wasPrice is not None else '',
        'Deeplink': url,
        'Picture_link': image if image is not None else '',
        'Picture_link_with_badge': imageWithBadge if imageWithBadge is not None else '',
        'rating': rating if rating is not None else '',
        'brand': brand if brand is not None else '',
        'availability': availability[18:28] if availability is not None else '',
        'promotionName': promotionName if promotionName is not None else '',
        'ean': ean if ean is not None else '',
        'mpn': mpn if mpn is not None else '',
        'breadcrumb' : breadcrumb if breadcrumb is not None else '',
        'longDescription' : longDescription if longDescription is not None else ''
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
#pageurl = 'http://direct.asda.com/on/demandware.store/Sites-ASDA-Site/default/Search-Show?cgid=4025'
pageurl= 'http://direct.asda.com/on/demandware.store/Sites-ASDA-Site/default/Search-Show?q=%22bike%20shop%22&prefn1=catalogCode&prefv1=946-019&showHits&fix'
#pageurl = 'http://direct.asda.com/on/demandware.store/Sites-ASDA-Site/default/Search-Show?q=000969350'
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

