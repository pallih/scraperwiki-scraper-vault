import scraperwiki
import requests
import lxml.html


def scrape_people():

    # Let's start blindly scraping each results page…
    for i in range(1,10):
        r = requests.get('http://airbnb.herokuapp.com/s/Stockholm--Sweden?page=%s' % (i))
        if r.status_code==200:
            dom = lxml.html.fromstring(r.text)

            if len(dom.cssselect('#results')):
                # Great! This page contains people to scrape.
                ads = []
                for listobject in dom.cssselect('.search_result'):
                    ad = {
                        'name': get_element_or_none(listobject, 'a.name'),
                        'price': get_element_or_none(listobject, '.price_data'),
                        'url': 'http://airbnb.herokuapp.com/s/Stockholm--Sweden' + get_element_or_none(listobject, 'a.name', 'href')
                    }
                    print ad['name']
                    ads.append(ad)


                print 'saving page %s' % i
                scraperwiki.sqlite.save(['url'], ads)

            else:
                # Yay! We've reached the end.
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



scrape_people()


