"""
Scrapes www.guernseyfc.com to obtain recent news articles.
"""

import scraperwiki
import urllib2
import hashlib
import string
from html5lib import HTMLParser, treebuilders
from lxml import etree


def ourhash(x):
    return "%010d"%(int(hashlib.sha224(str(x)).hexdigest(),16)%10000000000)


url = "http://www.guernseyfc.com/news-team-news"
ns = "{http://www.w3.org/1999/xhtml}"
headers = [("user-agent","Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.1.16) Gecko/20120131 Iceweasel/3.5.16 (like Firefox/3.5.16)")]


def news():
    global url
    global ns
    global headers

    opener = urllib2.build_opener()
    opener.addheaders = headers

    pagetext = opener.open(url)
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
    page = parser.parse(pagetext)
    main = page.find("//%sdiv[@class='centre-wide-main-content-column']"%ns)
    for entry in main.findall("%sdiv"%ns):
        title = entry.find("%sdiv[@class='news-item news-title']"%ns).text.strip()

        number = int(filter(lambda c: c in string.digits, (entry.attrib.get("onclick","0"))))
        url = "http://www.guernseyfc.com/news.details.php?id=%d&random=%s"%(number,ourhash(number))

        head_tag = entry.find("%sdiv[@class='news-item news-brief-descript']/%stable/%stbody/%str/%std/%sh1"%(ns,ns,ns,ns,ns,ns))
        if head_tag is None:
            head = ""
        else:
            head = head_tag.text
        
        scraperwiki.sqlite.save(unique_keys=["number"],data={"title":title, "number":number, "url":url, "head":head})

news()

