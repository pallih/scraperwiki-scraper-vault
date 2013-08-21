import scraperwiki
import urllib2
import lxml.etree

url = "http://www.pharmacy.gov.my/v2/sites/default/files/document-upload/fukkm-2-2012.pdf"
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
print "The first 2000 characters are: ", xmldata[:4000]

root = lxml.etree.fromstring(xmldata)
# this line uses xpath to find <text tags 
lines = root.findall('.//text')
print lines
for line in lines:
     print line.text