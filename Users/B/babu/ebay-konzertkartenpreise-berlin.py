from BeautifulSoup import BeautifulSoup
import urllib2
import json
import re
import scraperwiki
import time 
from datetime import date

offset=0
 
scraperwiki.metadata.save('data_columns', ['id','venue', 'title', 'concertDate', 'price', 'buyingDate', 'veryfiedSale'])

host = "http://api.scraperwiki.com/api/1.0/datastore/getdata?format=json&name=konzertkarten-preise-berlin-ebay&limit=500&offset=861" #
req = urllib2.Request(host)
response_stream = urllib2.urlopen(req)

response = json.load(response_stream)
#print response -> []

c = 0
for dataset in response :
    
    c = c+1
    print c
    #dataset["id"] = "310286088249";
    print dataset["id"]
    
    host2 = ("http://api.scraperwiki.com/api/1.0/datastore/search?format=json&name=ebay-konzertkartenpreise-berlin&filter=id,"+dataset["id"])
    req2 = urllib2.Request(host2)
    response_stream2 = urllib2.urlopen(req2)
    response2 = json.load(response_stream2)

    #print len(response2)
    if len(response2) == 0 :
    
        website = scraperwiki.scrape("http://cgi.ebay.de/"+dataset["id"])
        
        soup = BeautifulSoup(website)
    
        end = False
        #if website.find("Dieses Angebot wurde beendet.") != -1 :
        #    end = True
    
        title = soup.find("h1").string 
        print title
        
        amount = soup.find("td",text="Anzahl: ")
        if amount != None :
            amount = amount.parent.nextSibling.string
        #print amount
        
        price = soup.find("th","vi-is1-lblp vi-is1-solidBg").nextSibling.span.span.string
        if price == None :
            price = str(soup.find("th","vi-is1-lblp vi-is1-solidBg").nextSibling.span.span).split("EUR</font>")[1].split("</span>")[0]
        else : price = price[4:]
        price = price.replace(".","").replace(",",".")
        if amount != "--" and amount != None : price = str(float(price)/float(amount))
        #print price
        
        year = soup.find("th",text="Jahr: ")
        if year != None :
            year = year.parent.nextSibling.string
        #print year
        m = soup.find("td",text="Monat: ")
        if m != None :
            m = m.parent.nextSibling.text.strip()
        
        
        month_names = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September",  "Oktober", "November", "Dezember"]
           
        if m != "--" and m != None : 
            month = month_names.index(m.encode("utf-8")) + 1
            #print month
            day = soup.find("td",text="Tag: ")
            if day != None :
                day = day.parent.nextSibling.string
            #print day
            if day != "--" or year != "--"  : d = date(int(year),int(month),int(day)).isoformat()
        
        city = soup.find("td",text="Stadt: ")
        #print city
        if city != None :
            city = city.parent.nextSibling.string
        
        venue = soup.find("td",text="Veranstaltungsort: ")
        #print venue
        if venue != None :
             venue = venue.parent.nextSibling.string
      
        endTime = soup.find("td",text="Beendet:")
        if soup.find("td",text="Beendet:") != None : 
            endTime = endTime.parent.nextSibling.span.span.string + " - " + endTime.parent.nextSibling.span.span.nextSibling.string
            end = True
            #print endTime
    
        record = {}
        if city == "Berlin" and end == True and amount != None:
            record['id'] = dataset["id"]
            #print ("TITLE: "+title)
            record['title'] = title
            if venue != None : print ("VENUE: "+venue)
            record['venue'] = venue
            print("PRICE: "+price)
            record['price'] = price
            print(d)
            record['concertDate'] = d
            print("END TIME: "+endTime)
            record['buyingDate'] = endTime
            scraperwiki.datastore.save(["id"], record)
    
        # datum, preis, ort, veranstaltung, verkaufsdatum
    
        #WURDE WIRKLICH ETWAS ZU DIESEM PREIS GEKAUFT?
    
        #print ("FINISHED YET: " + str(end))
    
        print("----")
