import mechanize
import scraperwiki
import lxml.html
import lxml.etree

def scrape_tables(root):
    applications = root.cssselect("div.highlight")
    print len(applications)


startURL = "http://www.aberdeencity.gov.uk/planning/pla/pla_planningapps.asp"
br = mechanize.Browser()
br.open(startURL)
response = br.follow_link(url_regex="pla_wl_\d*")
scrape_tables(lxml.html.fromstring(response.read()))

import mechanize
import scraperwiki
import lxml.html
import lxml.etree

def scrape_tables(root):
    applications = root.cssselect("div.highlight")
    print len(applications)


startURL = "http://www.aberdeencity.gov.uk/planning/pla/pla_planningapps.asp"
br = mechanize.Browser()
br.open(startURL)
response = br.follow_link(url_regex="pla_wl_\d*")
scrape_tables(lxml.html.fromstring(response.read()))

