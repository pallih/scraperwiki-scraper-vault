import scraperwiki
import urllib2
import lxml.etree

url = "http://www.met.police.uk/foi/pdfs/priorities_and_how_we_are_doing/corporate/monthly_knife_crime_summary_november2012.pdf" #tried various PDFs, format seems the same at least for top block


pdfdata = urllib2.urlopen(url).read()

print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)

print "After converting to xml it has %d bytes" % len(xmldata)

print xmldata # helpful to see what order in the XML the text tags are in; sometimes top to bottom rather than left to right, which can make scraping rows of data difficult // goes across in rows; that's why OGC won't work as easily, because goes down in columns; maybe need to cycle through looking for matching "top" text tags, then grab all those going across using the leftintegers

import scraperwiki
import urllib2
import lxml.etree

url = "http://www.met.police.uk/foi/pdfs/priorities_and_how_we_are_doing/corporate/monthly_knife_crime_summary_november2012.pdf" #tried various PDFs, format seems the same at least for top block


pdfdata = urllib2.urlopen(url).read()

print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)

print "After converting to xml it has %d bytes" % len(xmldata)

print xmldata # helpful to see what order in the XML the text tags are in; sometimes top to bottom rather than left to right, which can make scraping rows of data difficult // goes across in rows; that's why OGC won't work as easily, because goes down in columns; maybe need to cycle through looking for matching "top" text tags, then grab all those going across using the leftintegers

