import scraperwiki           
import lxml.html
html = scraperwiki.scrape("https://scraperwiki.com/")
root = lxml.html.fromstring(html)

for el in root:           
    print el.tag
    for el2 in el:
        print "--", el2.tag, el2.attrib
eg = lxml.html.fromstring('<h2>A thing <b>goes boom</b> up <i>on <em>the tree</em></i></h2>')           
print eg[1].tag                # i
print eg[1].getparent().tag    # h2
print eg[1].getprevious().tag  # b
print eg[1].getnext()          # None
print eg[1].getchildren()      # [<Element em>]import scraperwiki           
import lxml.html
html = scraperwiki.scrape("https://scraperwiki.com/")
root = lxml.html.fromstring(html)

for el in root:           
    print el.tag
    for el2 in el:
        print "--", el2.tag, el2.attrib
eg = lxml.html.fromstring('<h2>A thing <b>goes boom</b> up <i>on <em>the tree</em></i></h2>')           
print eg[1].tag                # i
print eg[1].getparent().tag    # h2
print eg[1].getprevious().tag  # b
print eg[1].getnext()          # None
print eg[1].getchildren()      # [<Element em>]