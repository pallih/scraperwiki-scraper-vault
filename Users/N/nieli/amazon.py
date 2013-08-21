import scraperwiki
import json
import re
import urlparse
import lxml.html

def scrape_laptop(url):
    html = scraperwiki.scrape(url)
    tree = lxml.html.fromstring(html)
    
    title = tree.find('.//span[@id="btAsinTitle"]')
    
    reviews = tree.find('.//span[@class="crAvgStars"]')
    review = ''
    rating = ''
    reviewurl = ''
    prddescurl = ''
    prddetailsurl = ''
    
    if reviews is not None:
        reviewstr = reviews.text_content().replace('See all reviews','#')
        reviewsrating = reviewstr.split('#')
        print reviewsrating

        if len(reviewsrating) > 0:
            rating = reviewsrating [0].rstrip()
            rating = rating.encode('utf-8')
            print rating
            #rating = rating.replace(u'\xa0',u'')
            if len(reviewsrating) > 1:
                review = reviewsrating [1]
                print review
                review = review.encode('utf-8')                
                review = review.strip(')')

                review = review.replace('(','')

                print review
    
    for r1 in tree.cssselect("div#technical-data_feature_div a"):
        if r1 is not None:
            prddescurl = r1.get('href','')
    if prddescurl == '':
        prddetailsurl  = url + '#productDetails'


    #price
    
    


    data = {
        'title': title.text if title is not None else '',
        'url': url,
        'rating': rating if rating is not None else '',
        'review': review if review is not None else '',
        'prdurl': prddescurl if prddescurl is not None else '',
        'prddetailsurl ': prddetailsurl if prddetailsurl is not None else ''

    }
    for row in tree.findall('.//table[@class="product"]//tr'):


            tds= row.cssselect("td")
            if (len(tds) == 2):

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
                    data[key] = value

                
            #print value.text
            #if label is not None and value is not None and label.text is not None:
                # Ensure key is simple text.
               # key = re.sub(r'[^a-zA-Z0-9_\- ]+', '-', label.text)
    
                #data[key] = value.text


    
    if data['prdurl'] is not '':
        scrape_techdetails(data)

    if data['prddetailsurl '] is not '':
        scrape_prddetails(data)
    url = url.encode('utf-8')
    print url
    print data
    scraperwiki.sqlite.save(unique_keys=["url"], data=data)
    

        
def scrape_techdetails(data):
    techdetails = ''
    prdhtml = scraperwiki.scrape(data['prdurl'])
    tree = lxml.html.fromstring(prdhtml)
    for r1 in tree.cssselect("div.content"):
        if r1 is not None:
            techdetails = r1.text_content() 
            techdetails = techdetails.encode('utf-8')         
    data['product_specifications'] = techdetails

def scrape_prddetails(data):
    prddetails = ''
    prdhtml = scraperwiki.scrape(data['prddetailsurl '])
    tree = lxml.html.fromstring(prdhtml)
    for r1 in tree.cssselect("div.pdTab table"):
        if r1 is not None:
            tbody = r1.find('tbody')
            for row in tbody.findall('tr'):
                label = row.find('td[@class="label"]')
                value = row.find('td[@class="value"]')   
                if label is not None and value is not None and label.text is not None:
                    # Ensure key is simple text. 
                    key = re.sub(r'[^a-zA-Z0-9_\- ]+', '-', label.text)
    
                    data[key] = value.text                           
                 
                  
        
        #reviewlist = {
        #'url':   url,                
        #'reviews': userreviews if not None else ''}
        #print reviewlist

        #data[reviewdesc] = userreviews
        #print userreviews

        #scraperwiki.sqlite.save(unique_keys=["url"], data=reviewlist)
        #start += 10


start = 0
#pageurl = 'http://www.amazon.com/s/ref=sr_nr_n_1?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A565108&bbn=541966&ie=UTF8&qid=1351233157&rnid=541966'
pageurl = 'http://www.amazon.com/s?ie=UTF8&page=4&rh=n%3A565108'
while (start >= 0):

    html= scraperwiki.scrape(pageurl)
    tree = lxml.html.fromstring(html)
  
    for el in tree.cssselect('div.productTitle a'):
        if el is not None:
            url = el.attrib['href']
            if not url:
                continue
            #parsed_url = urlparse.urlparse(url)
            print url
            scrape_laptop(url)
    pagnext = tree.find('.//span[@class="pagnNext"]//a')
    if pagnext is not None:
        pageurl = pagnext.get('href','')
        print pageurl
        start += 1
    else:
        start = -1  

