import scraperwiki, re

#cleaning tables
#scraperwiki.sqlite.execute("drop table if exists swdata")
#import table from tenderscrapy
scraperwiki.sqlite.attach("tenderscrapy", 'tenders')
tenders=scraperwiki.sqlite.select("* from tenders.swdata")

urlbase="http://api.maps.yahoo.com"
urldir="/ajax/geocode"
urlparms="?appid=onestep&qt=1&id=m&qs="
urladdress=""

def posting(url, params, method):
    params = urllib.urlencode(params)
    if method=='POST':
        f = urllib2.urlopen(url, params)
    else:
        f = urllib2.urlopen(url+'?'+params)
    return (f.read(), f.code)

for t in tenders:
    if t.get('oggetto') and t.get('luogo'):
        try:
            address=re.search(r'\s((via|viale|largo|piazza)\s([a-zA-Z]|\s){4,})\s[\d+|\.|\-]',t.get('oggetto'),re.I)
            posto=re.search(r'\-\s+(\w{4,})',t.get('luogo'),re.I)
            if address and posto:
                print ">>luogo: "+posto.group(1)+" >>indirizzo: "+address.group(1)
                print ">>url: "+urlbase+urldir+urlparms+address.group(1).replace(' ','+')+"+"+posto.group(1).replace(' ','+')
                content = scraperwiki.scrape(urlbase+urldir+urlparms+address.group(1).replace(' ','+')+"+"+posto.group(1).replace(' ','+'))
                latlon=re.search('.Lat.\:(\d+\.\d+)\,.Lon.\:(\d+\.\d+)',content)
                if latlon:
                    print "LatLon: "+str(latlon.group(1))+","+str(latlon.group(2))
                    t.update({"indirizzo":str(address.group(1)),
                                "posto":str(posto.group(1)),
                                "lat":latlon.group(1),
                                "lon":latlon.group(2),
                                "latlon":str(latlon.group(1))+","+str(latlon.group(2))})
                    scraperwiki.sqlite.save(['id'], t, table_name="swdata")
        except:
            pass

print "len: "+str(len(tenders))


#YGeoCode.getMap({"GeoID":"m","GeoAddress":"via salvatore d amelio roma","GeoPoint":{"Lat":41.904908,"Lon":12.430845},"GeoMID":false,"success":1},1);
#http://api.maps.yahoo.com/ajax/geocode?appid=onestep&qt=1&id=m&qs=via+salvatore+d+amelio+roma
