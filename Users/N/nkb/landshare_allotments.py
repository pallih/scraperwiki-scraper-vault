import scraperwiki
import re

id_start  = 0;

id_start_array = scraperwiki.sqlite.execute("select max(id) from swdata");

id_start = id_start_array["data"][0][0]

for id in range(id_start, id_start+10):

    url = "http://www.landshare.net/listings/" + str(id) + "/"
    
    html = scraperwiki.scrape(url)
    
    
    if id_start>0:

        ## Looks for the lat/lng data
        
        pattern = "var marker = new GMarker\(new GLatLng\(([-\d\.]*), ([-\d\.]*)\), { icon : icon } \);"
            
        match = re.search(pattern, html)
        
        lat = 0
        lng = 0
    
        if match:
            lat = match.group(1)  
            lng = match.group(2)
        
        
        if (float(lat)!=0 and float(lng)!=0):
            ## Saves everything
            
            record = { "id": id, "lat" : float(lat), "lng": float(lng) }
            scraperwiki.sqlite.save(["id"], record)