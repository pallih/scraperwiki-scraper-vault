import scraperwiki
import requests
import lxml.html

def scrape_people():
    for i in range(1,15):
        print 'scraping page %s' % i
        r = requests.get('http://www.hyperisland.com/people?filter=true&page=%s&role=student' % i).text
        dom = lxml.html.fromstring(r)
        for student in dom.cssselect('div class ="resultListHeader'):
            d = {
                'name': resultListHeader.cssselect('Namn')[0].,
                'Tyoe': resultListHeader.cssselect('Type')[0].
                'Price': resultListHeader.cssselect('Pris')[0].text
            }
            scraperwiki.sqlite.save(['url'], d)

scrape_people()import scraperwiki
import requests
import lxml.html

def scrape_people():
    for i in range(1,15):
        print 'scraping page %s' % i
        r = requests.get('http://www.hyperisland.com/people?filter=true&page=%s&role=student' % i).text
        dom = lxml.html.fromstring(r)
        for student in dom.cssselect('div class ="resultListHeader'):
            d = {
                'name': resultListHeader.cssselect('Namn')[0].,
                'Tyoe': resultListHeader.cssselect('Type')[0].
                'Price': resultListHeader.cssselect('Pris')[0].text
            }
            scraperwiki.sqlite.save(['url'], d)

scrape_people()