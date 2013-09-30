# Blank Python

import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://studio.jwcc.jp/")
root = lxml.html.fromstring(html)

for el in root.cssselect("div.menu_area a"):

    print lxml.html.tostring(el)
    print el.attrib['href']
    print el.text
    print el.tail

def ctext(el):
    result = [ ]
    if el.text:
        result.append(el.text)
    for sel in el:
        assert sel.tag in ["b", "i"]
        result.append("<"+sel.tag+">")
        result.append(ctext(sel))
        result.append("</"+sel.tag+">")
        if sel.tail:
            result.append(sel.tail)
    return "".join(result)


#eg = lxml.html.fromstring('<h2>A thing <b>goes boom</b> up <i>on <em>the tree</em></i></h2>')
eg = lxml.html.fromstring(html)
print eg.text_content() # 'A thing goes boom up on the tree'



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
# Blank Python

import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://studio.jwcc.jp/")
root = lxml.html.fromstring(html)

for el in root.cssselect("div.menu_area a"):

    print lxml.html.tostring(el)
    print el.attrib['href']
    print el.text
    print el.tail

def ctext(el):
    result = [ ]
    if el.text:
        result.append(el.text)
    for sel in el:
        assert sel.tag in ["b", "i"]
        result.append("<"+sel.tag+">")
        result.append(ctext(sel))
        result.append("</"+sel.tag+">")
        if sel.tail:
            result.append(sel.tail)
    return "".join(result)


#eg = lxml.html.fromstring('<h2>A thing <b>goes boom</b> up <i>on <em>the tree</em></i></h2>')
eg = lxml.html.fromstring(html)
print eg.text_content() # 'A thing goes boom up on the tree'



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
