import scraperwiki
import json
import re
import urlparse
import lxml.html

def scrape_laptop(prdurl):
    html = scraperwiki.scrape(prdurl)
    if html is not None:
        tree = lxml.html.fromstring(html)
        
        title = tree.find('.//span[@id="btAsinTitle"]')
        #price = tree.find('[class="priceLarge"]')
        #if price is not None:
        #    print price.text        
        reviews = tree.find('.//span[@class="crAvgStars"]')
        review = ''
        rating = ''
        reviewurl = ''
        prddetailsurl = ''
        
        if reviews is not None:
            reviewstr = reviews.text_content().replace('See all reviews','#')
            reviewsrating = reviewstr.split('#')
            print reviewsrating
            if len(reviewsrating) > 0:
                rating = reviewsrating [0].rstrip()
                #print rating
                rating = rating.encode('utf-8')
                rating = rating.replace("out of 5 stars","")
                rating = rating.strip()
                print rating
                if len(reviewsrating) > 1:
                    review = reviewsrating [1]
                    #print review
                    review = review.encode('utf-8')               
                    review = review.replace('customer reviews)','')
                    review = review.replace('(','')
                    review = review.strip()
                    print review

        
        for r in tree.cssselect('div[class="bucket"]'):
            if r is not None:
                 #print lxml.html.tostring(r)
                 for s in r.cssselect('a[name="technical_details"]'):
                     if s is not None:
                         #print lxml.html.tostring(s)
                         for t in r.cssselect("div.content a"):
                             if t is not None:
                                 #print lxml.html.tostring(t)
                                 #print t.attrib['href']
                                 prddetailsurl = t.attrib['href']
      
    
        data = {
            'Title': title.text if title is not None else '',
            #'price': price.text if price is not None else '',
            'Rating': rating if rating is not None else '',
            'No of Reviews': review if review is not None else '',
            'URL': prddetailsurl if prddetailsurl is not None else ''
        }
                
  
        if data['URL'] is not '':
            scrape_techdetails(data)
        print data
        scraperwiki.sqlite.save(unique_keys=['URL'], data=data)
        

        
def scrape_techdetails(data):
    #print 'inside techdetails'
    print data['URL']
    if data is not None:
        prdhtml = scraperwiki.scrape(data['URL'])
        if prdhtml is not None:
            tree = lxml.html.fromstring(prdhtml)
            for r in tree.cssselect('div[class="bucket"]'):
                if r is not None:
                    #print lxml.html.tostring(r)
                    for s in r.cssselect('a[name="technical_details"]'):
                        if s is not None:
                            #print lxml.html.tostring(s)
                            #data ['Technical Details'] = r.text_content()
                            #print data ['Technical Details']
                            other = ''
                            for t in r.cssselect("div.content li"):
                                if t is not None:
                                    #print lxml.html.tostring(t) 
                                    textinli = t.text_content()           
                                    print textinli
                                    if textinli.find(":") != -1:
                                        words = textinli.split(":")
                                        key = words[0].strip()
                                        #key = key.replace('(','')
                                        #key = key.replace(')','')
                                        #key = key.replace(',','')
                                        #key = key.replace("'","")
                                        #key = key.strip()
                                        #print key
                                        value = textinli.replace(words[0]+":","").strip()
                                        #print value  
                                        #data[key] = value
                                        if key.upper().find("DISPLAY")!=-1:
                                            data['Display'] = value
                                        #    print data['Display']
                                        elif key.upper().find("CAMERA")!=-1:
                                            data['Camera'] = value
                                        #    print data['Camera']
                                        elif key.upper().find("PROCESSOR SPEED")!=-1:
                                            data['Processor Speed'] = value
                                        #    print data['Processor Speed']                                   
                                        elif key.upper().find("OS")!=-1:
                                            data['OS'] = value
                                        #    print data['OS']
                                        elif key.upper().find("SIZE")!=-1:
                                            data['Size'] = value
                                        #    print data['Size']
                                        elif key.upper().find("WEIGHT")!=-1:
                                            data['Weight'] = value
                                        #    print data['Weight']                                     
                                        elif key.upper().find("NETWORK COMPATIBILITY")!=-1:
                                            data['Network Compatibility'] = value
                                        #    print data['Network Compatibility']
                                        elif key.upper().find("MINIMUM RATED TALK TIME")!=-1:
                                            data['Minimum Rated Talk Time'] = value
                                        #    print data['Minimum Rated Talk Time']
                                        elif key.upper().find("MINIMUM RATED STANDBY TIME")!=-1:
                                            data['Minimum Rated Standby Time'] = value
                                        #    print data['Minimum Rated Standby Time']
                                        elif key.upper().find("NETWORK BAND")!=-1:
                                            data['Network Band'] = value
                                        #    print data['Network Band']
                                        elif key.upper().find("DIMENSIONS")!=-1:
                                            data['Dimensions'] = value
                                        #    print data['Dimensions']
                                        elif key.upper().find("INTERNAL STORAGE CAPACITY")!=-1:
                                            data['Internal Storage Capacity'] = value
                                        #    print data['Internal Storage Capacity']
                                        elif key.upper().find("CPU")!=-1:
                                            data['CPU'] = value
                                        #    print data['CPU']
                                        elif key.upper().find("BATTERY TYPE")!=-1:
                                            data['Battery Type'] = value
                                        #    print data['Battery Type']
                                        else:
                                            if other is not '':
                                                other = other+" # "+textinli
                                            else:
                                                other = textinli
                            data['Other'] = other





start = 0
#pageurl = 'http://www.amazon.com/s/ref=sr_nr_n_0?rh=n%3A2335752011%2Cn%3A%212335753011%2Cn%3A2407747011&bbn=2335753011&ie=UTF8&qid=1368616362&rnid=2335753011'
pageurl = 'http://www.amazon.com/s/ref=sr_nr_n_1?rh=n%3A2335752011%2Cn%3A%212335753011%2Cn%3A2407749011&bbn=2335753011&ie=UTF8&qid=1368953026&rnid=2335753011'

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

import scraperwiki
import json
import re
import urlparse
import lxml.html

def scrape_laptop(prdurl):
    html = scraperwiki.scrape(prdurl)
    if html is not None:
        tree = lxml.html.fromstring(html)
        
        title = tree.find('.//span[@id="btAsinTitle"]')
        #price = tree.find('[class="priceLarge"]')
        #if price is not None:
        #    print price.text        
        reviews = tree.find('.//span[@class="crAvgStars"]')
        review = ''
        rating = ''
        reviewurl = ''
        prddetailsurl = ''
        
        if reviews is not None:
            reviewstr = reviews.text_content().replace('See all reviews','#')
            reviewsrating = reviewstr.split('#')
            print reviewsrating
            if len(reviewsrating) > 0:
                rating = reviewsrating [0].rstrip()
                #print rating
                rating = rating.encode('utf-8')
                rating = rating.replace("out of 5 stars","")
                rating = rating.strip()
                print rating
                if len(reviewsrating) > 1:
                    review = reviewsrating [1]
                    #print review
                    review = review.encode('utf-8')               
                    review = review.replace('customer reviews)','')
                    review = review.replace('(','')
                    review = review.strip()
                    print review

        
        for r in tree.cssselect('div[class="bucket"]'):
            if r is not None:
                 #print lxml.html.tostring(r)
                 for s in r.cssselect('a[name="technical_details"]'):
                     if s is not None:
                         #print lxml.html.tostring(s)
                         for t in r.cssselect("div.content a"):
                             if t is not None:
                                 #print lxml.html.tostring(t)
                                 #print t.attrib['href']
                                 prddetailsurl = t.attrib['href']
      
    
        data = {
            'Title': title.text if title is not None else '',
            #'price': price.text if price is not None else '',
            'Rating': rating if rating is not None else '',
            'No of Reviews': review if review is not None else '',
            'URL': prddetailsurl if prddetailsurl is not None else ''
        }
                
  
        if data['URL'] is not '':
            scrape_techdetails(data)
        print data
        scraperwiki.sqlite.save(unique_keys=['URL'], data=data)
        

        
def scrape_techdetails(data):
    #print 'inside techdetails'
    print data['URL']
    if data is not None:
        prdhtml = scraperwiki.scrape(data['URL'])
        if prdhtml is not None:
            tree = lxml.html.fromstring(prdhtml)
            for r in tree.cssselect('div[class="bucket"]'):
                if r is not None:
                    #print lxml.html.tostring(r)
                    for s in r.cssselect('a[name="technical_details"]'):
                        if s is not None:
                            #print lxml.html.tostring(s)
                            #data ['Technical Details'] = r.text_content()
                            #print data ['Technical Details']
                            other = ''
                            for t in r.cssselect("div.content li"):
                                if t is not None:
                                    #print lxml.html.tostring(t) 
                                    textinli = t.text_content()           
                                    print textinli
                                    if textinli.find(":") != -1:
                                        words = textinli.split(":")
                                        key = words[0].strip()
                                        #key = key.replace('(','')
                                        #key = key.replace(')','')
                                        #key = key.replace(',','')
                                        #key = key.replace("'","")
                                        #key = key.strip()
                                        #print key
                                        value = textinli.replace(words[0]+":","").strip()
                                        #print value  
                                        #data[key] = value
                                        if key.upper().find("DISPLAY")!=-1:
                                            data['Display'] = value
                                        #    print data['Display']
                                        elif key.upper().find("CAMERA")!=-1:
                                            data['Camera'] = value
                                        #    print data['Camera']
                                        elif key.upper().find("PROCESSOR SPEED")!=-1:
                                            data['Processor Speed'] = value
                                        #    print data['Processor Speed']                                   
                                        elif key.upper().find("OS")!=-1:
                                            data['OS'] = value
                                        #    print data['OS']
                                        elif key.upper().find("SIZE")!=-1:
                                            data['Size'] = value
                                        #    print data['Size']
                                        elif key.upper().find("WEIGHT")!=-1:
                                            data['Weight'] = value
                                        #    print data['Weight']                                     
                                        elif key.upper().find("NETWORK COMPATIBILITY")!=-1:
                                            data['Network Compatibility'] = value
                                        #    print data['Network Compatibility']
                                        elif key.upper().find("MINIMUM RATED TALK TIME")!=-1:
                                            data['Minimum Rated Talk Time'] = value
                                        #    print data['Minimum Rated Talk Time']
                                        elif key.upper().find("MINIMUM RATED STANDBY TIME")!=-1:
                                            data['Minimum Rated Standby Time'] = value
                                        #    print data['Minimum Rated Standby Time']
                                        elif key.upper().find("NETWORK BAND")!=-1:
                                            data['Network Band'] = value
                                        #    print data['Network Band']
                                        elif key.upper().find("DIMENSIONS")!=-1:
                                            data['Dimensions'] = value
                                        #    print data['Dimensions']
                                        elif key.upper().find("INTERNAL STORAGE CAPACITY")!=-1:
                                            data['Internal Storage Capacity'] = value
                                        #    print data['Internal Storage Capacity']
                                        elif key.upper().find("CPU")!=-1:
                                            data['CPU'] = value
                                        #    print data['CPU']
                                        elif key.upper().find("BATTERY TYPE")!=-1:
                                            data['Battery Type'] = value
                                        #    print data['Battery Type']
                                        else:
                                            if other is not '':
                                                other = other+" # "+textinli
                                            else:
                                                other = textinli
                            data['Other'] = other





start = 0
#pageurl = 'http://www.amazon.com/s/ref=sr_nr_n_0?rh=n%3A2335752011%2Cn%3A%212335753011%2Cn%3A2407747011&bbn=2335753011&ie=UTF8&qid=1368616362&rnid=2335753011'
pageurl = 'http://www.amazon.com/s/ref=sr_nr_n_1?rh=n%3A2335752011%2Cn%3A%212335753011%2Cn%3A2407749011&bbn=2335753011&ie=UTF8&qid=1368953026&rnid=2335753011'

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

