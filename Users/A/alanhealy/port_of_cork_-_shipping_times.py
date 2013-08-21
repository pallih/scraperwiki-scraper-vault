import scraperwiki  
import lxml.html   
import datetime

now = datetime.datetime.now()
         
html = scraperwiki.scrape("http://www.portofcork.ie/index.cfm/page/shippingschedule1")
root = lxml.html.fromstring(html)

for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds)==8:
        data = {
            'Vessel Status' : tds[0].text_content(),
            'VesselName' : tds[1].text_content(),
            'Date of Arrival' : tds[2].text_content(),
            'Time of Arrival' : tds[3].text_content(),
            'Vessel Cubic Feet per Minute' : tds[4].text_content(),            
            'Vessel Length' : tds[5].text_content(),
            'Vessel Draft' : tds[6].text_content(),
            'Vessel Port' : tds[7].text_content(),
            # 'Db Time' : datetime.date(now.)
        }
        scraperwiki.sqlite.save(unique_keys=['VesselName'], data=data, table_name="portarrivals")
        print data


# scraperwiki.sqlite.execute("create table portarrivals")

# scraperwiki.sqlite.execute("delete * from portarrivals")

# scraperwiki.sqlite.save(unique_keys, data, table_name="portarrivals", verbose=2) 

# scraperwiki.sqlite.execute("insert into swdata values (?,?,?)", [a,b,c])






