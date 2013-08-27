import scraperwiki
import urllib2
import lxml.etree
url = "http://www.saps.gov.za/statistics/reports/crimestats/2012/provinces/w_cape/pdf/capetowncentral.pdf"
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
#print len(xmldata)
#print xmldata
root = lxml.etree.fromstring(xmldata)
lines = root.findall('.//text')
for line in lines:
    
    record1 = line.text
    print record1


import scraperwiki
import urllib2
import lxml.etree
url = "http://www.saps.gov.za/statistics/reports/crimestats/2012/provinces/w_cape/pdf/capetowncentral.pdf"
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
#print len(xmldata)
#print xmldata
root = lxml.etree.fromstring(xmldata)
lines = root.findall('.//text')
for line in lines:
    
    record1 = line.text
    print record1


