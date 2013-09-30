import scraperwiki
import lxml.html
import datetime

html = scraperwiki.scrape("http://www.mehr-demokratie.de/volkentscheide-in-deutschland.html")
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[class='contenttable contenttable-0'] tr"):
    tds = tr.cssselect("td")
    tds = [td.text_content().encode('utf-8').replace("&quot;", "") for td in tds]
    if len(tds)>1:
        data = {'Nr' : tds[0],'Datum VE' : tds[1], 'Bundesland' : tds[2],'Titel' : tds[3] , 'Initiatoren' :  tds[4], 'Unterstuetzer' : tds[5], 'Erfolg-formal' : tds[6], 'Erfolg-faktisch' : tds[7],'Nachgeschichte' : tds[8]}
        tempdate=data['Datum VE'].split('.')
        data['Datum VE']=datetime.date(int(tempdate[2]),int(tempdate[1]),int(tempdate[0]))
        #print data['Datum VE']

        #print data
        scraperwiki.sqlite.save(['Bundesland','Titel'], data)import scraperwiki
import lxml.html
import datetime

html = scraperwiki.scrape("http://www.mehr-demokratie.de/volkentscheide-in-deutschland.html")
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[class='contenttable contenttable-0'] tr"):
    tds = tr.cssselect("td")
    tds = [td.text_content().encode('utf-8').replace("&quot;", "") for td in tds]
    if len(tds)>1:
        data = {'Nr' : tds[0],'Datum VE' : tds[1], 'Bundesland' : tds[2],'Titel' : tds[3] , 'Initiatoren' :  tds[4], 'Unterstuetzer' : tds[5], 'Erfolg-formal' : tds[6], 'Erfolg-faktisch' : tds[7],'Nachgeschichte' : tds[8]}
        tempdate=data['Datum VE'].split('.')
        data['Datum VE']=datetime.date(int(tempdate[2]),int(tempdate[1]),int(tempdate[0]))
        #print data['Datum VE']

        #print data
        scraperwiki.sqlite.save(['Bundesland','Titel'], data)