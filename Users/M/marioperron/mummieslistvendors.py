import scraperwiki
import lxml.html
import unicodedata
from googlemaps import GoogleMaps
#mettre le code GoogleMaps

for i in range(1,13):
    html = scraperwiki.scrape("http://mummieslist.com/mummy-card-savings-list/999/" + str(i) + "/")
    root = lxml.html.fromstring(html)
    last = ""
    for el in root.cssselect("div a"):
        if el.attrib['href'][0:8] == '/vendor/':
            if el.attrib['href'] != last:
                url = el.attrib['href']
                html2 = scraperwiki.scrape("http://mummieslist.com" + url)
                root2 = lxml.html.fromstring(html2)
                name = root2.cssselect("h3")[1].text_content()
                print name
                try:
                    name = name.decode('ascii','replace')
                except:
                    name = "Erreur"
                start = "<h2>Coordinates</h2>"
                end = "<br />Phone"
                addr = (html2.split(start))[1].split(end)[0]
                addr = addr.replace('<br />','')
                addr = addr.replace('\n    ',' ')
                try:
                    addr = addr.decode('ascii','replace')
                except:
                    addr = "Erreur"
                start = "<strong>Discount</strong><br />"
                end = "<br /><br />"
                disc = (html2.split(start))[1].split(end)[0]
                disc = disc.replace('<br />','')
                disc = disc.replace('\n    ',' ')
                try:
                    disc = disc.decode('ascii','replace')
                except:
                    disc = "Erreur"
                try:
                    lat, long = gmaps.address_to_latlng(addr)
                except:
                    lat = 0.00
                    long = 0.00
                    print "NOT FOUND: " + addr
                if (name != "Erreur") and (addr != "Erreur") and (disc != "Erreur"):
                    scraperwiki.sqlite.save(unique_keys=["url"], data={"url":url, "name":name, "addr":addr, "disc":disc, "long":long, "lat":lat}) 

        last = el.attrib['href']

print "Done!"
