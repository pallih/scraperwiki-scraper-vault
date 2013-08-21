from pyquery import PyQuery as pq
import lxml.html
import scraperwiki

BASE_URL = 'http://www.blunt.senate.gov'

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("ff793f3122f94d359b958b534db34071", "B000575")

def scrape_bio():

    print "scraping biography"

    url = BASE_URL + '/public/index.cfm/about-the-senator'
    html = scraperwiki.scrape(url)
    content = pq(html)('.section #copy').text()
    gasp.add_biography(content, url=url)

def scrape_socialmedia():

    print "scraping social media"
    url = BASE_URL + '/public/index.cfm/home'
    html = scraperwiki.scrape(url)

    elems = pq(html)('.soc-net div.templateWrapper a')


def scrape_offices():

    print "scraping offices"

    url = BASE_URL + '/public/index.cfm/office-locations'
    html = scraperwiki.scrape(url)
    content = pq(html)('div.section #copy').text()
    
    for content in (pq(e) for e in pq(html)('.article')):
        content.find('.header h2').text(),
        content.find('p').text()
        print content.text()

    gasp.add_office(content, html, url=url)
    
     

def scrape_issues():
    
    
    url = BASE_URL + '/public/index.cfm/issues'
    html = scraperwiki.scrape(url)
    content = pq(html)('#content').text()
    headerContent = pq(html)('.table-of-contents ul li h2 a').text()
    issuesContent = pq(html)('.abstract').text()

    

    gasp.add_issue(content, issuesContent, url=url)

def scrape_pressreleases():
    
    for y in xrange(2011, 2012):
        for p in xrange(1, 1000):

            print "scraping press releases from %s, page %s" % (y, p)

            path = '/public/index.cfm/press-releases' % (p, y) 
            html = scraperwiki.scrape(BASE_URL + path)

            elems = pq(html)('table tr td.record-list td.record-list-title a')

            if not elems:
                break

            for elem in elems:
                scrape_pressreleases_page(elem.attrib['href'].strip())

def scrape_pressreleases_page(url):

    html = scraperwiki.scrape(url)
    
    doc = pq(html)('article')

    title = doc.find('h1').text()
    subtitle = doc.find('h2').text()
    if subtitle:
        title += ' ' + subtitle

    date = doc.find('time').text()

    content = "\n\n".join(pq(e).text() for e in doc.children()[4:-1])

    gasp.add_press_release(title, date, content, url=url)


scrape_bio()
scrape_socialmedia()
scrape_offices()
scrape_issues()


gasp.finish()