import scraperwiki
import urllib2
import lxml.etree

url = "http://planningcommission.nic.in/data/datatable/0904/tab_12.pdf"

pdfdata = urllib2.urlopen(url).read()

print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)


