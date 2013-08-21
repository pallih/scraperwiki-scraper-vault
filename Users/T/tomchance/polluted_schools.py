###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree
from BeautifulSoup import BeautifulSoup, Tag, NavigableString


url = "http://www.cleanairinlondon.org/_attachments/4842298/CAL%20139%20Update_%202270%20schools%20within%20400%20metres%20of%20London%20roads%20carrying%20over%2010000%20vpd_alphabetical%20order%20and%20searchable.pdf"
pdfdata = urllib2.urlopen(url).read()

xmldata = scraperwiki.pdftoxml(pdfdata)
soup = BeautifulSoup(xmldata)
soupy_data = soup.findAll('text')

for row in soupy_data:
    if (row['left'] == 94):
        print row['text']

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
    return "".join(res)

# print the first hundred text elements from the first page
#page0 = pages[0]
#for el in list(page)[:100]:
#    if el.tag == "text":
#        print el.attrib['left'], gettext_with_bi_tags(el)