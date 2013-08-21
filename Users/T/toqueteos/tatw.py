"""
Above & Beyond - TATW

Trance Around the World Podcast scraper
"""

PODCAST_URL = "http://www.tatw.co.uk/podcast.xml"

BULK_KEYS = [
    "category", "description", "author",
    "title", "explicit", "keywords",
    "link", "guid", "summary"
]

import scraperwiki
from lxml import etree

# Get podcast contents
xml = scraperwiki.scrape(PODCAST_URL)
print "Got xml file!"

# Parse it as XML, or something
events = ["start", "end"]
root = etree.XML(xml)
print "Starting tag is '<{0}>'.".format(root.tag)

# Traverse tree
context = etree.iterwalk(root, events=events)

# Flags
podcast = []
add_to_item = False
item = -1

# Save items on dict
for action, elem in context:
    if elem.tag.startswith("{"):
        ns = elem.tag.find("}") + 1
        elem.tag = elem.tag[ns:]

    if action == "start":
        if elem.tag == "item":
            add_to_item = True
            item += 1
            podcast.append( dict() )
        else:
            if add_to_item:
                if elem.tag == "enclosure":
                    podcast[item]["url"] = elem.attrib["url"]
                    podcast[item]["length"] = elem.attrib["length"]
                else:
                    podcast[item][elem.tag] = elem.text
    elif action == "end":
        if elem.tag == "item":
            add_to_item = False

    # print "{0}: {1}".format(action, elem.tag)

print "Finished parsing podcast RSS!"
print "Podcast dict has length {0}.".format( len(podcast) )

print "Saving podcast to database..."
for item in podcast:
    # Delete some data from dict
    for k in BULK_KEYS:
        try:
            del item[k]
        except KeyError:
            pass
    scraperwiki.sqlite.save(unique_keys=["subtitle"], data=item)
print "Podcast saved!"
