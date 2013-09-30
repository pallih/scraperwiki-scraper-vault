import scraperwiki
import lxml.html

url = "http://search.twitter.com/search.atom?geocode=52.525509,--2.003334,5km"

root = lxml.html.parse(url).getroot()
print lxml.html.tostring(root)

for el in root.cssselect("div.content a"):
    print el
    print lxml.html.tostring(el)

import urllib
html = urllib.urlopen("http://scraperwiki.com").read()
root = lxml.html.fromstring(html)

for el in root:
    print el.tag
    for el2 in el:
        print "--", el2.tag, el2.attrib

# all paragraphs with class="kkk"
paras = root.cssselect("p.title")

print paras
for p in paras:
    print (p.tag, p.attrib.get("id"), p.text)
    print ("hello")

# For more, click on Quick help and select lxml cheat sheet

import scraperwiki
import lxml.html

url = "http://search.twitter.com/search.atom?geocode=52.525509,--2.003334,5km"

root = lxml.html.parse(url).getroot()
print lxml.html.tostring(root)

for el in root.cssselect("div.content a"):
    print el
    print lxml.html.tostring(el)

import urllib
html = urllib.urlopen("http://scraperwiki.com").read()
root = lxml.html.fromstring(html)

for el in root:
    print el.tag
    for el2 in el:
        print "--", el2.tag, el2.attrib

# all paragraphs with class="kkk"
paras = root.cssselect("p.title")

print paras
for p in paras:
    print (p.tag, p.attrib.get("id"), p.text)
    print ("hello")

# For more, click on Quick help and select lxml cheat sheet

