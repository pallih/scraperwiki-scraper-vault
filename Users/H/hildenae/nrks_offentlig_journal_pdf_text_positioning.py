import scraperwiki, urllib2, datetime, base64, time, re
from bs4 import BeautifulSoup
from collections import deque
import scraperwiki
lazycache = scraperwiki.swimport('lazycache')
u = scraperwiki.swimport('hildenae_utils')

def d(text):
    if(False):
        print "DEBUG:", text

def process_pdf(pdfurl):
    pdfxml = u.findInCache(pdfurl,verbose=True) # look for html parse in cache
    if pdfxml is None: # a html parse is not cached
        pdfdata=lazycache.lazycache(pdfurl, verbose=True) # look for pdf document in cache, if not download
        pdfxml = scraperwiki.pdftoxml(pdfdata, "-hidden") # parse pdf text to html
        u.putInCache(pdfurl, pdfxml, verbose=True) # save cache of html parse

    beautifulxml = BeautifulSoup(pdfxml) # convert html to BeautifulSoup(4) object

    for page in beautifulxml.find_all('page'):
        FIRSTPAGE = 6
        LASTPAGE = 6
        if int(page['number']) < FIRSTPAGE:
            continue
        if int(page['number']) == FIRSTPAGE:
            print "*******************************************"
            print "***** FIRSTPAGE #%d while developing ******" % (FIRSTPAGE)
            print "*******************************************"
        if int(page['number']) == LASTPAGE+1: 
            print "*******************************************"
            print "****** LASTPAGE #%d while developing ******" % (LASTPAGE)
            print "*******************************************"
            break

        print( "*******************************************")
        print( "********** Working on page #%s **********" % page['number'])
        print( "*******************************************")
        elementList = deque(page.find_all('text')) # we want to be able to use popleft
        d(elementList)
        while True:
            try:
                currElement = elementList.popleft()
                if "Innhold:" in currElement.text and currElement.b: # we found a "Innhold:"-header
                    entry = parseDocumentRecord(currElement, elementList)
                    print entry
                    scraperwiki.sqlite.save(unique_keys=["innhold", "sakstittel"], data=entry)
                    d( "back in process_pdf")
                #else:
                    #print currElement.text
            except IndexError, e:
                d("No more text elements on page (%s)" % e)
                break



def parseDocumentRecord(currElement, elementList):
    # previous element in list is "Innhold:"
    d ("starting parseDocumentRecord")
    entry = {}
    while(True):
        try:
            d(elementList)
            if "Innhold:" in elementList[0].text: # look ahead, if next is "Innhold:" return to process_pdf
                break

            currElement = elementList.popleft() # first text in innhold
            entry["innhold"] = ""
            while(True):
                if "Sakstittel:" in currElement.text: # we found sakstittel, go to next
                    break
                entry["innhold"] += currElement.text
                currElement = elementList.popleft()
            entry["innhold"] = u.removeDoubleSpaces(entry["innhold"])

            currElement = elementList.popleft() # first text in sakstittel
            entry["sakstittel"] = ""
            while(True):
                if "DokType" in currElement.text: # we found DokType, go to next
                    break
                entry["sakstittel"] += currElement.text
                currElement = elementList.popleft()
            entry["sakstittel"] = u.removeDoubleSpaces(entry["sakstittel"])

            print("before spool to 'mottaker:'")

            '''



            Komments: Virker som om pdf2html noen ganger ikke klarer å lese DokType. Hittil er dette kun observert når
            DokType er U (selv om den klarer å lese noen DokType U). Dette er bekreftet mesteparten av 18 og 22 i juni



            '''
            print elementList



            print("spool to 'mottaker:'")
            currElement = elementList.popleft() # first text after DocType
            while(True):
                if re.search( r'[t].*[t].*[a].*[k].*[e].*[r].*[:]', currElement.text): # match "motta ker:" (some last pages - nooooot pretty)
                    d("found mottaker")
                    break
                currElement = elementList.popleft()

            d(elementList)

            entry["avsender_mottager"] = ""
            while(True):
                if ("Innhold:" in elementList[0].text) or ("Side:" in elementList[0].text): # ***look ahead***, if next is "Innhold:" return to process_pdf
                    #print "next is innhold, cleanup"
                    entry["avsender_mottager"] = u.removeDoubleSpaces(entry["avsender_mottager"])
                    if re.match("^[*]+$", entry["avsender_mottager"]):
                        entry["avsender_mottager"] = None
                    #print elementList
                    #print entry
                    d("finished with record")
                    break
                #print "Adding to avs_mot (%s)" % currElement.text
                entry["avsender_mottager"] += currElement.text
                currElement = elementList.popleft()

            #print "lastBreak"
            break # we are finished with this Innhold
        except IndexError, e:
            d("No more text elements on page (%s)" % e)
            break
    return entry

process_pdf("http://www.nrk.no/contentfile/file/1.8221353!offentlig22062012.pdf") # 4 records on last page
#process_pdf("http://www.nrk.no/contentfile/file/1.8217234!offentligjournal21062012.pdf") # 3 records on last page
#process_pdf("http://www.nrk.no/contentfile/file/1.8214156!offentligjournal20062012.pdf")
#process_pdf("http://www.nrk.no/contentfile/file/1.8212381!offentligjournal19062012.pdf")

# https://views.scraperwiki.com/run/pdf_to_html_preview_4/?url=http%3A%2F%2Fwww.nrk.no%2Fcontentfile%2Ffile%2F1.8209505%21offentligjournal18062012.pdf&hidden=1
#process_pdf("http://www.nrk.no/contentfile/file/1.8209505!offentligjournal18062012.pdf") # 1 record on last page


import scraperwiki, urllib2, datetime, base64, time, re
from bs4 import BeautifulSoup
from collections import deque
import scraperwiki
lazycache = scraperwiki.swimport('lazycache')
u = scraperwiki.swimport('hildenae_utils')

def d(text):
    if(False):
        print "DEBUG:", text

def process_pdf(pdfurl):
    pdfxml = u.findInCache(pdfurl,verbose=True) # look for html parse in cache
    if pdfxml is None: # a html parse is not cached
        pdfdata=lazycache.lazycache(pdfurl, verbose=True) # look for pdf document in cache, if not download
        pdfxml = scraperwiki.pdftoxml(pdfdata, "-hidden") # parse pdf text to html
        u.putInCache(pdfurl, pdfxml, verbose=True) # save cache of html parse

    beautifulxml = BeautifulSoup(pdfxml) # convert html to BeautifulSoup(4) object

    for page in beautifulxml.find_all('page'):
        FIRSTPAGE = 6
        LASTPAGE = 6
        if int(page['number']) < FIRSTPAGE:
            continue
        if int(page['number']) == FIRSTPAGE:
            print "*******************************************"
            print "***** FIRSTPAGE #%d while developing ******" % (FIRSTPAGE)
            print "*******************************************"
        if int(page['number']) == LASTPAGE+1: 
            print "*******************************************"
            print "****** LASTPAGE #%d while developing ******" % (LASTPAGE)
            print "*******************************************"
            break

        print( "*******************************************")
        print( "********** Working on page #%s **********" % page['number'])
        print( "*******************************************")
        elementList = deque(page.find_all('text')) # we want to be able to use popleft
        d(elementList)
        while True:
            try:
                currElement = elementList.popleft()
                if "Innhold:" in currElement.text and currElement.b: # we found a "Innhold:"-header
                    entry = parseDocumentRecord(currElement, elementList)
                    print entry
                    scraperwiki.sqlite.save(unique_keys=["innhold", "sakstittel"], data=entry)
                    d( "back in process_pdf")
                #else:
                    #print currElement.text
            except IndexError, e:
                d("No more text elements on page (%s)" % e)
                break



def parseDocumentRecord(currElement, elementList):
    # previous element in list is "Innhold:"
    d ("starting parseDocumentRecord")
    entry = {}
    while(True):
        try:
            d(elementList)
            if "Innhold:" in elementList[0].text: # look ahead, if next is "Innhold:" return to process_pdf
                break

            currElement = elementList.popleft() # first text in innhold
            entry["innhold"] = ""
            while(True):
                if "Sakstittel:" in currElement.text: # we found sakstittel, go to next
                    break
                entry["innhold"] += currElement.text
                currElement = elementList.popleft()
            entry["innhold"] = u.removeDoubleSpaces(entry["innhold"])

            currElement = elementList.popleft() # first text in sakstittel
            entry["sakstittel"] = ""
            while(True):
                if "DokType" in currElement.text: # we found DokType, go to next
                    break
                entry["sakstittel"] += currElement.text
                currElement = elementList.popleft()
            entry["sakstittel"] = u.removeDoubleSpaces(entry["sakstittel"])

            print("before spool to 'mottaker:'")

            '''



            Komments: Virker som om pdf2html noen ganger ikke klarer å lese DokType. Hittil er dette kun observert når
            DokType er U (selv om den klarer å lese noen DokType U). Dette er bekreftet mesteparten av 18 og 22 i juni



            '''
            print elementList



            print("spool to 'mottaker:'")
            currElement = elementList.popleft() # first text after DocType
            while(True):
                if re.search( r'[t].*[t].*[a].*[k].*[e].*[r].*[:]', currElement.text): # match "motta ker:" (some last pages - nooooot pretty)
                    d("found mottaker")
                    break
                currElement = elementList.popleft()

            d(elementList)

            entry["avsender_mottager"] = ""
            while(True):
                if ("Innhold:" in elementList[0].text) or ("Side:" in elementList[0].text): # ***look ahead***, if next is "Innhold:" return to process_pdf
                    #print "next is innhold, cleanup"
                    entry["avsender_mottager"] = u.removeDoubleSpaces(entry["avsender_mottager"])
                    if re.match("^[*]+$", entry["avsender_mottager"]):
                        entry["avsender_mottager"] = None
                    #print elementList
                    #print entry
                    d("finished with record")
                    break
                #print "Adding to avs_mot (%s)" % currElement.text
                entry["avsender_mottager"] += currElement.text
                currElement = elementList.popleft()

            #print "lastBreak"
            break # we are finished with this Innhold
        except IndexError, e:
            d("No more text elements on page (%s)" % e)
            break
    return entry

process_pdf("http://www.nrk.no/contentfile/file/1.8221353!offentlig22062012.pdf") # 4 records on last page
#process_pdf("http://www.nrk.no/contentfile/file/1.8217234!offentligjournal21062012.pdf") # 3 records on last page
#process_pdf("http://www.nrk.no/contentfile/file/1.8214156!offentligjournal20062012.pdf")
#process_pdf("http://www.nrk.no/contentfile/file/1.8212381!offentligjournal19062012.pdf")

# https://views.scraperwiki.com/run/pdf_to_html_preview_4/?url=http%3A%2F%2Fwww.nrk.no%2Fcontentfile%2Ffile%2F1.8209505%21offentligjournal18062012.pdf&hidden=1
#process_pdf("http://www.nrk.no/contentfile/file/1.8209505!offentligjournal18062012.pdf") # 1 record on last page


