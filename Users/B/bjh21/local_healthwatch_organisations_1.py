import scraperwiki


baseurl="http://www.healthwatch.co.uk/find-local-heathwatch"
import scraperwiki
import sys

scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swdata")

from urlparse import urlparse

import lxml.html

def scrape_bodies():
    html = scraperwiki.scrape(baseurl)
    root = lxml.html.fromstring(html)
    for item in root.xpath('//div[@class="map-item"]'):
        try:
            name=item.xpath('string(.//h3)')
            website=item.xpath('string(.//a[.="Visit website"]/@href)')
            emailurl=item.xpath('string(.//a[.="Send an email"]/@href)')
            email=urlparse(emailurl).path
            scraperwiki.sqlite.save(unique_keys=["name"],
                data={"name": name, "website": website, "email": email})
        except:
            print "while scraping %s:" % name, sys.exc_info()[0]

scrape_bodies()
import scraperwiki


baseurl="http://www.healthwatch.co.uk/find-local-heathwatch"
import scraperwiki
import sys

scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swdata")

from urlparse import urlparse

import lxml.html

def scrape_bodies():
    html = scraperwiki.scrape(baseurl)
    root = lxml.html.fromstring(html)
    for item in root.xpath('//div[@class="map-item"]'):
        try:
            name=item.xpath('string(.//h3)')
            website=item.xpath('string(.//a[.="Visit website"]/@href)')
            emailurl=item.xpath('string(.//a[.="Send an email"]/@href)')
            email=urlparse(emailurl).path
            scraperwiki.sqlite.save(unique_keys=["name"],
                data={"name": name, "website": website, "email": email})
        except:
            print "while scraping %s:" % name, sys.exc_info()[0]

scrape_bodies()
