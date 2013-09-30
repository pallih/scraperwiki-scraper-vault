import scraperwiki

# Blank Python

import lxml.html 
root = lxml.html.parse("http://scraperwiki.com").getroot() 
for el in root.cssselect("div.featured a"): print el 
print lxml.html.tostring(el) 
import urllib html = urllib.urlopen("http://scraperwiki.com").read() root = lxml.html.fromstring(html) 
html = urllib2.urlopen("http://www.meclis.gov.az/?/az/deputat/229").read() root = lxml.html.fromstring(html.decode("utf8")) 
eg = lxml.html.fromstring('<h2>A thing <b>goes boom</b> up <i class="t">on <em id="s">the tree</em></i></h2>') print eg.cssselect("i.t em#s") # [ <element em > ] 

for el in root: print el.tag for el2 in el: print "--", el2.tag, el2.attrib 
for el in root: print el.tag for el2 in el: print "--", el2.tag, el2.attrib 
eg = lxml.html.fromstring('<h2>A thing <b>goes boom</b> up <i>on <em>the tree</em></i></h2>') print eg[1].tag # i print eg[1].getparent().tag # h2 print eg[1].getprevious().tag # b print eg[1].getnext() # None print eg[1].getchildren() # [ <element em > ] 

eg = lxml.html.fromstring('<h2>A thing <b>goes boom</b> up <i>on <em>the tree</em></i></h2>') print eg.text # 'A thing ' print eg[0].text # 'goes boom' print eg[0].tail # ' up ' print eg.text_content # 'A thing goes boom up on the tree' 

def ctext(el): result = [ ] if el.text: result.append(el.text) for sel in el: assert sel.tag in ["b", "i"] result.append("<"+sel.tag+">") result.append(ctext(sel)) result.append("</"+sel.tag+">") if sel.tail: result.append(sel.tail) return "".join(result) import scraperwiki

# Blank Python

import lxml.html 
root = lxml.html.parse("http://scraperwiki.com").getroot() 
for el in root.cssselect("div.featured a"): print el 
print lxml.html.tostring(el) 
import urllib html = urllib.urlopen("http://scraperwiki.com").read() root = lxml.html.fromstring(html) 
html = urllib2.urlopen("http://www.meclis.gov.az/?/az/deputat/229").read() root = lxml.html.fromstring(html.decode("utf8")) 
eg = lxml.html.fromstring('<h2>A thing <b>goes boom</b> up <i class="t">on <em id="s">the tree</em></i></h2>') print eg.cssselect("i.t em#s") # [ <element em > ] 

for el in root: print el.tag for el2 in el: print "--", el2.tag, el2.attrib 
for el in root: print el.tag for el2 in el: print "--", el2.tag, el2.attrib 
eg = lxml.html.fromstring('<h2>A thing <b>goes boom</b> up <i>on <em>the tree</em></i></h2>') print eg[1].tag # i print eg[1].getparent().tag # h2 print eg[1].getprevious().tag # b print eg[1].getnext() # None print eg[1].getchildren() # [ <element em > ] 

eg = lxml.html.fromstring('<h2>A thing <b>goes boom</b> up <i>on <em>the tree</em></i></h2>') print eg.text # 'A thing ' print eg[0].text # 'goes boom' print eg[0].tail # ' up ' print eg.text_content # 'A thing goes boom up on the tree' 

def ctext(el): result = [ ] if el.text: result.append(el.text) for sel in el: assert sel.tag in ["b", "i"] result.append("<"+sel.tag+">") result.append(ctext(sel)) result.append("</"+sel.tag+">") if sel.tail: result.append(sel.tail) return "".join(result) 