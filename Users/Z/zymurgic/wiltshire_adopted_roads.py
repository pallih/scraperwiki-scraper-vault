###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This tries to make extract meaning from a PDF of road descriptions in Wiltshire
###########################################################################################

import scraperwiki
import lxml.etree
import urllib2
import re

pdfurl = "http://www.wiltshire.gov.uk/adopted-roads-list-wiltshire.pdf"
pdfdata = urllib2.urlopen(pdfurl).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)
# <text top="148" left="84" width="57" height="14" font="0">Principal</text>
# <text top="148" left="284" width="35" height="14" font="0">A27  </text>
# <text top="148" left="362" width="426" height="14" font="0">BRICKWORTH ROAD (A36 EAST TO 30 MPH) WHITEPARISH</text>
# <text top="148" left="1206" width="33" height="14" font="0">1444</text>
# <text top="148" left="1268" width="50" height="14" font="0">422495</text>
# <text top="148" left="1351" width="50" height="14" font="0">123703</text>
# <text top="148" left="1423" width="50" height="14" font="0">423862</text>
# <text top="148" left="1500" width="50" height="14" font="0">123425</text>
# <text top="166" left="84" width="57" height="14" font="0">Principal</text>
# We want to go grouping stuff by text top= per page

match_name_portion_locality=re.compile("^(.+?)\s*?\((.*?)\)\s*?(.+?)$")
match_name_locality=re.compile("^(.+?)\s*?\((.+?)\)$")

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

for page in list(pages):
    for el in list(page):
        if el.tag == "text":
            row = int((int(el.attrib.get('top'))-148)/18)
            if ((row>=0) and (row<57)):
                left = int(el.attrib.get('left'))
                if (left==84):
                    classification=el.text
                if (left==284):
                    ref=el.text.rstrip()
                if (left==362):
                    descr=el.text
                if (left>1200 and left<1260):
                    segment_length=int(el.text);
                if (left>1260 and left<1348):
                    start_e=int(el.text)
                if (left>1348 and left<1400):
                    start_n=int(el.text)
                if (left>1400 and left<1490):
                    end_e=int(el.text)
                if (left>1490):
                    end_n=int(el.text)
                    print classification, ref, descr, segment_length, start_e, start_n, end_e, end_n
                    scraperwiki.sqlite.save(unique_keys=["descr"],data={"classification": classification, "ref": ref, "descr" : descr, "segment_length": segment_length, "start_e" : start_e, "start_n" : start_n, "end_e" : end_e, "end_n" : end_n }, table_name="wiltshire_roads")
#            print row, el.attrib.get('left'), gettext_with_bi_tags(el)

