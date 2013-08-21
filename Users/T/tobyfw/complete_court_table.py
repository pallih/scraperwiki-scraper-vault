import scraperwiki
import simplejson
import urllib

# Viasna association table
print "Step 1"
doc='https://spreadsheets.google.com/feeds/list/0Aqz287ckIQd-dHJmM25Oa3RkYnhJVGVuam90eVpyWFE/1/public/values?alt=json'
entities=simplejson.load(urllib.urlopen(doc))
rows = entities['feed']['entry']

for row in rows:
    courtViasna = row["gsx$viasna"]["$t"]
    courtMOJ = row["gsx$ministryofjustice"]["$t"]
    lat = row["gsx$lat"]["$t"]
    lng = row["gsx$lng"]["$t"]
    
    data = {
        'CourtViasna' : courtViasna,
        'Court' : courtMOJ,
        'Lat' : lat,
        'Lng' : lng
    }
    #scraperwiki.sqlite.save(unique_keys=['Court'], data=data, table_name="viasna")

#Court information
print "Step 2"
doc='https://spreadsheets.google.com/feeds/list/0Aqz287ckIQd-dHJmM25Oa3RkYnhJVGVuam90eVpyWFE/2/public/values?alt=json'
entities=simplejson.load(urllib.urlopen(doc))
rows = entities['feed']['entry']

for row in rows:
    courtMOJ = row["gsx$court"]["$t"]
    telephone = row["gsx$telephone"]["$t"]
    district = row["gsx$district"]["$t"]
    address = row["gsx$address"]["$t"]
    lng = row["gsx$lng"]["$t"]
    lat = row["gsx$lat"]["$t"]
    
    data = {
        'Court' : courtMOJ,
        'Telephone' : telephone,
        'District' : district,
        'Address' : address,
        'Lat' : lat,
        'Lng' : lng
    }
    #scraperwiki.sqlite.save(unique_keys=['Court'], data=data, table_name="moj")

#Join
print "Step 3"
data = scraperwiki.sqlite.select("moj.Court, viasna.CourtViasna, (ifnull(moj.Lat,'') || ifnull(viasna.Lat,'')) as Lat, (ifnull(moj.Lng,'') || ifnull(viasna.Lng,'')) as Lng, moj.Address, moj.Telephone, moj.District from viasna left join moj on viasna.Court=moj.Court")  

for d in data:
    scraperwiki.sqlite.save(unique_keys=['CourtViasna'], data=d)




