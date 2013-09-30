###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree

url = "https://sistemas.usp.br/anuario/tabelas/T02_10.pdf"
pdfdata = urllib2.urlopen(url).read()
print "Este PDF possui %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "Após ser convertido para xml ele ficou com %d bytes" % len(xmldata)
print "Os primeiros 2000 caracteres são: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "As páginas estão numeradas:", [ page.attrib.get("number")  for page in pages ]


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
    return "".join(res)

# print the first hundred text elements from the first page
page0 = pages[0]
for el in list(page)[:100]:
    if el.tag == "text":
        print el.attrib, gettext_with_bi_tags(el)


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

url = "https://sistemas.usp.br/anuario/tabelas/T02_10.pdf"
pdfdata = urllib2.urlopen(url).read()
print "Este PDF possui %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "Após ser convertido para xml ele ficou com %d bytes" % len(xmldata)
print "Os primeiros 2000 caracteres são: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "As páginas estão numeradas:", [ page.attrib.get("number")  for page in pages ]


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
    return "".join(res)

# print the first hundred text elements from the first page
page0 = pages[0]
for el in list(page)[:100]:
    if el.tag == "text":
        print el.attrib, gettext_with_bi_tags(el)


# If you have many PDF documents to extract data from, the trick is to find what's similar
# in the way that the information is presented in them in terms of the top left bottom right
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/

