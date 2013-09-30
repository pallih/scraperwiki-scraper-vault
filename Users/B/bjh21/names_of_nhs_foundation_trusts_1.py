baseurl="http://scambs.moderngov.co.uk/mgListCommittees.aspx?PC=1"
import scraperwiki
import sys

scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swdata")

import urlparse

import lxml.html

def scrape_pc(name, url):
    pc_html = scraperwiki.scrape(url)
    pc_root = lxml.html.fromstring(pc_html)
    href = pc_root.xpath('string(//h3[text()="Clerk"]/following::a[1]/@href)')
    href = urlparse.urlsplit(href)
    if href.scheme == 'mailto':
        scraperwiki.sqlite.save(unique_keys=["district", "name"],
            data={"district": "scambs", "name": name, "email": href.path})

def scrape_pcs():
    html = scraperwiki.scrape(baseurl)
    root = lxml.html.fromstring(html)
    for a in root.cssselect(".mgContent a"):
        try:
            name=a.text_content().strip()
            href=a.attrib['href']
            href=urlparse.urljoin(baseurl, href)
            scrape_pc(name, href)
        except:
            print "while scraping %s:" % name, sys.exc_info()[0]

scrape_pcs()
baseurl="http://scambs.moderngov.co.uk/mgListCommittees.aspx?PC=1"
import scraperwiki
import sys

scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swdata")

import urlparse

import lxml.html

def scrape_pc(name, url):
    pc_html = scraperwiki.scrape(url)
    pc_root = lxml.html.fromstring(pc_html)
    href = pc_root.xpath('string(//h3[text()="Clerk"]/following::a[1]/@href)')
    href = urlparse.urlsplit(href)
    if href.scheme == 'mailto':
        scraperwiki.sqlite.save(unique_keys=["district", "name"],
            data={"district": "scambs", "name": name, "email": href.path})

def scrape_pcs():
    html = scraperwiki.scrape(baseurl)
    root = lxml.html.fromstring(html)
    for a in root.cssselect(".mgContent a"):
        try:
            name=a.text_content().strip()
            href=a.attrib['href']
            href=urlparse.urljoin(baseurl, href)
            scrape_pc(name, href)
        except:
            print "while scraping %s:" % name, sys.exc_info()[0]

scrape_pcs()
