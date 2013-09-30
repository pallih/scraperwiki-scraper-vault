import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.mehr-demokratie.de/volksbegehren-deutschland.html")
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[class='contenttable contenttable-2'] tr"):
    tds = tr.cssselect("td")
    tds = [td.text_content().encode('utf-8').replace("&quot;", "") for td in tds]
    if len(tds)>1:
        data = {'Nr' : tds[0],'Bundesland' : tds[1],'Verfahrenstyp' : tds[2],'Titel' : tds[3],'Ziel' : tds[4],'Status' : tds[5],'Homepage' : tds[6]}
        #print data
        scraperwiki.sqlite.save(['Bundesland','Titel'], data)
import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.mehr-demokratie.de/volksbegehren-deutschland.html")
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[class='contenttable contenttable-2'] tr"):
    tds = tr.cssselect("td")
    tds = [td.text_content().encode('utf-8').replace("&quot;", "") for td in tds]
    if len(tds)>1:
        data = {'Nr' : tds[0],'Bundesland' : tds[1],'Verfahrenstyp' : tds[2],'Titel' : tds[3],'Ziel' : tds[4],'Status' : tds[5],'Homepage' : tds[6]}
        #print data
        scraperwiki.sqlite.save(['Bundesland','Titel'], data)
