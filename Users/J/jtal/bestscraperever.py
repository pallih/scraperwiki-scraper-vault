import scraperwiki
import urllib2
import lxml.etree

url = "http://comptroller.defense.gov/defbudget/fy2011/fy2011_r1.pdf"

pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)

print xmldata[:60000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

# print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

import scraperwiki
import urllib2
import lxml.etree

url = "http://comptroller.defense.gov/defbudget/fy2011/fy2011_r1.pdf"

pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)

print xmldata[:60000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

# print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

