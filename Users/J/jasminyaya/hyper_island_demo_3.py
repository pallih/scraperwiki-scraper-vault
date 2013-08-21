import scraperwiki
import requests
import lxml.html

def scrape_people():
    for i in range(1,15):
        print 'scraping page %s' % i
        r = requests.get('http://salaamlove.com/' % i).text
        dom = lxml.html.fromstring(r)
        for age in dom.cssselect('div.community_list td'):
            d = {
                'name': age.cssselect('h6')[0].text,
                'url': age.cssselect('a')[0].get('href'),
                'course': student.cssselect('p.subtitle')[0].text
            }
            scraperwiki.sqlite.save(['url'], d)

scrape_age()

#td is the images