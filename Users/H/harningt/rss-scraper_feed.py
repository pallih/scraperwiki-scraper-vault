# Blank Python
sourcescraper = 'rss_merger'

import cgi, os
import scraperwiki

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

baseURL = paramdict.get("baseURL")
if baseURL is None:
    raise Exception("FATAL")

#applyDateRestriction = paramdict.get("applyDateRestriction") == "TRUE"
#dateRestrictionValue = os.getenv("HTTP_IF_MODIFIED_SINCE", "")

#scraperwiki.utils.httpresponseheader("Last-Modified", "Thu, 15 Apr 2004 20:42:41 GMT")

#print dateRestrictionValue
#os.exit()
from lxml import etree

# Grab root RSS data
scraperwiki.sqlite.attach(sourcescraper)
items = scraperwiki.sqlite.select("* FROM rss_merger.rss_root WHERE baseURL = ?", baseURL)

if len(items) < 1:
    raise Exception("Unprocessed RSS feed")

root = items[0]

scraperwiki.utils.httpresponseheader("Content-Type", "text/xml+rss")

parser = etree.XMLParser(ns_clean = True, strip_cdata = False)
tree = etree.fromstring(root.get("data"), parser)

channel = tree.find('channel')

# Apply restriction filtering


entries = scraperwiki.sqlite.select("data FROM rss_merger.rss_item WHERE baseURL = ? ORDER BY julianday(date) DESC", baseURL)
for entry in entries:
    parsed_entry = etree.fromstring(entry.get("data"), parser)
    channel.append(parsed_entry)

print(etree.tostring(tree))# Blank Python
sourcescraper = 'rss_merger'

import cgi, os
import scraperwiki

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

baseURL = paramdict.get("baseURL")
if baseURL is None:
    raise Exception("FATAL")

#applyDateRestriction = paramdict.get("applyDateRestriction") == "TRUE"
#dateRestrictionValue = os.getenv("HTTP_IF_MODIFIED_SINCE", "")

#scraperwiki.utils.httpresponseheader("Last-Modified", "Thu, 15 Apr 2004 20:42:41 GMT")

#print dateRestrictionValue
#os.exit()
from lxml import etree

# Grab root RSS data
scraperwiki.sqlite.attach(sourcescraper)
items = scraperwiki.sqlite.select("* FROM rss_merger.rss_root WHERE baseURL = ?", baseURL)

if len(items) < 1:
    raise Exception("Unprocessed RSS feed")

root = items[0]

scraperwiki.utils.httpresponseheader("Content-Type", "text/xml+rss")

parser = etree.XMLParser(ns_clean = True, strip_cdata = False)
tree = etree.fromstring(root.get("data"), parser)

channel = tree.find('channel')

# Apply restriction filtering


entries = scraperwiki.sqlite.select("data FROM rss_merger.rss_item WHERE baseURL = ? ORDER BY julianday(date) DESC", baseURL)
for entry in entries:
    parsed_entry = etree.fromstring(entry.get("data"), parser)
    channel.append(parsed_entry)

print(etree.tostring(tree))