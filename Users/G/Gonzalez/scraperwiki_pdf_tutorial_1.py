###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree
from BeautifulSoup import BeautifulSoup  

# Iterate through months and day
for y in range(13, 14):
    for m in range(1, 4):
        for d in range(1, 32):
            # Checck if already gone through month
            if (m == 2 and d> 28):
                break
            elif (m in [4, 6, 9, 11] and d >30):
                break
            # Open url
            timestamp = str(y) + str(m) + str(d)
            print "Getting data for " + timestamp
            url = "http://www.diputados.gob.mx/asistencias/inasistencias/" + str(d).zfill(2) + str(m).zfill(2) + str(y) + ".pdf"
            try:
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
                            scraperwiki.sqlite.save(["ID"],record)
                    return "".join(res)
                #print the first hundred text elements from the first page
                page0 = pages[0]
                ID = 0
                for el in list(page)[:150]:
                    print el.tag
                    if el.tag == "text":
                        print el.attrib, gettext_with_bi_tags(el)
                        record = {}
                        record["text"] = gettext_with_bi_tags(el)
                        ID = ID+1
                        record["ID"] = ID
                        scraperwiki.sqlite.save(["ID"],record)
                        print record
                

            except:
                pass



###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree
from BeautifulSoup import BeautifulSoup  

# Iterate through months and day
for y in range(13, 14):
    for m in range(1, 4):
        for d in range(1, 32):
            # Checck if already gone through month
            if (m == 2 and d> 28):
                break
            elif (m in [4, 6, 9, 11] and d >30):
                break
            # Open url
            timestamp = str(y) + str(m) + str(d)
            print "Getting data for " + timestamp
            url = "http://www.diputados.gob.mx/asistencias/inasistencias/" + str(d).zfill(2) + str(m).zfill(2) + str(y) + ".pdf"
            try:
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
                            scraperwiki.sqlite.save(["ID"],record)
                    return "".join(res)
                #print the first hundred text elements from the first page
                page0 = pages[0]
                ID = 0
                for el in list(page)[:150]:
                    print el.tag
                    if el.tag == "text":
                        print el.attrib, gettext_with_bi_tags(el)
                        record = {}
                        record["text"] = gettext_with_bi_tags(el)
                        ID = ID+1
                        record["ID"] = ID
                        scraperwiki.sqlite.save(["ID"],record)
                        print record
                

            except:
                pass



