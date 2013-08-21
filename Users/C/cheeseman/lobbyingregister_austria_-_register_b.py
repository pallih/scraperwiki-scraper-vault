import scraperwiki
import lxml.html
# from BeautifulSoup import BeautifulSoup
# import urllib2

# Blank Python


html = scraperwiki.scrape("http://www.lobbyreg.justiz.gv.at/edikte/ir/iredi18.nsf/suchera!OpenForm&subf=r&RestrictToCategory=B") 
#print html

root = lxml.html.fromstring(html)
#print root

i = 0

for trs in root.cssselect("tbody tr"): 
    #print lxml.html.tostring(trs)
    tds = trs.cssselect("td")
    
    data = { 
        'id' : i,
        'Bezeichnung' : tds[1].text_content(), 
        'Registerzahl' : tds[2].text_content(), 
        #'RegisterzahlURL' : tds[2].attrib['href'], 
        'Registerabteilung' : tds[3].text_content(), 
        'Details' : tds[4].text_content(), 
        'LetzteAenderung' : tds[5].text_content(), 
        'Lobbyisten' : 10
    }
    scraperwiki.sqlite.save(unique_keys=['id', 'Registerzahl'], data=data)
    i = i+1





