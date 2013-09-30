import scraperwiki
import urllib2
import lxml.etree

url = "http://cfo.dc.gov/cfo/lib/cfo/budget/fy2013/tables/government_direction_and_support/ab_council_tables.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
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
# page0 = pages[0]
# for el in list(page)[:100]:
#    if el.tag == "text":
#        print el.attrib, gettext_with_bi_tags(el)

for page in pages[0]:
    print gettext_with_bi_tags(page)import scraperwiki
import urllib2
import lxml.etree

url = "http://cfo.dc.gov/cfo/lib/cfo/budget/fy2013/tables/government_direction_and_support/ab_council_tables.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
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
# page0 = pages[0]
# for el in list(page)[:100]:
#    if el.tag == "text":
#        print el.attrib, gettext_with_bi_tags(el)

for page in pages[0]:
    print gettext_with_bi_tags(page)