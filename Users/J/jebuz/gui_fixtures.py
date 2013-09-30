import scraperwiki
import urlparse
import lxml.html

base_url = 'http://gui.ie/fixture_detail.asp?club='
max_id = 500

def getTableRows(id):
    url = generateUrl(id)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    trs = root.cssselect('tr')
    return trs;

def scrapeFixtures(id):
    trs = getTableRows(id)
    for tr in trs:
        tds = tr.cssselect('td')
        if(len(tds) == 4):
            record = {}
            record['id'] = id
            record['club'] = tds[2].text
            record['type'] = tds[3].text
            record['start'] = tds[0].text
            record['end'] = tds[1].text
            print record
            scraperwiki.datastore.save(['club', 'start'], record)

def generateUrl(id):
    return base_url + str(id)

def scrapeAllCourses():
    for i in range(max_id ):
        scrapeFixtures(i+1)


# scrape just one course (test)
#scrapeFixtures(2)

# scrape all courses
scrapeAllCourses()

import scraperwiki
import urlparse
import lxml.html

base_url = 'http://gui.ie/fixture_detail.asp?club='
max_id = 500

def getTableRows(id):
    url = generateUrl(id)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    trs = root.cssselect('tr')
    return trs;

def scrapeFixtures(id):
    trs = getTableRows(id)
    for tr in trs:
        tds = tr.cssselect('td')
        if(len(tds) == 4):
            record = {}
            record['id'] = id
            record['club'] = tds[2].text
            record['type'] = tds[3].text
            record['start'] = tds[0].text
            record['end'] = tds[1].text
            print record
            scraperwiki.datastore.save(['club', 'start'], record)

def generateUrl(id):
    return base_url + str(id)

def scrapeAllCourses():
    for i in range(max_id ):
        scrapeFixtures(i+1)


# scrape just one course (test)
#scrapeFixtures(2)

# scrape all courses
scrapeAllCourses()

