import scraperwiki

# Blank Python
import urllib2
import lxml.etree
url = "http://www.madingley.org/uploaded/Hansard_08.07.2010.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)
xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata [:2000]
root = lxml.etree.fromstring(xmldata)
pages = list(root)
print   "The pages are numbered:",  [page.attrib.get("number") for page in pages]
def gettext_with_bi_tags(el):  
    res = [ ] 
    if el.text: 
        res.append(el.text) 
    for lel in el:
        res.append("<%s>" % lel.tag) 
        res.append(gettext_with_bi_tags(lel)) 
        res.append("</%s>" % lel.tag) 
    if el.tail: 
        res.append(el.tail) 
    return "".join(res) 
# print the first hundred text elements from the first page 
page0 = pages[0] 
for el in list(page0)[:100]: 
    if el.tag == "text": 
        print el.attrib, gettext_with_bi_tags(el)
ID = 0 
record = {} 
record["text"] = gettext_with_bi_tags(el) 
ID = ID+1 
record["ID"] = ID 
scraperwiki.sqlite.save(["ID"],record) 
print record






import scraperwiki

# Blank Python
import urllib2
import lxml.etree
url = "http://www.madingley.org/uploaded/Hansard_08.07.2010.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)
xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata [:2000]
root = lxml.etree.fromstring(xmldata)
pages = list(root)
print   "The pages are numbered:",  [page.attrib.get("number") for page in pages]
def gettext_with_bi_tags(el):  
    res = [ ] 
    if el.text: 
        res.append(el.text) 
    for lel in el:
        res.append("<%s>" % lel.tag) 
        res.append(gettext_with_bi_tags(lel)) 
        res.append("</%s>" % lel.tag) 
    if el.tail: 
        res.append(el.tail) 
    return "".join(res) 
# print the first hundred text elements from the first page 
page0 = pages[0] 
for el in list(page0)[:100]: 
    if el.tag == "text": 
        print el.attrib, gettext_with_bi_tags(el)
ID = 0 
record = {} 
record["text"] = gettext_with_bi_tags(el) 
ID = ID+1 
record["ID"] = ID 
scraperwiki.sqlite.save(["ID"],record) 
print record






import scraperwiki

# Blank Python
import urllib2
import lxml.etree
url = "http://www.madingley.org/uploaded/Hansard_08.07.2010.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)
xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata [:2000]
root = lxml.etree.fromstring(xmldata)
pages = list(root)
print   "The pages are numbered:",  [page.attrib.get("number") for page in pages]
def gettext_with_bi_tags(el):  
    res = [ ] 
    if el.text: 
        res.append(el.text) 
    for lel in el:
        res.append("<%s>" % lel.tag) 
        res.append(gettext_with_bi_tags(lel)) 
        res.append("</%s>" % lel.tag) 
    if el.tail: 
        res.append(el.tail) 
    return "".join(res) 
# print the first hundred text elements from the first page 
page0 = pages[0] 
for el in list(page0)[:100]: 
    if el.tag == "text": 
        print el.attrib, gettext_with_bi_tags(el)
ID = 0 
record = {} 
record["text"] = gettext_with_bi_tags(el) 
ID = ID+1 
record["ID"] = ID 
scraperwiki.sqlite.save(["ID"],record) 
print record






