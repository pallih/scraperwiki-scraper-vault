# A scraper to collect words with the selected keyword (find)
#not working atm.


import scraperwiki
import requests
import lxml.html

def scrape_ads():
    find = "test"
    r = requests.get('http://mashable.com/tech/') #doubelcheck %s
    if r.status_code==200: #what does this mean?
        dom = lxml.html.fromstring(r.text)

        targetList = dom.cssselect('h1.article-title')
        print str(targetList)
        if len(targetList):
            print "target list found"
            # Great! This page contains articles to scrape.
            articles = []
            for result in targetList:
                if find in get_element_or_none(results, 'a'):
                    article = {
                    'titel': get_element_or_none(results, 'a'),
                    'url': get_element_or_none(results, 'a', 'href')
                    }
                    articles.append(article)
                    print article['name']
                else:
                    print "not a match"

            # we've done all the articles on this page… let's save.
            print 'saving page %s' % i
            scraperwiki.sqlite.save(['url'], article)
        else:
            print "target list not found"


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
