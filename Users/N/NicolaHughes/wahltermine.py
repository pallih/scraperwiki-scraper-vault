import scraperwiki
import lxml.html
import re
import datetime

html = scraperwiki.scrape("http://www.wahlrecht.de/termine.htm")
root = lxml.html.fromstring(html)

months = [u"Januar", u"Februar", u"M\xe4rz", u"April", u"Mai", u"Juni", u"Juli", u"August", u"September", u"Oktober", u"November", u"Dezember"]
months
def convertdate(d):
    
    #print "date is ", [d]

    md = re.match("(?u)(\d+)\. (\w+) (\d+)$", d.decode('utf-8'))
    #print [md.group(2)]
    #print "month is ", [md.group(2)]
    imonth = months.index(md.group(2)) + 1
    return datetime.date(int(md.group(3)), imonth, int(md.group(1)))

date0 = ''

for tr in root.cssselect("table[class='wilko'] tr"):
    
    tds = tr.cssselect("td")

    #print tds, len(tds)
    if len(tds)> 3:
        
        tds = [td.text_content().encode('utf-8').replace("\xc2\xa0", " ") for td in tds]
        if tds[0].strip() != '':
            date0 = tds[0]
        else:
            tds[0] = date0


        # Reads include the encoded text_content for each td in our list of tds. After this tds is a list of string
        data = {'Jahr' : tds[0],'Termin' : tds[1],'Bundesland' : tds[2],'Organ' : tds[3],'Wahl-periode' : tds[4]}        
        if tds[1]!=' ':
        #standardise date
            print data
            #if(re.match('^\d.*',data['Termin'])):
                #print [convertdate(data['Termin'] + ' ' + data['Jahr'])]

            #for a,b in data.items(): print a,b
            scraperwiki.sqlite.save(['Termin','Bundesland'],data)