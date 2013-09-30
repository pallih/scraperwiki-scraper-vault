# ---------------------------------------------------------------------------
# Since October 1st 2010 all Ministries and Prefectures of Greece 
# are obliged to publicize their resolutions and acts, 
# through the "DIAVGEIA" programme of the Ministry of Interior.
# This collects all such publications from 
# their site http://diavgeia.gov.gr/
# There are some issues with the original data 
# (consistency, cleanliness, lack of explanation etc) but overall it might 
# be very usefull for analyzing the workings of the government.
# If you do something with this please write something 
# in the discussion section.
# ---------------------------------------------------------------------------

#20101008 added Στοιχεία ΦΕΚ label/ fek column

import scraperwiki
import datetime
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup


def get_links (rssurl):
    rss = scraperwiki.scrape(rssurl)
    rsssoup = BeautifulStoneSoup(rss)
    #print rss
    #print rsssoup.prettify()
    myitems = rsssoup.findAll('link')
    #print myitems
    for eachitem in myitems:
        thelinks.append(eachitem.text)
    thelinks.remove('http://et.diavgeia.gov.gr/f/all/rss') # remove top channel link hich is not useful

    

# ---------------------------------------------------------------------------
# START HERE: define the Diavgeia RSS URL - then
# call a function to get all links from the rss
# ---------------------------------------------------------------------------
rssurl = 'http://et.diavgeia.gov.gr/f/all/rss'
thelinks = []
get_links(rssurl)
#print thelinks

#process each item
for link in thelinks:
    print link
    html = scraperwiki.scrape(link.encode('utf-8'))
    soup = BeautifulSoup(html)
    #print soup.prettify()
    # so far so good
    myitems = soup.find('div', id="content").findAll('li')
    record = {}
    theDate = ""
    for theitem in myitems:    
        span = theitem.span
        #print span
        if span:
            if span.text == "ΑΔΑ".decode('utf8') :
                span.extract() # remove <span></span>
                content = theitem.text
                #print content
                #print '<ada>' + content + '</ada>'
                record["ada"] = content
            elif span.text == "Αριθμός Πρωτοκόλου".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<identifier>' + theitem.text + '</identifier>'
                record['identifier'] = theitem.text
            elif span.text == "Θέμα".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<subject>' + theitem.text + '</subject>'
                record['subject'] = theitem.text
            elif span.text == "Στοιχεία ΦΕΚ".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<fek>' + theitem.text + '</fek>'
                record['fek'] = theitem.text
            elif span.text == "Ημερομηνία Απόφασης".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<created>' + theitem.text + '</created>'
                datestring=theitem.text
                day = int(datestring[:2])
                month = int(datestring[3:5])
                year = int (datestring[6:10])
                try:
                    theDate = datetime.datetime(year,month,day)
                    #print theDate
                    record['created'] = theDate
                except:
                    print 'Wrongly formatted Ημερομηνία Απόφασης' 

            elif span.text == "Ημερομηνία Ανάρτησης".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<dateAccepted>' + theitem.text + '</dateAccepted>'
                #record['dateAccepted'] = theitem.text
                datestring=theitem.text
                day = int(datestring[:2])
                month = int(datestring[3:5])
                year = int (datestring[6:10])
                hour = int(datestring[11:13])
                #print hour
                minute = int(datestring[14:16])
                #print minute
                second = int (datestring[17:19])
                #print second
                theDateUp = datetime.datetime(year,month,day,hour,minute,second)
                #print theDateUp
                record['dateAccepted'] = theDateUp               
            elif span.text == "Φορέας".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<publisher>' + theitem.text + '</publisher>'
                record['publisher'] = theitem.text
            elif span.text == "Τελικός Υπογράφων".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<signee>' + theitem.text + '</signee>'
                record['signee'] = theitem.text
            elif span.text == "Είδος Απόφασης".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<type>' + theitem.text + '</type>'
                record['type'] = theitem.text
            elif span.text == "Μονάδα".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<unit>' + theitem.text + '</unit>'
                record['unit'] = theitem.text
            elif span.text == "Θεματική".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<category>' + theitem.text + '</category>'
                record['category'] = theitem.text
            elif span.text == "Αρχείο".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<doclink>' + theitem.find('a')['href'] + '</doclink>'
                #print theitem.find('a')['href']
                record['doclink'] = theitem.find('a')['href']
            elif span.text == "ΠΟΣΟ ΔΑΠΑΝΗΣ / ΣΥΝΑΛΛΑΓΗΣ (ΜΕ ΦΠΑ)".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<amount>' + theitem.text + '</amount>'
                record['amount'] = theitem.text
            elif span.text == "ΑΦΜ Φορέα".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<publisherTaxCode>' + theitem.text + '</publisherTaxCode>'
                record['publisherTaxCode'] = theitem.text
            elif span.text == "ΕΠΩΝΥΜΙΑ ΦΟΡΕΑ".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<publisherName>' + theitem.text + '</publisherName>'
                record['publisherName'] = theitem.text
            elif span.text == "ΑΦΜ Αναδόχου".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<contractorTaxCode>' + theitem.text + '</contractorTaxCode>'
                record['contractorTaxCode'] = theitem.text
            elif span.text == "ΕΠΩΝΥΜΙΑ ΑΝΑΔΟΧΟΥ".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<contractorName>' + theitem.text + '</contractorName>'
                record['contractorName'] = theitem.text                
            elif span.text == "Περιγραφή Αντικειμένου".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<contractDescription>' + theitem.text + '</contractDescription>'
                record['contractDescription'] = theitem.text                
            elif span.text == "ΕΠΩΝΥΜΙΑ ΑΝΑΔΟΧΟΥ".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<contractorName>' + theitem.text + '</contractorName>'
                record['contractorName'] = theitem.text                            
    #print record 
    if (isinstance(theDate, datetime.datetime)):
        scraperwiki.datastore.save(['ada'], record, theDate)
    else:
        scraperwiki.datastore.save(['ada'], record) # in case wrong or no date input for "Ημερομηνία Απόφασης"
            
            


            

# ---------------------------------------------------------------------------
# Since October 1st 2010 all Ministries and Prefectures of Greece 
# are obliged to publicize their resolutions and acts, 
# through the "DIAVGEIA" programme of the Ministry of Interior.
# This collects all such publications from 
# their site http://diavgeia.gov.gr/
# There are some issues with the original data 
# (consistency, cleanliness, lack of explanation etc) but overall it might 
# be very usefull for analyzing the workings of the government.
# If you do something with this please write something 
# in the discussion section.
# ---------------------------------------------------------------------------

#20101008 added Στοιχεία ΦΕΚ label/ fek column

import scraperwiki
import datetime
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup


def get_links (rssurl):
    rss = scraperwiki.scrape(rssurl)
    rsssoup = BeautifulStoneSoup(rss)
    #print rss
    #print rsssoup.prettify()
    myitems = rsssoup.findAll('link')
    #print myitems
    for eachitem in myitems:
        thelinks.append(eachitem.text)
    thelinks.remove('http://et.diavgeia.gov.gr/f/all/rss') # remove top channel link hich is not useful

    

# ---------------------------------------------------------------------------
# START HERE: define the Diavgeia RSS URL - then
# call a function to get all links from the rss
# ---------------------------------------------------------------------------
rssurl = 'http://et.diavgeia.gov.gr/f/all/rss'
thelinks = []
get_links(rssurl)
#print thelinks

#process each item
for link in thelinks:
    print link
    html = scraperwiki.scrape(link.encode('utf-8'))
    soup = BeautifulSoup(html)
    #print soup.prettify()
    # so far so good
    myitems = soup.find('div', id="content").findAll('li')
    record = {}
    theDate = ""
    for theitem in myitems:    
        span = theitem.span
        #print span
        if span:
            if span.text == "ΑΔΑ".decode('utf8') :
                span.extract() # remove <span></span>
                content = theitem.text
                #print content
                #print '<ada>' + content + '</ada>'
                record["ada"] = content
            elif span.text == "Αριθμός Πρωτοκόλου".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<identifier>' + theitem.text + '</identifier>'
                record['identifier'] = theitem.text
            elif span.text == "Θέμα".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<subject>' + theitem.text + '</subject>'
                record['subject'] = theitem.text
            elif span.text == "Στοιχεία ΦΕΚ".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<fek>' + theitem.text + '</fek>'
                record['fek'] = theitem.text
            elif span.text == "Ημερομηνία Απόφασης".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<created>' + theitem.text + '</created>'
                datestring=theitem.text
                day = int(datestring[:2])
                month = int(datestring[3:5])
                year = int (datestring[6:10])
                try:
                    theDate = datetime.datetime(year,month,day)
                    #print theDate
                    record['created'] = theDate
                except:
                    print 'Wrongly formatted Ημερομηνία Απόφασης' 

            elif span.text == "Ημερομηνία Ανάρτησης".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<dateAccepted>' + theitem.text + '</dateAccepted>'
                #record['dateAccepted'] = theitem.text
                datestring=theitem.text
                day = int(datestring[:2])
                month = int(datestring[3:5])
                year = int (datestring[6:10])
                hour = int(datestring[11:13])
                #print hour
                minute = int(datestring[14:16])
                #print minute
                second = int (datestring[17:19])
                #print second
                theDateUp = datetime.datetime(year,month,day,hour,minute,second)
                #print theDateUp
                record['dateAccepted'] = theDateUp               
            elif span.text == "Φορέας".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<publisher>' + theitem.text + '</publisher>'
                record['publisher'] = theitem.text
            elif span.text == "Τελικός Υπογράφων".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<signee>' + theitem.text + '</signee>'
                record['signee'] = theitem.text
            elif span.text == "Είδος Απόφασης".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<type>' + theitem.text + '</type>'
                record['type'] = theitem.text
            elif span.text == "Μονάδα".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<unit>' + theitem.text + '</unit>'
                record['unit'] = theitem.text
            elif span.text == "Θεματική".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<category>' + theitem.text + '</category>'
                record['category'] = theitem.text
            elif span.text == "Αρχείο".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<doclink>' + theitem.find('a')['href'] + '</doclink>'
                #print theitem.find('a')['href']
                record['doclink'] = theitem.find('a')['href']
            elif span.text == "ΠΟΣΟ ΔΑΠΑΝΗΣ / ΣΥΝΑΛΛΑΓΗΣ (ΜΕ ΦΠΑ)".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<amount>' + theitem.text + '</amount>'
                record['amount'] = theitem.text
            elif span.text == "ΑΦΜ Φορέα".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<publisherTaxCode>' + theitem.text + '</publisherTaxCode>'
                record['publisherTaxCode'] = theitem.text
            elif span.text == "ΕΠΩΝΥΜΙΑ ΦΟΡΕΑ".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<publisherName>' + theitem.text + '</publisherName>'
                record['publisherName'] = theitem.text
            elif span.text == "ΑΦΜ Αναδόχου".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<contractorTaxCode>' + theitem.text + '</contractorTaxCode>'
                record['contractorTaxCode'] = theitem.text
            elif span.text == "ΕΠΩΝΥΜΙΑ ΑΝΑΔΟΧΟΥ".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<contractorName>' + theitem.text + '</contractorName>'
                record['contractorName'] = theitem.text                
            elif span.text == "Περιγραφή Αντικειμένου".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<contractDescription>' + theitem.text + '</contractDescription>'
                record['contractDescription'] = theitem.text                
            elif span.text == "ΕΠΩΝΥΜΙΑ ΑΝΑΔΟΧΟΥ".decode('utf8') :
                span.extract() # remove <span></span>
                #print '<contractorName>' + theitem.text + '</contractorName>'
                record['contractorName'] = theitem.text                            
    #print record 
    if (isinstance(theDate, datetime.datetime)):
        scraperwiki.datastore.save(['ada'], record, theDate)
    else:
        scraperwiki.datastore.save(['ada'], record) # in case wrong or no date input for "Ημερομηνία Απόφασης"
            
            


            

