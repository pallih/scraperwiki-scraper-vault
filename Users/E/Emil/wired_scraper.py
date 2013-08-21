# A scraper to collect words with the selected keyword (find)
#not working atm.


import scraperwiki
import requests
import lxml.html

def scrape_wired(keyword):
    for i in range(2007, 2012):
        for j in range(1, 12):
            r = requests.get('http://www.wired.com/business/%s/%s/' % (i,j))

            if r.status_code == 200:
                dom = lxml.html.fromstring(r.text)
    
                targetList = dom.cssselect('h2 a')
                print str(targetList)
                if len(targetList):
                    print "target list found"
                    # Great! This page contains articles to scrape.
                    articles = []
                    for result in targetList:
                        if keyword in result.text_content():
                            article = {
                            'title': result.text_content(),
                            'url': result.get("href"),
                            'year': str(i),
                            'month': str(j),
                            'keyword': keyword,
                            'source': "wired"
                            }
                            articles.append(article)
                            print article['title']
        
                    # we've done all the articles on this page… let's save.
                    if len(articles):
                        print 'saving page %s' % i
                        scraperwiki.sqlite.save(['url'], article)
                else:
                    print "target list not found"

def scrape_techCrunch(keyword):   
    for i in range(1,1000):
        r = requests.get('http://techcrunch.com/page/%s/' % i)
        if r.status_code==200: #what does this mean?i
            dom = lxml.html.fromstring(r.text)
    
            targetList = dom.cssselect('.headline a')
            if len(targetList):
                # Great! This page contains ads to scrape.
                articles = []
                for result in targetList:
                    if keyword in result.text_content():
                        article = {
                        'title': result.text_content(),
                        'url': result.get("href"),
                        'keyword': keyword,
                        'source': 'techcrunch'
                        }
                        print article['title']
                        print article['url']
                        
                        # add this person to the list
                        articles.append(article)

                if len(articles):
                    print 'saving page %s' % i
                    scraperwiki.sqlite.save(['url'], articles)
                else:
                    print "targetList not found"
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
# type in the keyword you want to search for here
# needs to be exact match

keyword = "tanja"

scrape_wired(keyword)
scrape_techCrunch(keyword)
