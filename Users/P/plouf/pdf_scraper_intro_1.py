# 1. Add some necessary libraries
import scraperwiki
import urllib2, lxml.etree

# 2. The URL/web address where we can find the PDF we want to scrape
url = 'http://www.liege.be/telechargements/pdf/vie-communale/carte-de-visite/liege-tableau-de-bord-population-2007.pdf'

# 3. Grab the file and convert it to an XML document we can work with
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)

# 4. Have a peek at the XML (click the "more" link in the Console to preview it).
print lxml.etree.tostring(root, pretty_print=True)

# 5. How many pages in the PDF document?
pages = list(root)
print "There are",len(pages),"pages"

# 6. Iterate through the elements in each page, and preview them
for page in pages:
    for el in page:
        if el.tag == "text":
            print el.text, el.attrib
exit(-1)
# REPLACE STEP 6 WITH THE FOLLOWING
# 7. We can use the positioning attibutes in the XML data to help us regenerate the rows and columns
for page in pages:
    for el in page:
        if el.tag == "text":
            if int(el.attrib['left']) < 100: print 'Country:', el.text,
            elif int(el.attrib['left']) < 250: print 'Factory name:', el.text,
            elif int(el.attrib['left']) < 500: print 'Address:', el.text,
            elif int(el.attrib['left']) < 1000: print 'City:', el.text,
            else:
                print 'Region:', el.text

# REPLACE STEP 7 WITH THE FOLLOWING
# 8. Rather than just printing out the data, we can generate and display a data structure representing each row.
#    We can also skip the first page, the title page that doesn't contain any of the tabulated information we're after.
for page in pages[1:]:
    for el in page:
        if el.tag == "text":
            if int(el.attrib['left']) < 100: data = { 'Country': el.text }
            elif int(el.attrib['left']) < 250: data['Factory name'] = el.text
            elif int(el.attrib['left']) < 500: data['Address'] = el.text
            elif int(el.attrib['left']) < 1000: data['City'] = el.text
            else:
                data['Region'] = el.text
                print data# 1. Add some necessary libraries
import scraperwiki
import urllib2, lxml.etree

# 2. The URL/web address where we can find the PDF we want to scrape
url = 'http://www.liege.be/telechargements/pdf/vie-communale/carte-de-visite/liege-tableau-de-bord-population-2007.pdf'

# 3. Grab the file and convert it to an XML document we can work with
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)

# 4. Have a peek at the XML (click the "more" link in the Console to preview it).
print lxml.etree.tostring(root, pretty_print=True)

# 5. How many pages in the PDF document?
pages = list(root)
print "There are",len(pages),"pages"

# 6. Iterate through the elements in each page, and preview them
for page in pages:
    for el in page:
        if el.tag == "text":
            print el.text, el.attrib
exit(-1)
# REPLACE STEP 6 WITH THE FOLLOWING
# 7. We can use the positioning attibutes in the XML data to help us regenerate the rows and columns
for page in pages:
    for el in page:
        if el.tag == "text":
            if int(el.attrib['left']) < 100: print 'Country:', el.text,
            elif int(el.attrib['left']) < 250: print 'Factory name:', el.text,
            elif int(el.attrib['left']) < 500: print 'Address:', el.text,
            elif int(el.attrib['left']) < 1000: print 'City:', el.text,
            else:
                print 'Region:', el.text

# REPLACE STEP 7 WITH THE FOLLOWING
# 8. Rather than just printing out the data, we can generate and display a data structure representing each row.
#    We can also skip the first page, the title page that doesn't contain any of the tabulated information we're after.
for page in pages[1:]:
    for el in page:
        if el.tag == "text":
            if int(el.attrib['left']) < 100: data = { 'Country': el.text }
            elif int(el.attrib['left']) < 250: data['Factory name'] = el.text
            elif int(el.attrib['left']) < 500: data['Address'] = el.text
            elif int(el.attrib['left']) < 1000: data['City'] = el.text
            else:
                data['Region'] = el.text
                print data