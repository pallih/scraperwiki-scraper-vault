#The data collected here is for educational purposes only. It will only be used for a class research project. All data belongs to airbnb.
#


import scraperwiki
import requests
import lxml.html

def scrape_ads():   
    for i in range(1,50):
        r = requests.get('https://www.airbnb.co.uk/s/Stockholm--Sweden?page=%s' % i, verify=False)
        if r.status_code==200:
            dom = lxml.html.fromstring(r.text)

    
            targetList = dom.cssselect('.search_result')
            if len(targetList):
                # Great! This page contains ads to scrape.
                ads = []
                for results in targetList:
                    ad = {
                        'name': get_element_or_none(results, 'a.name').replace(',',''),
                        'url': get_element_or_none(results, 'a.name', 'href')#,
                        #'reviewCount': get_element_or_none(results, '.reviews-bubble')
                    }
                    print ad['name']
                     
                    # Why stop there? Let's scrape more!!
                    # Using the practice url for rooms.
                    print 'https://www.airbnb.co.uk'+ad['url']
                    r2 = requests.get('https://www.airbnb.co.uk'+ad['url'], verify=False)
                    dom2 = lxml.html.fromstring(r2.text)
    
                    #lets get the price/per night from inside the ad instead.
                    ad['price per night'] = get_element_or_none(dom2, 'h2#price_amount')
                    print ad['price per night']

                    description = dom2.cssselect('#description_details li.clearfix')
                    for detail in description:
                        key = get_element_or_none(detail, 'span.property').strip(':')
                        value = get_element_or_none(detail, 'span.value').replace(',','')
                        ad[key] = value
                    
                    #Lets get the overall rating for the ad.
                    #first we get the overall rating.
                    value = get_overall_star(dom2)
                    ad['overall rating'] = value

                    #almost forgot the adress.
                    ad['address'] = get_element_or_none(dom2,'#display_address').replace(',','')
                    ad['review count'] = get_element_or_none(dom2,'#this_hosting_reviews_link span')
                    print ad['review count']
                    


                    #lets get all the specific ratings as well.
                    ratingList = dom2.cssselect('#review_stats li')
                    for rating in ratingList:
                        key = get_element_or_none(rating, '.attribute')+' rating'
                        value = get_specific_star(rating)
                        ad[key] = value
                    
                    #whah i cant stop coding lets get the number of images in the gallery as well.
                    imageCountValue = str(len(dom2.cssselect('#galleria_container img'))-1) #the .cssselect() on this line no longer returns a list of images, why?
                    ad['image count'] = imageCountValue
                    print len(dom2.cssselect('#galleria_container img'))
            
                        
                    # add this person to the list
                    ads.append(ad)

                # we've done all the ads on this page… let's save.
                print 'saving page %s' % i
                scraperwiki.sqlite.save(['url'], ads)
            else:
                break


# A handy function to get text or attributes out of HTML elements
def get_element_or_none(context, css, attribute=None):
    try:
        element = context.cssselect(css)[0]
    except:
        return None
    else:
        if attribute:
            return element.get(attribute)
        else:
            return element.text_content().strip()

def get_overall_star(context):
    for i in range (0,11):
        if context.cssselect('#guest_satisfaction .star_%s' % i):
            return str(i)
        else:
            continue

def get_specific_star(context):
    for i in range (0,11):
        if context.cssselect('.hosting-star-rating .star_%s' % i):
            return str(i)
        else:
            continue



scrape_ads()#The data collected here is for educational purposes only. It will only be used for a class research project. All data belongs to airbnb.
#


import scraperwiki
import requests
import lxml.html

def scrape_ads():   
    for i in range(1,50):
        r = requests.get('https://www.airbnb.co.uk/s/Stockholm--Sweden?page=%s' % i, verify=False)
        if r.status_code==200:
            dom = lxml.html.fromstring(r.text)

    
            targetList = dom.cssselect('.search_result')
            if len(targetList):
                # Great! This page contains ads to scrape.
                ads = []
                for results in targetList:
                    ad = {
                        'name': get_element_or_none(results, 'a.name').replace(',',''),
                        'url': get_element_or_none(results, 'a.name', 'href')#,
                        #'reviewCount': get_element_or_none(results, '.reviews-bubble')
                    }
                    print ad['name']
                     
                    # Why stop there? Let's scrape more!!
                    # Using the practice url for rooms.
                    print 'https://www.airbnb.co.uk'+ad['url']
                    r2 = requests.get('https://www.airbnb.co.uk'+ad['url'], verify=False)
                    dom2 = lxml.html.fromstring(r2.text)
    
                    #lets get the price/per night from inside the ad instead.
                    ad['price per night'] = get_element_or_none(dom2, 'h2#price_amount')
                    print ad['price per night']

                    description = dom2.cssselect('#description_details li.clearfix')
                    for detail in description:
                        key = get_element_or_none(detail, 'span.property').strip(':')
                        value = get_element_or_none(detail, 'span.value').replace(',','')
                        ad[key] = value
                    
                    #Lets get the overall rating for the ad.
                    #first we get the overall rating.
                    value = get_overall_star(dom2)
                    ad['overall rating'] = value

                    #almost forgot the adress.
                    ad['address'] = get_element_or_none(dom2,'#display_address').replace(',','')
                    ad['review count'] = get_element_or_none(dom2,'#this_hosting_reviews_link span')
                    print ad['review count']
                    


                    #lets get all the specific ratings as well.
                    ratingList = dom2.cssselect('#review_stats li')
                    for rating in ratingList:
                        key = get_element_or_none(rating, '.attribute')+' rating'
                        value = get_specific_star(rating)
                        ad[key] = value
                    
                    #whah i cant stop coding lets get the number of images in the gallery as well.
                    imageCountValue = str(len(dom2.cssselect('#galleria_container img'))-1) #the .cssselect() on this line no longer returns a list of images, why?
                    ad['image count'] = imageCountValue
                    print len(dom2.cssselect('#galleria_container img'))
            
                        
                    # add this person to the list
                    ads.append(ad)

                # we've done all the ads on this page… let's save.
                print 'saving page %s' % i
                scraperwiki.sqlite.save(['url'], ads)
            else:
                break


# A handy function to get text or attributes out of HTML elements
def get_element_or_none(context, css, attribute=None):
    try:
        element = context.cssselect(css)[0]
    except:
        return None
    else:
        if attribute:
            return element.get(attribute)
        else:
            return element.text_content().strip()

def get_overall_star(context):
    for i in range (0,11):
        if context.cssselect('#guest_satisfaction .star_%s' % i):
            return str(i)
        else:
            continue

def get_specific_star(context):
    for i in range (0,11):
        if context.cssselect('.hosting-star-rating .star_%s' % i):
            return str(i)
        else:
            continue



scrape_ads()