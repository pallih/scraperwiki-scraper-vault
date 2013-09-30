###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree

url = "http://www.portdebarcelona.cat/cntmng/d/d/workspace/SpacesStore/182864f6-1471-4e38-8dd1-8fed6a3e2766/en.13.01b.pdf"
pdfdata = urllib2.urlopen(url).read()

xmldata = scraperwiki.pdftoxml(pdfdata)

root = lxml.etree.fromstring(xmldata)
pages = list(root)

[ page.attrib.get("number")  for page in pages ]


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
data = [ ]
boat = ""
date = ""
for el in list(page)[:100]:
    if el.tag == "text":
        left = el.attrib['left']
        if el.attrib['left'] > '400' and el.attrib['left'] < '500':
            boat = gettext_with_bi_tags(el)
        if el.attrib['left'] == '832':
            date = gettext_with_bi_tags(el)
            info = {
                'boat' : boat,
                'date' : date
            }
            data.append(info)

print data
scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1, "data":data})

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

url = "http://www.portdebarcelona.cat/cntmng/d/d/workspace/SpacesStore/182864f6-1471-4e38-8dd1-8fed6a3e2766/en.13.01b.pdf"
pdfdata = urllib2.urlopen(url).read()

xmldata = scraperwiki.pdftoxml(pdfdata)

root = lxml.etree.fromstring(xmldata)
pages = list(root)

[ page.attrib.get("number")  for page in pages ]


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
data = [ ]
boat = ""
date = ""
for el in list(page)[:100]:
    if el.tag == "text":
        left = el.attrib['left']
        if el.attrib['left'] > '400' and el.attrib['left'] < '500':
            boat = gettext_with_bi_tags(el)
        if el.attrib['left'] == '832':
            date = gettext_with_bi_tags(el)
            info = {
                'boat' : boat,
                'date' : date
            }
            data.append(info)

print data
scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1, "data":data})

# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/

