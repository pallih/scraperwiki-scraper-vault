#Cant seem to figure out what im doing wrong build this scraper off of Zarino Zappia hyperisland student scraper "https://scraperwiki.com/scrapers/hyper_island_student_profiles/"
#
#


import scraperwiki
import requests
import lxml.html

def scrape_ads():   
    for i in range(1,10):
        r = requests.get('http://airbnb.herokuapp.com/s/Stockholm--Sweden?page=%s' % i) #doubelcheck %s
        if r.status_code==200: #what does this mean?
            dom = lxml.html.fromstring(r.text)

    
            targetList = dom.cssselect('.search_result')
            if len(targetList):
                # Great! This page contains people to scrape.
                ads = [] #changed from people = []
                for results in targetList: #Hey Daniel suspect the problem is somewhere in this loop.
                    ad = {
                        'name': get_element_or_none(results, 'a.name'),
                        'price': get_element_or_none(results, '.price_data'),
                        'url': get_element_or_none(results, 'a.name', 'href')
                    }
                    print ad['name']

                    # add this person to the list
                    ads.append(ad)

                # we've done all the people on this page… let's save.
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
            return element.text_content()


scrape_ads()
#Cant seem to figure out what im doing wrong build this scraper off of Zarino Zappia hyperisland student scraper "https://scraperwiki.com/scrapers/hyper_island_student_profiles/"
#
#


import scraperwiki
import requests
import lxml.html

def scrape_ads():   
    for i in range(1,10):
        r = requests.get('http://airbnb.herokuapp.com/s/Stockholm--Sweden?page=%s' % i) #doubelcheck %s
        if r.status_code==200: #what does this mean?
            dom = lxml.html.fromstring(r.text)

    
            targetList = dom.cssselect('.search_result')
            if len(targetList):
                # Great! This page contains people to scrape.
                ads = [] #changed from people = []
                for results in targetList: #Hey Daniel suspect the problem is somewhere in this loop.
                    ad = {
                        'name': get_element_or_none(results, 'a.name'),
                        'price': get_element_or_none(results, '.price_data'),
                        'url': get_element_or_none(results, 'a.name', 'href')
                    }
                    print ad['name']

                    # add this person to the list
                    ads.append(ad)

                # we've done all the people on this page… let's save.
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
            return element.text_content()


scrape_ads()
