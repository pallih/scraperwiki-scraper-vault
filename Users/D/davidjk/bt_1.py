import scraperwiki
import lxml.html

# Blank Python
html = scraperwiki.scrape("http://www.bundestag.de/bundestag/abgeordnete17/biografien/S/steinbrueck_peer.html")
root = lxml.html.fromstring(html)

#print lxml.html.tostring(html)

info = root.cssselect('div[class=\"standardBox biografie\"] h1')
info =  info[0].text_content()
name, splitter, party = info.partition(", ")


#for voa in root.cssselect('div[class=\"infoBox voa\"] p[class=\"voa_tab1\"]'):
#    print voa.text_content()
    


#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        print data