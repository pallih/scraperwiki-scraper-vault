import scraperwiki
import json
import re
import urlparse
import lxml.html
import time

def scrape_laptop(url):
    html = scraperwiki.scrape(url)
    tree = lxml.html.fromstring(html)

    title = tree.find('.//h1')
    price = tree.find('.//span[@id="fk-mprod-our-id"]')
    reviewcount = tree.find('.//span[@itemprop="reviewCount"]')
    rating = ''
    reviewurl = ''
    el = tree.cssselect("div.fk-stars")
    for el in tree.cssselect("div.fk-stars"):

         if el is not None:
            if el.attrib['title'] is not None:

                rating = el.attrib['title']
                rating = rating.replace('stars',' ')
                rating = rating.rstrip()
    
    for r1 in tree.cssselect("div.tmargin5 a"):
        if r1 is not None:
            reviewurl = r1.get('href','')



    data = {
        'title': title.text if title is not None else '',
        'url': url,
        'price': price.text_content() if price is not None else '',
        'rating': rating if rating is not None else '',
        'reviewcount': reviewcount.text_content() if reviewcount is not None else '0',
        'reviewurl': reviewurl if reviewurl is not None else ''
    }
    

    if data['reviewurl'] is not '':
        li = 'http://www.flipkart.com' + data['reviewurl']
        if(int(data['reviewcount']) > 0):
            print int(data['reviewcount'])
            scrape_reviews(li,data)
    print data

    for row in tree.findall('.//table[@class="fk-specs-type2"]//tr'):
        label = row.find('th')
        value = row.find('td')
        if label is not None and value is not None and label.text is not None:
            # Ensure key is simple text. 
            key = re.sub(r'[^a-zA-Z0-9_\- ]+', '-', label.text)

            data[key] = value.text
    print data
    scraperwiki.sqlite.save(unique_keys=["url"], data=data)
    

        
def scrape_reviews(url,data):
    start = 0
    count =int(data['reviewcount'])
    print count
    userreviews=''
    page = 1
    while start <= count:
        reviewdata = scraperwiki.scrape(url + '&start=%d' %start)
        
        tree = lxml.html.fromstring(reviewdata)
        print tree
        page = 1
        rcount = 0
        for review in tree.cssselect('p.bmargin10'):
        
            if review is not None:
                userreviews = userreviews + review.text_content() + '(nextrewviewswatilaptops)'

        data['reviews'] = userreviews
        
        #scraperwiki.sqlite.save(unique_keys=["url"], data=reviewlist)
        start += 10



start = 0
while True:
    data = scraperwiki.scrape('http://www.flipkart.com/all-xbox-360-format-games?response-type=json&inf-start=%d' % start)
    data = json.loads(data)
    if data['count'] <= 0:
        break
    print data['html']
    tree = lxml.html.fromstring(data['html'])
    for el in tree.cssselect("div.fk-product-thumb a"):
        if el is not None:
            url = el.get('href','')
        if not url:
            continue
        parsed_url = urlparse.urlparse(url)
        print parsed_url.path
        scrape_laptop('http://www.flipkart.com' + parsed_url.path)
        start += 20
        time.sleep(5)

