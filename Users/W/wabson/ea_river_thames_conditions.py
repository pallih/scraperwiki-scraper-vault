import scraperwiki
from lxml import etree
from email.utils import parsedate_tz, mktime_tz

# Scrape River Thames conditions from the EA site riverconditions.environment-agency.gov.uk

rss_uri = 'http://riverconditions.environment-agency.gov.uk/feed.rss'
data_items = []
unique_keys = ['location', 'status', 'pubdate']
table_name = 'conditions'
data_verbose = 1

def main():
    conditions_xml = scraperwiki.scrape(rss_uri)
    item_els = etree.fromstring(conditions_xml).findall('channel/item')
    for item in item_els:
        scrape_item(item)
    scraperwiki.sqlite.save(unique_keys=unique_keys, data=data_items, table_name=table_name, verbose=data_verbose)

def scrape_item(el):
    title = el.find('title').text.strip()
    pubdate = int(mktime_tz(parsedate_tz(el.find('pubDate').text.strip())))
    titleparts = title.split(' - ')
    if len(titleparts) <> 2:
        raise Exception('Could not parse item title ' + title)
    data_items.append({ 'location': titleparts[0], 'status': titleparts[1], 'pubdate': pubdate })

main()
import scraperwiki
from lxml import etree
from email.utils import parsedate_tz, mktime_tz

# Scrape River Thames conditions from the EA site riverconditions.environment-agency.gov.uk

rss_uri = 'http://riverconditions.environment-agency.gov.uk/feed.rss'
data_items = []
unique_keys = ['location', 'status', 'pubdate']
table_name = 'conditions'
data_verbose = 1

def main():
    conditions_xml = scraperwiki.scrape(rss_uri)
    item_els = etree.fromstring(conditions_xml).findall('channel/item')
    for item in item_els:
        scrape_item(item)
    scraperwiki.sqlite.save(unique_keys=unique_keys, data=data_items, table_name=table_name, verbose=data_verbose)

def scrape_item(el):
    title = el.find('title').text.strip()
    pubdate = int(mktime_tz(parsedate_tz(el.find('pubDate').text.strip())))
    titleparts = title.split(' - ')
    if len(titleparts) <> 2:
        raise Exception('Could not parse item title ' + title)
    data_items.append({ 'location': titleparts[0], 'status': titleparts[1], 'pubdate': pubdate })

main()
