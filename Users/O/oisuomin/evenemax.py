# evenemax.fi event scraper
# output schema is similar to http://schema.org/Event

import scraperwiki
import urllib
import sys
from lxml import etree

# limit number of events (per language), set to 0 to disable (no limit)
LIMIT=0

# read and parse RSS feeds first

RSS_FEEDS = { 
'fi': "http://www.evenemax.fi/tabid/89/IsFreeEvent/False/language/fi-FI/Default.aspx?Feed=RSS",
'sv': "http://www.evenemax.fi/tabid/82/IsFreeEvent/False/language/sv-SE/Default.aspx?Feed=RSS",
}

htmlparser = etree.HTMLParser(encoding='UTF-8')

def date2iso(findate):
    d,m,y = findate.split('.')
    return "%s-%s-%s" % (y,m,d)

# more robust version of etree.parse(), tries up to 3 times
def try_parse(url):
    for i in range(3):
        try:
            tree = etree.parse(url, parser=htmlparser)
            # check that tree is non-empty and actually works
            tree.findtext("//div[@class='SingleSearchResultPlaceAddress']")
            return tree
        except:
            pass
    # failed...
    return None

for lang, url in RSS_FEEDS.items():
    tree = etree.parse(url)
    root = tree.getroot()
    items = 0
    for item in root.findall('.//item'):
        itemdata = {}
        items += 1
        if LIMIT and items > LIMIT: break
        url = item.findtext('link')
        evid = url.split('=')[-1]

        itemdata['id'] = evid
        itemdata['language'] = lang
        itemdata['url'] = url
        itemdata['name'] = item.findtext('title')
        desc = item.findtext('description')
        if desc is not None and desc.strip() != '':
            itemdata['description'] = desc
        itemdata['startDate'] = date2iso(item.findtext('StartDate'))
        itemdata['endDate'] = date2iso(item.findtext('EndDate'))
        itemdata['category'] = item.findtext('Category')
        itemdata['Place_name'] = item.findtext('PlaceName')
        itemdata['addressLocality'] = item.findtext('CountyName')

        # fetch the actual event page to get detailed address information (missing from the RSS feed)
        htmltree = try_parse(url)
        adr = htmltree.findtext("//div[@class='SingleSearchResultPlaceAddress']")
        if adr is not None: itemdata['streetAddress'] = adr.strip()
        pc = htmltree.findtext("//span[@class='SingleSearchResultPlaceAddress']")
        if pc is not None: itemdata['postalCode'] = pc.strip()

        scraperwiki.sqlite.save(unique_keys=["id","language"], data=itemdata)
        print "got items:", items
