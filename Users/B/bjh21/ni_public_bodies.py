import scraperwiki
import urllib2
import lxml.etree

url = "http://www.ofmdfmni.gov.uk/public-appointments-annual-report-2010-2011.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 200000 characters are: ", xmldata[:200000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

rows = root.xpath('//page[@number >= 7 and @number <= 11]/text[@left=108]')

prev = None
for row in rows:
    if prev is not None and int(row.attrib['top']) - int(prev.attrib['top']) in [20, 21]:
        # Continuation row
        row.text = prev.text + " " + row.text
        prev.text = ''
    row.text = row.text.strip()
    prev = row

for row in rows:
    if row.text != '':
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name": row.text})import scraperwiki
import urllib2
import lxml.etree

url = "http://www.ofmdfmni.gov.uk/public-appointments-annual-report-2010-2011.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 200000 characters are: ", xmldata[:200000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

rows = root.xpath('//page[@number >= 7 and @number <= 11]/text[@left=108]')

prev = None
for row in rows:
    if prev is not None and int(row.attrib['top']) - int(prev.attrib['top']) in [20, 21]:
        # Continuation row
        row.text = prev.text + " " + row.text
        prev.text = ''
    row.text = row.text.strip()
    prev = row

for row in rows:
    if row.text != '':
        scraperwiki.sqlite.save(unique_keys=["name"], data={"name": row.text})