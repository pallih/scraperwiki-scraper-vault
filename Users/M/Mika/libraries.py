import scraperwiki
html = scraperwiki.scrape('http://www.torontopubliclibrary.ca/branches/index.jsp') #'http://www.dairyqueen.com/us-en/stores/nc/')

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
results = root.cssselect('div.result-list')


address_fields = ["store_id INTEGER PRIMARY KEY","name TEXT", "url TEXT", "googleRef TEXT", "latitude TEXT", "longitude TEXT"] 
scraperwiki.sqlite.execute("drop table if exists locations")
scraperwiki.sqlite.execute("drop table if exists LibrariesTO")
scraperwiki.sqlite.execute("create table if not exists LibrariesTO (%s)" \
  % ",".join(address_fields))
dqStoreId = 0
cards = root.cssselect('div.record-result')
for card in cards: 
    
    a = card.cssselect('div div.title a')[0]
    url =  "http://www.torontopubliclibrary.ca" + a.get("href")
    name =  a.text
    #text = card.cssselect('div.text')
    
    ####test ###
    #lat = 0
    #lon = 0  
    #googleRef = 'hy'

    #if dqStoreId >90:
    html2 = scraperwiki.scrape(url)
    root2 = lxml.html.fromstring(html2)
    
    imgDiv= root2.cssselect('div.map-container img')[0]
    googleRef = imgDiv.get("src")
          
    market = "?markers="
    format = "&format="
    x = googleRef.find(market) + len(market ) 
    y = googleRef.find(format) #- len(format) 
    #43.654184-79.403176
    latlong = googleRef[x:y]
    #print latlong
    a = latlong.find(",")
    lat = latlong[:a]
    #b = a + 3
    lon = latlong[a:]
    lon = lon.replace(",", "")
    #print latlong;
    #print "lat:"+lat + "long:"+lon
    #### if test end ### 
    scraperwiki.sqlite.execute("DELETE from 'LibrariesTO' where store_id = ?", (dqStoreId))
    scraperwiki.sqlite.execute("INSERT into 'LibrariesTO' values(?,?,?,?,?,?)", (dqStoreId, name, url, googleRef,lat,lon))
    dqStoreId = dqStoreId + 1

scraperwiki.sqlite.commit()
results = scraperwiki.sqlite.execute("select count(*) from LibrariesTO")
print(results)



