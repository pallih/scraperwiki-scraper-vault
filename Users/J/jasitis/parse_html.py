import scraperwiki 
import lxml.html
import urllib2
from urllib2 import urlopen
from lxml.html import parse


html = scraperwiki.scrape("http://lurnq.com/")
page = urlopen('http://lurnq.com/')
p = parse(page)
p.getroot()
root = lxml.html.fromstring(html)
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
tree = lxml.html.fromstring(html)
tree.xpath('//table[@class="quotes"]/tr')
print tree[1].tag                # i
print tree[1].getparent().tag    # h2
print tree[1].getprevious().tag  # b
print tree[1].getnext()          # None
print tree[1].getchildren()      # [<Element em>]
import scraperwiki 
import lxml.html
import urllib2
from urllib2 import urlopen
from lxml.html import parse


html = scraperwiki.scrape("http://lurnq.com/")
page = urlopen('http://lurnq.com/')
p = parse(page)
p.getroot()
root = lxml.html.fromstring(html)
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
tree = lxml.html.fromstring(html)
tree.xpath('//table[@class="quotes"]/tr')
print tree[1].tag                # i
print tree[1].getparent().tag    # h2
print tree[1].getprevious().tag  # b
print tree[1].getnext()          # None
print tree[1].getchildren()      # [<Element em>]
