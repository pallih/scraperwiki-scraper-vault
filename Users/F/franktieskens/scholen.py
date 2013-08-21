import scraperwiki

meuk = "http://toezichtkaart.owinsp.nl/brincode/16UO/pdf?id=A0000123351"
import urllib2
import lxml.etree
from bs4 import BeautifulSoup
url = meuk
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
eerste5000 = xmldata[:5000]

soep = BeautifulSoup(xmldata)




print soep

