import scraperwiki

# Dummy URL load to give ScraperWiki something to screenshot.
scraperwiki.scrape("http://www.legislation.gov.uk/nisr/2013/109/made?view=plain")

xml = scraperwiki.scrape("http://www.legislation.gov.uk/nisr/2013/109/data.xml")

from lxml import etree
doc = etree.fromstring(xml)
ns = {'ukl': 'http://www.legislation.gov.uk/namespaces/legislation'}

texts = doc.xpath('//*[@id="schedule-1"]/ukl:ScheduleBody//ukl:Text', namespaces = ns)
for t in texts:
    name = t.xpath('string()').strip()
    scraperwiki.sqlite.save(unique_keys=["name"], data={"name": name})

#scraperwiki.sqlite.execute('CREATE INDEX swdata_byname ON swdata(name)')
