import scraperwiki


baseurl="http://www.commissioningboard.nhs.uk/ccg-details/"
import scraperwiki
import sys

scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swdata")

import urlparse

import lxml.html

def scrape_body(p):
    name = p.xpath('string(strong)')
    website = p.xpath('string(a[1]/@href)')
    #emailhref = body_root.xpath('string(//span[text()="Email: "]/following::a[1]/@href)')
    #emailparts = urlparse.urlsplit(emailhref)
    #if emailparts.scheme == 'mailto':
    #    email = emailparts.path
    #else:
    #    email = None
    scraperwiki.sqlite.save(unique_keys=["name"],
        data={"name": name, "website": website})

def scrape_bodies():
    html = scraperwiki.scrape(baseurl)
    root = lxml.html.fromstring(html)
    for p in root.xpath('//div[@class="entry-content"]//p[strong]'):
        try:
            scrape_body(p)
        except:
            print "while scraping %s:" % name, sys.exc_info()[0]

scrape_bodies()
import scraperwiki


baseurl="http://www.commissioningboard.nhs.uk/ccg-details/"
import scraperwiki
import sys

scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swdata")

import urlparse

import lxml.html

def scrape_body(p):
    name = p.xpath('string(strong)')
    website = p.xpath('string(a[1]/@href)')
    #emailhref = body_root.xpath('string(//span[text()="Email: "]/following::a[1]/@href)')
    #emailparts = urlparse.urlsplit(emailhref)
    #if emailparts.scheme == 'mailto':
    #    email = emailparts.path
    #else:
    #    email = None
    scraperwiki.sqlite.save(unique_keys=["name"],
        data={"name": name, "website": website})

def scrape_bodies():
    html = scraperwiki.scrape(baseurl)
    root = lxml.html.fromstring(html)
    for p in root.xpath('//div[@class="entry-content"]//p[strong]'):
        try:
            scrape_body(p)
        except:
            print "while scraping %s:" % name, sys.exc_info()[0]

scrape_bodies()
