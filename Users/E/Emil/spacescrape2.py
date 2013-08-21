#Cant seem to figure out what im doing wrong build this scraper off of Zarino Zappia hyperisland student scraper "https://scraperwiki.com/scrapers/hyper_island_student_profiles/"
#
#


import scraperwiki
import requests
import lxml.html

def scrape_ads():   
    for i in range(1,10):
        # r = requests.get('https://www.airbnb.co.uk/s/Stockholm--Sweden?page=%s' % i, verify=False)
        r = requests.get('http://airbnb.herokuapp.com/s/Stockholm--Sweden?page=%s' % i) #doubelcheck %s
        if r.status_code==200: #what does this mean?i
            dom = lxml.html.fromstring(r.text)

    
            targetList = dom.cssselect('.search_result')
            if len(targetList):
                # Great! This page contains ads to scrape.
                ads = []
                for results in targetList:
                    ad = {
                        'name': get_element_or_none(results, 'a.name'),
                        'price': get_element_or_none(results, '.price_data'),
                        'url': get_element_or_none(results, 'a.name', 'href'),
                        'reviewCount': get_element_or_none(results, '.reviews-bubble')
                    }
                    print ad['name']
                    print ad['url']
                     
                    # Why stop there? Let's scrape more!!
                    # Using the practice url for rooms.
                    # r2 = requests.get(ad['url'])
                    r2 = requests.get("http://airbnb.herokuapp.com/rooms/123456")
                    dom2 = lxml.html.fromstring(r2.text)
                    
                    description = dom2.cssselect('#description_details li.clearfix')
                    for detail in description:
                        key = get_element_or_none(detail, 'span.property').strip(':')
                        value = get_element_or_none(detail, 'span.value')
                        ad[key] = value
                    
                    #Lets get the overall rating for the ad.
                    #first we get the overall rating.
                    value = get_overall_star(dom2)
                    ad['overall rating'] = value

                    #almost forgot the adress.
                    ad['address'] = get_element_or_none(dom2,'#display_address')

                    


                    #lets get all the specific ratings as well.
                    ratingList = dom2.cssselect('#review_stats li')
                    for rating in ratingList:
                        key = get_element_or_none(rating, '.attribute')+' rating'
                        value = get_specific_star(rating)
                        ad[key] = value
                    
                    #whah i cant stop coding lets get the number of images in the gallery as well.
                    imageCountValue = str(len(dom2.cssselect('.galleria-image'))-1)
                    ad['image count'] = imageCountValue
                        
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
    for i in range (0,10):
        if context.cssselect('#guest_satisfaction .star_%s' % i):
            return str(i)
        else:
            continue

def get_specific_star(context):
    for i in range (0,10):
        if context.cssselect('.hosting-star-rating .star_%s' % i):
            return str(i)
        else:
            continue



scrape_ads()