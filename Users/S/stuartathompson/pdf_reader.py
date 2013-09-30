###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree

url = "http://www.tbs-sct.gc.ca/est-pre/20122013/me-bpd/docs/me-bpd-eng.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return res

# print the first hundred text elements from the first page
page0 = pages[24]
output = []
for x in range(26,27): #33):
    i = 0
    data = []
    for el in list(pages[x]):
        if el.tag == "text":
            top = el.attrib['top'] #, gettext_with_bi_tags(el)
            if data == []:
                #first element, so adding to array
                cell = {
                    'top':top,
                    'text':el.text
                }
                data.append(cell)
                print data
                i = i + 1
            # if this el.top = the last entry data.top, join together since they're on the same line
            elif top == data[i-1]['top']:
                data[i-1]['text'] = str(data[i-1]['text']).encode('latin-1', 'ignore') + ',' + str(el.text)
                print 'same data'
                print data[i-1]
            else:
                cell = {
                    'top':top,
                    'text':el.text
                }
                data.append(cell)
                print data
                i = i + 1
    print data


# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/

###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree

url = "http://www.tbs-sct.gc.ca/est-pre/20122013/me-bpd/docs/me-bpd-eng.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return res

# print the first hundred text elements from the first page
page0 = pages[24]
output = []
for x in range(26,27): #33):
    i = 0
    data = []
    for el in list(pages[x]):
        if el.tag == "text":
            top = el.attrib['top'] #, gettext_with_bi_tags(el)
            if data == []:
                #first element, so adding to array
                cell = {
                    'top':top,
                    'text':el.text
                }
                data.append(cell)
                print data
                i = i + 1
            # if this el.top = the last entry data.top, join together since they're on the same line
            elif top == data[i-1]['top']:
                data[i-1]['text'] = str(data[i-1]['text']).encode('latin-1', 'ignore') + ',' + str(el.text)
                print 'same data'
                print data[i-1]
            else:
                cell = {
                    'top':top,
                    'text':el.text
                }
                data.append(cell)
                print data
                i = i + 1
    print data


# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/

