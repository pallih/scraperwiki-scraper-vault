import scraperwiki
import urllib, urlparse
import re
from xml.dom import minidom

url = "http://pipes.yahoo.com/pipes/pipe.run?_id=abb17cec97c3daff8821066d31c95aa5&_render=rss"

dom = minidom.parse(urllib.urlopen(url))

prog = re.compile("^(.*?), (.*?)(?: \((.*)\))?$")

for node in dom.getElementsByTagName('item'):
    record = {} 

    for cnode in node.childNodes:
        if cnode.nodeType == cnode.ELEMENT_NODE and cnode.firstChild:
            if cnode.localName == 'title':
                result = prog.match(cnode.firstChild.nodeValue)
                if result:
                    record["title"] = result.group(1)
                    record["location"] = result.group(2)
                    record["company"] = result.group(3)
                else:
                    print "<<%s>>" %cnode.firstChild.nodeValue
            else:
                record[cnode.localName] = cnode.firstChild.nodeValue

    #print record
    scraperwiki.sqlite.save(['link'], record)
import scraperwiki
import urllib, urlparse
import re
from xml.dom import minidom

url = "http://pipes.yahoo.com/pipes/pipe.run?_id=abb17cec97c3daff8821066d31c95aa5&_render=rss"

dom = minidom.parse(urllib.urlopen(url))

prog = re.compile("^(.*?), (.*?)(?: \((.*)\))?$")

for node in dom.getElementsByTagName('item'):
    record = {} 

    for cnode in node.childNodes:
        if cnode.nodeType == cnode.ELEMENT_NODE and cnode.firstChild:
            if cnode.localName == 'title':
                result = prog.match(cnode.firstChild.nodeValue)
                if result:
                    record["title"] = result.group(1)
                    record["location"] = result.group(2)
                    record["company"] = result.group(3)
                else:
                    print "<<%s>>" %cnode.firstChild.nodeValue
            else:
                record[cnode.localName] = cnode.firstChild.nodeValue

    #print record
    scraperwiki.sqlite.save(['link'], record)
