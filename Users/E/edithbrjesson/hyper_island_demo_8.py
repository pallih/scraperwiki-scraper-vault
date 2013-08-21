import scraperwiki
import requests
import lxml.html

def scrape_people():
    for i in range(1,15):
        print 'scraping page %s' % i
        r = requests.get('http://www.alltomstockholm.se/?c0=&c1=&c2=&c3=&x=23&y=7&filter=true&s=7').text
        dom = lxml.html.fromstring(r)
        for student in dom.cssselect('#AOS_DesignContent'):
            d = {
                'name': student.cssselect('h6')[0].text,
                'url': student.cssselect('a')[0].get('href'),
                'course': student.cssselect('p.subtitle')[0].text
            }
            scraperwiki.sqlite.save(['url'], d)

scrape_people()