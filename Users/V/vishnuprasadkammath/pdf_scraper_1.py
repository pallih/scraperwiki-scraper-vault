###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree

url = "https://dl.dropbox.com/u/268010/2800.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)
print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


## this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        #res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        #res.append("</%s>" % lel.tag)
        #if el.tail:
            #res.append(el.tail)
    return "".join(res)
row=[]
x=[]
for i in range(1000):
    x.append(i+1)
print x
# print the first hundred text elements from the first page
#page0 = pages[0]
i=0

for el in list(page)[:1000]:
    if el.tag == "text":
        row.append(gettext_with_bi_tags(el))
        print row
        
            scraperwiki.sqlite.save(unique_keys=["slno"], data={"slno":x[i],"1":row[0],}) #"2":row[1],})#"3":row[2],"4":row[3],"5":row[4],"6":row[5],"7":row[6],"8":row[7],"9":row[8]})
        row=[]
        i+=1
# If you have many PDF documents to extract data from, the trick is to find what's similar
# in the way that the information is presented in them in terms of the top left bottom right
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/




