from pyquery import PyQuery as pq
import lxml.html
import scraperwiki

BASE_URL = 'http://www.cardin.senate.gov'

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("a25cc8b1f8bc16b4fdbfc23995516049", "C000141")

def scrape_bio():

    print "scraping biography"

    url = BASE_URL + '/about/ben/'
    html = scraperwiki.scrape(url)
    content = pq(html)('#sam-main').text()[10:]
    gasp.add_biography(content, url=url)

def scrape_socialmedia():

    print "scraping social media"

    html = scraperwiki.scrape(BASE_URL)

    elems = pq(html)('ul#social-media li a')

    gasp.add_twitter(elems[0].attrib['href'][20:-3])
    gasp.add_facebook(elems[1].attrib['href'][20:-3])
    gasp.add_flickr(elems[2].attrib['href'][20:-3])
    gasp.add_youtube(elems[3].attrib['href'][20:-3])

def scrape_offices():

    print "scraping offices"
    
    url = BASE_URL + '/contact/regional_offices/'
    html = scraperwiki.scrape(url)

    for elem in (pq(e) for e in pq(html)('div#sam-main div.adr')):

        address = "%s, %s, %s %s" % (
            elem.find('.street-address').text(),
            elem.find('.locality').text(),
            elem.find('.region').text(),
            elem.find('.postal-code').text(),
        )
    
        tel = elem.parent().find('.tel').text()
        phone = tel[5:19]
        fax = tel[25:39] or None

        gasp.add_office(address, phone, fax=fax, url=url)

def scrape_issues():
    
    html = scraperwiki.scrape(BASE_URL + '/issues/')

    for elem in pq(html)('div.issue-list h2 a'):
        
        title = elem.text.strip()[:-2]
        url = elem.attrib['href']

        print "scraping issue %s" % title

        html = scraperwiki.scrape(url)
        content = "\n\n".join(pq(e).text() for e in pq(html)('article > *')[3:])

        gasp.add_issue(title, content, url=url)

def scrape_pressreleases():
    
    for y in xrange(2007, 2013):
        for p in xrange(1, 1000):

            print "scraping press releases from %s, page %s" % (y, p)

            path = '/newsroom/press/index.cfm?PageNum_rs=%s&year=%s' % (p, y) 
            html = scraperwiki.scrape(BASE_URL + path)

            elems = pq(html)('table tr a')

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
scrape_pressreleases()

gasp.finish()from pyquery import PyQuery as pq
import lxml.html
import scraperwiki

BASE_URL = 'http://www.cardin.senate.gov'

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("a25cc8b1f8bc16b4fdbfc23995516049", "C000141")

def scrape_bio():

    print "scraping biography"

    url = BASE_URL + '/about/ben/'
    html = scraperwiki.scrape(url)
    content = pq(html)('#sam-main').text()[10:]
    gasp.add_biography(content, url=url)

def scrape_socialmedia():

    print "scraping social media"

    html = scraperwiki.scrape(BASE_URL)

    elems = pq(html)('ul#social-media li a')

    gasp.add_twitter(elems[0].attrib['href'][20:-3])
    gasp.add_facebook(elems[1].attrib['href'][20:-3])
    gasp.add_flickr(elems[2].attrib['href'][20:-3])
    gasp.add_youtube(elems[3].attrib['href'][20:-3])

def scrape_offices():

    print "scraping offices"
    
    url = BASE_URL + '/contact/regional_offices/'
    html = scraperwiki.scrape(url)

    for elem in (pq(e) for e in pq(html)('div#sam-main div.adr')):

        address = "%s, %s, %s %s" % (
            elem.find('.street-address').text(),
            elem.find('.locality').text(),
            elem.find('.region').text(),
            elem.find('.postal-code').text(),
        )
    
        tel = elem.parent().find('.tel').text()
        phone = tel[5:19]
        fax = tel[25:39] or None

        gasp.add_office(address, phone, fax=fax, url=url)

def scrape_issues():
    
    html = scraperwiki.scrape(BASE_URL + '/issues/')

    for elem in pq(html)('div.issue-list h2 a'):
        
        title = elem.text.strip()[:-2]
        url = elem.attrib['href']

        print "scraping issue %s" % title

        html = scraperwiki.scrape(url)
        content = "\n\n".join(pq(e).text() for e in pq(html)('article > *')[3:])

        gasp.add_issue(title, content, url=url)

def scrape_pressreleases():
    
    for y in xrange(2007, 2013):
        for p in xrange(1, 1000):

            print "scraping press releases from %s, page %s" % (y, p)

            path = '/newsroom/press/index.cfm?PageNum_rs=%s&year=%s' % (p, y) 
            html = scraperwiki.scrape(BASE_URL + path)

            elems = pq(html)('table tr a')

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
scrape_pressreleases()

gasp.finish()