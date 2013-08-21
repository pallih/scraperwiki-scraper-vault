import scraperwiki           
html = scraperwiki.scrape("http://www.umweltbundesamt.at/umweltsituation/luft/luftguete_aktuell/tgl_bericht/")

import lxml.html     

def toFraction(position):
    parts1 = position.split(u"\xb0")
    degree = float(parts1[0])
    parts2 = parts1[1].split(u"'")
    degree += float(parts2[0]) / 60
    parts3 = parts2[1].split(u'"') 
    degree += float(parts3[0]) / (60 * 60)
    return degree

def getLongLat(network, station):
    params = {
                        'NETWORK' : network,
                        'STATION' : station
                    }
    html = scraperwiki.scrape("http://www.umweltbundesamt.at/umweltsituation/luft/luftguete_aktuell/tgl_bericht/?cgiproxy_url=http%3A%2F%2Fluft.umweltbundesamt.at%2Fpub%2Fstationinfo%2Findex.pl", params)
    root = lxml.html.fromstring(html)
    for table in root.cssselect("table"):
        for tr in table.cssselect("tr"):
            if len(tr.getchildren()) < 2:
                continue
            if tr[0].text_content() == "Breite":
                latitude = tr[1].text_content()
                latitudeVal = toFraction(latitude)
                prev = tr.getprevious()
                longitude = prev[1].text_content()
                longitudeVal = toFraction(longitude)
                return [longitudeVal , latitudeVal ]





root = lxml.html.fromstring(html)
for tr in root.cssselect("th[class='tabhead']"):
    if tr.text_content()=="Feinstaub Tages-Mittelwert":
        parent = tr.getparent()
        div = parent.getparent()
        titlerow = parent.getprevious()
        print titlerow[0][0].text_content()
        trlist = div.cssselect("tr[class='row']")
        trlist += div.cssselect("tr[bgcolor='white']")
        for valueTr in trlist:

            name = valueTr[0][0].text_content()
            onclick = valueTr[0][0].attrib['onclick']
            splitValues = onclick.split("'")
            network = splitValues[1]
            station = splitValues[3]
            id = network + ":" + station
            value = "-"
            if len(valueTr[1].getchildren()) > 0:
                value = valueTr[1][0].text_content()
            longLat = getLongLat(network, station)
            data = {
                        'id' : id,
                        'name' : name,
                        'pm10' : value,
                        'lon' : longLat[0],
                        'lat' : longLat[1]
                    }
            print data
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)
            
