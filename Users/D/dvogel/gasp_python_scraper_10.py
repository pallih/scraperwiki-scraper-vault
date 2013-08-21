import scraperwiki
gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("58706f6c46e34bbca5b2818b4d4a81ee", "B001230")

import re
import lxml.html
from cgi import parse_qsl
from StringIO import StringIO


def just_digits(s):
    return re.sub('[^0-9]+', '', s)


def scrape_frontpage():
    frontpage = scraperwiki.scrape("http://tammybaldwin.house.gov/")

    dom = lxml.html.fromstring(frontpage)
    for number in ["one", "two", "three"]:
        addrtext = dom.cssselect("#offices-%s p" % number)[0]
        links = addrtext.cssselect('a')
        for link in links:
            addrtext.remove(link)

        lines = [ln.strip() for ln in StringIO(addrtext.text_content()).readlines()]
        assert len(lines) == 4
        assert lines[-1].endswith(' Fax')

        address = lines[0]
        (city, state, zip) = re.split('[, ]+', lines[1], 2)
        phone = just_digits(lines[2])
        fax = just_digits(lines[3][:-4])

        gasp.add_office(address, city, state, zip, phone, fax)


def scrape_biography():
    biopage = scraperwiki.scrape("http://tammybaldwin.house.gov/about/biography.shtml")
    dom = lxml.html.fromstring(biopage)
    biotext = '\n\n'.join([p.text_content().strip() 
                           for p in dom.cssselect('div.grid_9 > div.holder-interior-body > p')])
    gasp.add_biography(biotext)


def scrape_issue_page(title, page):
    dom = lxml.html.fromstring(page)
    container = dom.cssselect('div.grid_9 > div.holder-interior-body')[0]
    container.remove(container.cssselect('div.breadcrumb')[0])
    container.remove(container.cssselect('div.boxeeRC50')[0])
    for hr in container.cssselect('div.hr'):
        container.remove(hr)
    container.remove(container.cssselect('div.toggle')[0])
    container.remove(container.cssselect('h5.indepth')[0])
    issuetext = '\n\n'.join([p.text_content().strip() 
                             for p in container.getchildren() 
                             if not isinstance(p, lxml.html.HtmlComment)])
    gasp.add_issue(title, issuetext)
    print title
    print repr(issuetext)


def scrape_issues():
    listingpage = scraperwiki.scrape("http://tammybaldwin.house.gov/issues/")
    dom = lxml.html.fromstring(listingpage)
    dom.make_links_absolute('http://tammybaldwin.house.gov/')
    links = dom.cssselect('div.grid_9 > div.holder-interior-body > h4 > a')
    for link in links:
        if 'href' in link.attrib and link.attrib['href']:
            page = scraperwiki.scrape(link.attrib['href'])
            scrape_issue_page(link.text, page)


def scrape_flickr():
    photospage = scraperwiki.scrape("http://tammybaldwin.house.gov/media/photos.shtml")
    dom = lxml.html.fromstring(photospage)
    flashvars = dom.cssselect('object > param[name="flashvars"]')[0]
    gasp.add_flickr(dict(parse_qsl(flashvars.attrib['value'])).get('page_show_url'))


scrape_frontpage()
scrape_biography()
scrape_issues()
scrape_flickr()
# TODO:
#    YouTube
#    Twitter
#    Facebook
#    Blog post -- entire archive or just RSS feed?
#    News
#    Press releases
#    Event?

gasp.finish()
