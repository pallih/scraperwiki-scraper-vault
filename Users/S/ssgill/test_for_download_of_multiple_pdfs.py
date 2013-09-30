###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree
dlset = range(3)
calcnum = 0
url1 = "http://www.madingley.org/uploaded/Hansard_08.07.201"
url3 = ".pdf"
counter = 1
for x in dlset:
    if counter == 1:
        calcnum = 0
    else:
        calcnum +=1
    counter +=1
    url2 = str(calcnum)
    print url1 + url2+url3
    url = url1 + url2 + url3
    #url = "http://www.madingley.org/uploaded/Hansard_08.07.2010.pdf"
    print calcnum
    try:
        pdfdata = urllib2.urlopen(url).read()
        print "The pdf file has %d bytes" % len(pdfdata)
    except:
        print "ERROR FILE NOT FOUND!!!!!!!!!!"
    xmldata = scraperwiki.pdftoxml(pdfdata)
    print "After converting to xml it has %d bytes" % len(xmldata)
#    xmldata.write("sgtest123.xml","w")
    f = open('sgdoctest123.pdf', 'w') # Save it locallyBack to scraper overview
    f.write(pdfdata)
    f.close()

#print "The first 2000 characters are: ", xmldata[:2000]

#root = lxml.etree.fromstring(xmldata)
#pages = list(root)

#print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
#def gettext_with_bi_tags(el):
#    res = [ ]
#    if el.text:
#        res.append(el.text)
#    for lel in el:
#        res.append("<%s>" % lel.tag)
#        res.append(gettext_with_bi_tags(lel))
#        res.append("</%s>" % lel.tag)
 #       if el.tail:
#            res.append(el.tail)
#    return "".join(res)

# print the first hundred text elements from the first page
#page0 = pages[0]
#for el in list(page)[:100]:
#    if el.tag == "text":
#        print el.attrib, gettext_with_bi_tags(el)


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
dlset = range(3)
calcnum = 0
url1 = "http://www.madingley.org/uploaded/Hansard_08.07.201"
url3 = ".pdf"
counter = 1
for x in dlset:
    if counter == 1:
        calcnum = 0
    else:
        calcnum +=1
    counter +=1
    url2 = str(calcnum)
    print url1 + url2+url3
    url = url1 + url2 + url3
    #url = "http://www.madingley.org/uploaded/Hansard_08.07.2010.pdf"
    print calcnum
    try:
        pdfdata = urllib2.urlopen(url).read()
        print "The pdf file has %d bytes" % len(pdfdata)
    except:
        print "ERROR FILE NOT FOUND!!!!!!!!!!"
    xmldata = scraperwiki.pdftoxml(pdfdata)
    print "After converting to xml it has %d bytes" % len(xmldata)
#    xmldata.write("sgtest123.xml","w")
    f = open('sgdoctest123.pdf', 'w') # Save it locallyBack to scraper overview
    f.write(pdfdata)
    f.close()

#print "The first 2000 characters are: ", xmldata[:2000]

#root = lxml.etree.fromstring(xmldata)
#pages = list(root)

#print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
#def gettext_with_bi_tags(el):
#    res = [ ]
#    if el.text:
#        res.append(el.text)
#    for lel in el:
#        res.append("<%s>" % lel.tag)
#        res.append(gettext_with_bi_tags(lel))
#        res.append("</%s>" % lel.tag)
 #       if el.tail:
#            res.append(el.tail)
#    return "".join(res)

# print the first hundred text elements from the first page
#page0 = pages[0]
#for el in list(page)[:100]:
#    if el.tag == "text":
#        print el.attrib, gettext_with_bi_tags(el)


# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/

