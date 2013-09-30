import scraperwiki
import urllib2
import lxml.etree

# fetch from http://www.lordswhips.org.uk/display/templatedisplay1.asp?sectionid=7

url = 'http://www.lordswhips.org.uk/documents/FB%202013%2003%2027%20r.pdf'
pdfdata = urllib2.urlopen(url).read()

xmldata = scraperwiki.pdftoxml(pdfdata)

#print xmldata

root = lxml.etree.fromstring(xmldata)
pages = list(root)
mytext = ""

for page in root:
    for line in page:
        #if line.tag == 'text':
        #    mytext += '\n[' + line.attrib['font'] + '] '
        if line.text:
            mytext += '\n' + line.text


print mytextimport scraperwiki
import urllib2
import lxml.etree

# fetch from http://www.lordswhips.org.uk/display/templatedisplay1.asp?sectionid=7

url = 'http://www.lordswhips.org.uk/documents/FB%202013%2003%2027%20r.pdf'
pdfdata = urllib2.urlopen(url).read()

xmldata = scraperwiki.pdftoxml(pdfdata)

#print xmldata

root = lxml.etree.fromstring(xmldata)
pages = list(root)
mytext = ""

for page in root:
    for line in page:
        #if line.tag == 'text':
        #    mytext += '\n[' + line.attrib['font'] + '] '
        if line.text:
            mytext += '\n' + line.text


print mytext