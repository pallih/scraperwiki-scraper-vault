# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import re
from xml.dom import minidom

url = "http://www.reallyuseful.com/news/latest-news/RSS"

dom = minidom.parse(urllib.urlopen(url))

for node in dom.getElementsByTagName('item'):
    record = {} 
    for cnode in node.childNodes:
    
        if cnode.nodeType == cnode.ELEMENT_NODE and cnode.firstChild:
            record[cnode.localName] = cnode.firstChild.nodeValue
    #print record
    scraperwiki.datastore.save(['title', 'date'], record)
# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import re
from xml.dom import minidom

url = "http://www.reallyuseful.com/news/latest-news/RSS"

dom = minidom.parse(urllib.urlopen(url))

for node in dom.getElementsByTagName('item'):
    record = {} 
    for cnode in node.childNodes:
    
        if cnode.nodeType == cnode.ELEMENT_NODE and cnode.firstChild:
            record[cnode.localName] = cnode.firstChild.nodeValue
    #print record
    scraperwiki.datastore.save(['title', 'date'], record)
