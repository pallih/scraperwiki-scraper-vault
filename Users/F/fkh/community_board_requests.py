###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree
import csv

data = scraperwiki.scrape("https://dl.dropbox.com/u/16744353/cbrboro6_12-selected_1.csv")

reader = csv.reader(data.splitlines())

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#output = {"request": "AAA", "preamble": "pream", "request": "req", "response": "respon"}

#requests = {"reqitem": output}

boardunique = ""
requestid = ""
request = ""
response = ""
preamble = ""

for row in reader:
    if row[0] is not "":

        # we have a new record to store!
        requestid = row[0]
        if is_number(requestid): # then it's a request id

            #report what we have
            print boardunique, " -- ", requestid, " REQUEST: ", request, "RESPONSE: ", response, " PREAMBLE: ", preamble
    
            #clean up
            boardunique = ""
            requestid = ""
            request = ""
            response = ""
            preamble = ""

            requestid = row[0]
            boardunique = row[1]
            request = row[2]
            response = row[3]
    else:
        request += " "
        request += row[2]
        response += " "
        response += row[3]
        preamble += row[0]
        preamble += " " 
        preamble += row[1]
        

quit()


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        #res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        #res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

url = "https://dl.dropbox.com/u/16744353/cbrboro6_12-selected%201.pdf"
pdfdata = urllib2.urlopen(url).read()
#print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
#print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 4000 characters are: ", xmldata[:4000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

for page in pages:
    pagenumber=int(page.attrib.get("number"))
    print "page", pagenumber

    for textchunk in page.xpath('text')[0:20]:
        leftcoord = int(textchunk.attrib.get('left'))
        topcoord = int(textchunk.attrib.get('top'))
        print topcoord, leftcoord, gettext_with_bi_tags(textchunk) 
        # print topcoord, leftcoord, gettext_with_bi_tags(textchunk)

quit()

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]




# print the first hundred text elements from the first page
page0 = pages[0]

for el in list(page)[:100]:
#    if el.tag == "text":
     print el.attrib, el.text #, gettext_with_bi_tags(el)
    
    
# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/

