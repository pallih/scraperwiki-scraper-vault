import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.bathstore.com/_application/showrooms_all.html") 
root = lxml.html.fromstring(html)
for el in root.cssselect("div.storeSummary a"):
    print el
    print lxml.html.tostring(el)
    print el.attrib['href']
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

     
import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.bathstore.com/_application/showrooms_all.html") 
root = lxml.html.fromstring(html)
for el in root.cssselect("div.storeSummary a"):
    print el
    print lxml.html.tostring(el)
    print el.attrib['href']
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

     
