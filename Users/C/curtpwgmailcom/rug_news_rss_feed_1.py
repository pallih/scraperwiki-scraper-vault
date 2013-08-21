# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import re
from xml.dom import minidom

url = "http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daz&max=100&links=preserve&exc=&submit=Create+Feed"

dom = minidom.parse(urllib.urlopen(url))

for node in dom.getElementsByTagName('item'):
    record = {} 
    for cnode in node.childNodes:
    
        if cnode.nodeType == cnode.ELEMENT_NODE and cnode.firstChild:
            record[cnode.localName] = cnode.firstChild.nodeValue
    #print record
    scraperwiki.datastore.save(['title', 'date'], record)
