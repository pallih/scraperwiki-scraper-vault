import scraperwiki

# Dummy URL load to give ScraperWiki something to screenshot.
scraperwiki.scrape("http://www.legislation.gov.uk/uksi/2012/1803/made?view=plain")

import urllib2

xml = urllib2.urlopen("http://www.legislation.gov.uk/uksi/2012/1803/data.xml")

from lxml import etree
doc = etree.parse(xml)
ns = {'ukl': 'http://www.legislation.gov.uk/namespaces/legislation',
      'html': 'http://www.w3.org/1999/xhtml'}

xheads = doc.xpath('//*[@id="schedule"]/ukl:ScheduleBody/ukl:Pblock', namespaces = ns)

for xhead in xheads:
    xhid = xhead.xpath('string(@IdURI)').rpartition('/')[2]
    texts = xhead.xpath('.//html:td', namespaces = ns)
    for t in texts:
        name = t.xpath('string()').strip()
        scraperwiki.sqlite.save(unique_keys=["name"], data={"xhead": xhid, "name": name})

scraperwiki.sqlite.execute('CREATE INDEX swdata_byname ON swdata(name)')
import scraperwiki

# Dummy URL load to give ScraperWiki something to screenshot.
scraperwiki.scrape("http://www.legislation.gov.uk/uksi/2012/1803/made?view=plain")

import urllib2

xml = urllib2.urlopen("http://www.legislation.gov.uk/uksi/2012/1803/data.xml")

from lxml import etree
doc = etree.parse(xml)
ns = {'ukl': 'http://www.legislation.gov.uk/namespaces/legislation',
      'html': 'http://www.w3.org/1999/xhtml'}

xheads = doc.xpath('//*[@id="schedule"]/ukl:ScheduleBody/ukl:Pblock', namespaces = ns)

for xhead in xheads:
    xhid = xhead.xpath('string(@IdURI)').rpartition('/')[2]
    texts = xhead.xpath('.//html:td', namespaces = ns)
    for t in texts:
        name = t.xpath('string()').strip()
        scraperwiki.sqlite.save(unique_keys=["name"], data={"xhead": xhid, "name": name})

scraperwiki.sqlite.execute('CREATE INDEX swdata_byname ON swdata(name)')
