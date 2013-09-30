import scraperwiki
import requests
import lxml.html


def scrape_people():
    for i in range (''):
        print 'scraping page %s' % i
        r = requests.get('http://stud.idevarlden.com/' % i).text
        dom = lxml.html.fromstring(r)
        for student in dom.cssselect('div.kol_300 li'):
           d = {
                'name': student.cssselect('href')[0].text
                }
            scraperwiki.sqlite.save([''], d)

scrape_people()


import scraperwiki
import requests
import lxml.html


def scrape_people():
    for i in range (''):
        print 'scraping page %s' % i
        r = requests.get('http://stud.idevarlden.com/' % i).text
        dom = lxml.html.fromstring(r)
        for student in dom.cssselect('div.kol_300 li'):
           d = {
                'name': student.cssselect('href')[0].text
                }
            scraperwiki.sqlite.save([''], d)

scrape_people()


