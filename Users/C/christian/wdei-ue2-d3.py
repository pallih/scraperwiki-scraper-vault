# This scraper fetches the OSCARS 2012 lists in PDF format and outputs
# all nominated movies. Nominated persons and categories are left out.

import scraperwiki
import urllib2
import lxml.etree

# fetch the oscars 2012 nominees list in pdf format
url = "http://a.oscar.go.com/media/2012/pdf/nominees.pdf"

# read pdf and convert to xmldata
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
# DEBUG: print "First 2000 characters: ", xmldata[:2000]

# define root and create list of page elements
root = lxml.etree.fromstring(xmldata)
pages = list(root)

# first count the pages
pagecount = 0
for page in pages:
 pagecount = pagecount + 1
print "There are " + str(pagecount) + " pages in the nominee list."

# this function has to work recursively
def gettext_with_bi_tags(el):
    res = [ ]
    # do this for text elements
    if el.text:
        res.append(el.text)
    for lel in el:
        # adding the tags before and after is necessary to detect the movie names - they are in bold
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

# print the first hundred text elements from a page
for page in pages:
 for el in list(page)[:100]:
  if el.tag == "text":
   if (gettext_with_bi_tags(el)).startswith("<b>"):
    print (gettext_with_bi_tags(el)).upper()

# This scraper fetches the OSCARS 2012 lists in PDF format and outputs
# all nominated movies. Nominated persons and categories are left out.

import scraperwiki
import urllib2
import lxml.etree

# fetch the oscars 2012 nominees list in pdf format
url = "http://a.oscar.go.com/media/2012/pdf/nominees.pdf"

# read pdf and convert to xmldata
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
# DEBUG: print "First 2000 characters: ", xmldata[:2000]

# define root and create list of page elements
root = lxml.etree.fromstring(xmldata)
pages = list(root)

# first count the pages
pagecount = 0
for page in pages:
 pagecount = pagecount + 1
print "There are " + str(pagecount) + " pages in the nominee list."

# this function has to work recursively
def gettext_with_bi_tags(el):
    res = [ ]
    # do this for text elements
    if el.text:
        res.append(el.text)
    for lel in el:
        # adding the tags before and after is necessary to detect the movie names - they are in bold
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

# print the first hundred text elements from a page
for page in pages:
 for el in list(page)[:100]:
  if el.tag == "text":
   if (gettext_with_bi_tags(el)).startswith("<b>"):
    print (gettext_with_bi_tags(el)).upper()

