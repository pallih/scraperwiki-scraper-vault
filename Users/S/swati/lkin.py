import scraperwiki
import json
import re
import urlparse
import lxml.html
import csv

def scrape_laptop(url):
    html = scraperwiki.scrape(url)
    if html is not None:
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
    if data is not None:
        prdhtml = scraperwiki.scrape(data['prdurl'])
        if prdhtml is not None:
            tree = lxml.html.fromstring(prdhtml)
            for r1 in tree.cssselect("div.content"):
                if r1 is not None:
                    techdetails = r1.text_content() 
                    techdetails = techdetails.encode('utf-8')         
            data['product_specifications'] = techdetails

def scrape_prddetails(data):
    if data is not None:
        prddetails = ''
        prdhtml = scraperwiki.scrape(data['prddetailsurl '])
        if prdhtml is not None:
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

urllist =['http://in.linkedin.com/pub/navin-agrawal/1/374/897',
          'http://in.linkedin.com/pub/ca-mukesh-p-mody/24/a26/6b5']

i=0

while (i < len(urllist)):
    
    pageurl = urllist[i]

    html= scraperwiki.scrape(pageurl)
    tree = lxml.html.fromstring(html)
    print html
    summary_current = ''
    summary_past = ''
    summary_education = ''
    current_title = ''
    current_company = ''
    current_period = ''
    current_details = ''
  
    

    for el in tree.cssselect('dd.summary-current ul '):
        if el is not None:
           summary_current = el.text_content()
      
    for el in tree.cssselect('dd.summary-past ul '):
        if el is not None:
            summary_past= el.text_content()
    for el in tree.cssselect('dd.summary-education ul '):
        if el is not None:
            sumamry_education = el.text_content()
    for el in tree.cssselect('div.summary-current'):
        if el is not None:
            print lxml.html.tostring(el)
            for cl in el.cssselect('div.postitle'):
                if cl is not None:
                    title = cl.find('.//span[@class="title"]') 
                    print title.text 
                    current_title = title.text
                    company = cl.find('.//span[@class="org summary"]')
                    if company is not None:
                        print company.text
                        current_company = company.text
            for cl in el.find('.//p[@class="period"]'):
                if cl is not None:
                    print cl.text
                    current_period = cl.text
            for cl in el.cssselect('p.current-position'):
                print cl
                if cl is not None:
                    print cl.text_content() 
                    current_details = cl.text_content() 
    data_current ={
        'summary-current':summary_current if summary_current is not None else '',
        'summary-past': summary_past if summary_past is not None else '',
        'summary-education': summary_education if summary_education is not None else '',
        'current-title': current_title if current_title is not None else '',
        'current-company':current_company if current_company is not None else '',
        'curren-period':current_period if current_period is not None else '',
        'current-details':current_details if current_details is not None else ''
    }
    data_history=[]

    for el in tree.cssselect('div.summary-past'):
        data_past=[]
        role=''
        company_name=''
        period = ''
        details=''
        if el is not None:
            print lxml.html.tostring(el)
            for cl in el.cssselect('div.postitle'):
                if cl is not None:
                    title = cl.find('.//span[@class="title"]') 
                    print title.text 
                    role= title.text
                    company = cl.find('.//span[@class="org summary"]')
                    if company is not None:
                        print company.text
                        company_name = company.text
            for cl in el.find('.//p[@class="period"]'):
                if cl is not None:
                    print cl.text
                    period = cl.text
            for cl in el.cssselect('p.past-position'):
                print cl
                if cl is not None:
                    details = cl.text_content()
            data_past={
                'title': role if role is not None else '',
                'company': company_name if company_name is not None else '',
                'period': period if period is not None else '',
                'details':details if details is not None else ''}
            data_history.append(data_past)
           
    data = {'url': pageurl if pageurl  is not None else '',
            'current-data': data_current if data_current is not None else '',
            'past-history': data_history if data_history  is not None else ''}  
    scraperwiki.sqlite.save(unique_keys=["url"], data=data)       
    i += 1
   

