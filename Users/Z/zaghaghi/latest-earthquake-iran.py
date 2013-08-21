import scraperwiki           
import lxml.html  

def scrape(root, selector):
    for tr in root.cssselect("tr[class='" + selector+ "']"):
        tds = tr.cssselect("td")
        id = tds[0].text
        datetd = tds[1].cssselect("a[class='" + selector+ "']")
        datetime = datetd[0].text.split(' ')
        date = datetime[0]
        time = datetime[1]
        lat = tds[2].text
        lon = tds[3].text
        depth = tds[4].text
        mag = tds[5].text
        loc = tds[6].text
        #print id, date, time, lat, lon, depth, mag, loc
        data = {
                'id': int(id),
                'date' : date,
                'time' : time,
                'latitude' : float(lat.strip()[:-1].strip()),
                'longitude' : float(lon.strip()[:-1].strip()),
                'depth' : float(depth),
                'mag' : float(mag),
                'location' : loc.strip()
        }
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)


html = scraperwiki.scrape("http://irsc.ut.ac.ir/currentearthq.php")
         
root = lxml.html.fromstring(html)

scrape(root, "DataRow1")
scrape(root, "DataRow2")



