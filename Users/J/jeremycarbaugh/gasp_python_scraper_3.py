from pyquery import PyQuery as pq
import lxml.html
import scraperwiki

BASE_URL = 'http://vanhollen.house.gov'

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("a25cc8b1f8bc16b4fdbfc23995516049", "V000128")

def scrape_bio():
    
    print "scraping biography"

    html = scraperwiki.scrape(BASE_URL + '/Biography/')
    gasp.add_biography(unicode(html, 'utf-8', errors="ignore"))

def scrape_offices():

    print "scraping offices"

    html = scraperwiki.scrape(BASE_URL)

    d = pq(html)

    for div in d("div.office"):

        lines = [pq(line) for line in pq(div).find('address > span')]

        address = "%s, %s" % (lines[0].text(), lines[1].text())

        phone = lines[2].text()[7:]
        fax = lines[3].text()[5:]

        gasp.add_office(address, phone, fax=fax)
    

def scrape_issues():

    html = scraperwiki.scrape(BASE_URL + "/Issues/")

    d = pq(html)

    for a in d("td#ctl00_ContentCell tr td a"):
    
        pq_a = pq(a)

        url = BASE_URL + pq_a.attr('href')
        title = pq_a.text()

        print "scraping issue %s" % title

        content = scraperwiki.scrape(url)
        content = unicode(content, 'utf-8')

        gasp.add_issue(title, content, url=url)

def scrape_pressreleases():
    for y in xrange(2003, 2013):
        scrape_pressreleases_year(y)

def scrape_pressreleases_year(y):

    for p in xrange(1, 1000):
    
        print "scraping %s, page %s" % (y, p)

        path = "/News/DocumentQuery.aspx?Year=%s&Page=%s" % (y, p)
        html = scraperwiki.scrape(BASE_URL + path)

        d = pq(html)

        a_elems = d("ul.UnorderedNewsList li .middlecopy > a.middlelinks")

        if not a_elems:
            break

        for a in a_elems:
            path = "/News/" + a.attrib['href']
            scrape_pressreleases_page(path)

def scrape_pressreleases_page(path):

    url = BASE_URL + path
    html = scraperwiki.scrape(url)

    d = pq(html)

    title = d("font.middlecopy font.middleheadline").text().strip()
    content = d("font.middlecopy > table tr p")[1]
    date = pq(content).find('b').text().split(',', 1)[1].strip()

    gasp.add_press_release(title, date, pq(content).text(), url=url)

def scrape_social_media():

    print "scraping social media"
    
    html = scraperwiki.scrape(BASE_URL)

    a_elems = pq(html).find('ul.social li a')

    gasp.add_facebook(a_elems[2].attrib['href'])
    gasp.add_twitter(a_elems[3].attrib['href'])
    gasp.add_youtube(a_elems[1].attrib['href'])


scrape_bio()
scrape_offices()
scrape_issues()
scrape_pressreleases()
scrape_social_media()

gasp.finish()