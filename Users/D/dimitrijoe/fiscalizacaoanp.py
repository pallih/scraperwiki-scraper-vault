import scraperwiki
import urllib2
import lxml.etree, lxml.html
import re

pdfurl = "http://personal.lse.ac.uk/szerman/AM.pdf"

request = urllib2.Request(pdfurl, headers={'User-Agent' : "Magic Browser"})
response = urllib2.urlopen(request)
pdfdata = response.read()
pdfxml = scraperwiki.pdftoxml(pdfdata)

root = lxml.html.fromstring(pdfxml)

for page in root:
    assert page.tag == 'page'
    print page.text_content().strip()
