from pdfminer.pdfparser import PDFParser, PDFDocument
import StringIO
import scraperwiki
import urllib2
import string
import lxml.etree
import lxml.html
import lxml.cssselect
from bs4 import BeautifulSoup


try:
    scraperwiki.sqlite.execute("create table donors (donor string, amount string, party string, major string,year string)")

except:
    print "Table probably already exists."

url = "http://periodicdisclosures.aec.gov.au/Returns/49/PNGX9.pdf"

pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
#print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 20000 characters are: ", xmldata[:20000]

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
page0 = pages[0]
for el in list(page)[:100]:
    if el.tag == "text":
        pass#print el.attrib, gettext_with_bi_tags(el)

#where = xmldata.find('Received from')
#thereitis = xmldata[where-500:]
#print thereitis

o = 0
count = 0
while o < len(root):
    for text in root[o].iter('text'):
        if text.text == None:
            pass
        else:
            if 'Donation' in text.text:
                count += 1
                try:
                    if root[o][root[o].index(text)+6].text.isupper() == False:
                        print count,root[o][root[o].index(text)-2].text,root[o][root[o].index(text)-1].text,root[o][root[o].index(text)+3].text,root[o][root[o].index(text)+5].text,root[o][root[o].index(text)+9].text
                    else:
                        print count,root[o][root[o].index(text)-2].text,root[o][root[o].index(text)-1].text,root[o][root[o].index(text)+3].text,root[o][root[o].index(text)+6].text,root[o][root[o].index(text)+7].text,root[o][root[o].index(text)+10].text
                except:
                    print 'it goes across the page!'
    o += 1