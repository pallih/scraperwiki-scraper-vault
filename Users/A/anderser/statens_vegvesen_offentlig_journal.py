import scraperwiki
import lxml.html
import datetime

#uncomment to run for a selected timeperiod
#fromdate = "01.04.2011"
#todate = "21.05.2011"

#fromdate = datetime.datetime.strptime(fromdate, "%d.%m.%Y")
#todate = datetime.datetime.strptime(todate, "%d.%m.%Y")
#adday = datetime.timedelta(days=1)

def scrapepage(mydate):
    
    formatteddate = mydate.strftime("%d.%m.%Y")
    #formatteddate = "10.05.2011"

    url = "http://www.vegvesen.no/Om+Statens+vegvesen/Aktuelt/Offentlig+journal?dokumenttyper=&dato=%s&journalenhet=6&utforSok=S%%C3%%B8k&submitButton=S%%C3%%B8k" % formatteddate
    
    root = lxml.html.parse(url).getroot()
    
    divs = root.cssselect("div.treff")
    
    for p in divs:
        
        dateandtype = p.xpath("p/text()")[0].split(" ")
        saksdetaljer = p.xpath("ul[@class='saksdetaljer']/li/text()")
    
        
        record = { 
                    "doknr": dateandtype[0],
                    "innut": dateandtype[2],
                    "tittel": p.xpath("h2/text()")[0],
                    "sak": p.xpath("span[@class='sak']")[0].text[6:],
                    "fratil": p.xpath("ul[@class='fraTil']/li/text()")[0][5:],
                }
    
        record.update(dict([x.split(":") for x in saksdetaljer]))

        record['Dokumenttdato'] = datetime.datetime.strptime(record['Dokumenttdato'].strip(), "%d.%m.%Y").date()
        record['Journaldato'] = datetime.datetime.strptime(record['Journaldato'].strip(), "%d.%m.%Y").date()
 
        scraperwiki.sqlite.save(unique_keys=["doknr"], data=record)

#uncomment to run for a selected timeperiod
#thedate = fromdate
#while thedate <= todate:
#    print thedate
#    thedate = thedate + adday
#    scrapepage(thedate)
#comment out these two lines in order to run for a selected timeperiod
thedate = datetime.datetime.now()
print thedate

scrapepage(thedate)
    import scraperwiki
import lxml.html
import datetime

#uncomment to run for a selected timeperiod
#fromdate = "01.04.2011"
#todate = "21.05.2011"

#fromdate = datetime.datetime.strptime(fromdate, "%d.%m.%Y")
#todate = datetime.datetime.strptime(todate, "%d.%m.%Y")
#adday = datetime.timedelta(days=1)

def scrapepage(mydate):
    
    formatteddate = mydate.strftime("%d.%m.%Y")
    #formatteddate = "10.05.2011"

    url = "http://www.vegvesen.no/Om+Statens+vegvesen/Aktuelt/Offentlig+journal?dokumenttyper=&dato=%s&journalenhet=6&utforSok=S%%C3%%B8k&submitButton=S%%C3%%B8k" % formatteddate
    
    root = lxml.html.parse(url).getroot()
    
    divs = root.cssselect("div.treff")
    
    for p in divs:
        
        dateandtype = p.xpath("p/text()")[0].split(" ")
        saksdetaljer = p.xpath("ul[@class='saksdetaljer']/li/text()")
    
        
        record = { 
                    "doknr": dateandtype[0],
                    "innut": dateandtype[2],
                    "tittel": p.xpath("h2/text()")[0],
                    "sak": p.xpath("span[@class='sak']")[0].text[6:],
                    "fratil": p.xpath("ul[@class='fraTil']/li/text()")[0][5:],
                }
    
        record.update(dict([x.split(":") for x in saksdetaljer]))

        record['Dokumenttdato'] = datetime.datetime.strptime(record['Dokumenttdato'].strip(), "%d.%m.%Y").date()
        record['Journaldato'] = datetime.datetime.strptime(record['Journaldato'].strip(), "%d.%m.%Y").date()
 
        scraperwiki.sqlite.save(unique_keys=["doknr"], data=record)

#uncomment to run for a selected timeperiod
#thedate = fromdate
#while thedate <= todate:
#    print thedate
#    thedate = thedate + adday
#    scrapepage(thedate)
#comment out these two lines in order to run for a selected timeperiod
thedate = datetime.datetime.now()
print thedate

scrapepage(thedate)
    