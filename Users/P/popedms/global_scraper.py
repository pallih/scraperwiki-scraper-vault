import scraperwiki
import re

#   Trick ScraperWiki into giving us a pretty thumbnail
scraperwiki.scrape('http://xchngd.files.wordpress.com/2011/11/dsc_00152.jpg')

def collate_data():
    
    scraperwiki.sqlite.attach("occupy_protest_locations_global")
    scraperwiki.sqlite.attach("occupy_protest_locations_usa")
    scraperwiki.sqlite.attach("occupy_protest_locations_california")
    
    global_locations = scraperwiki.sqlite.select("* from occupy_protest_locations_global.locations")
    usa_locations = scraperwiki.sqlite.select("* from occupy_protest_locations_usa.cities")
    california_locations = scraperwiki.sqlite.select("* from occupy_protest_locations_california.cities")
    
    print "Saving global locations"
    for location in global_locations:
        print "Saving " + location['location']
        scraperwiki.sqlite.save(unique_keys=["location"], data={"contintent": location['contintent'], "country": location['country'], "state": "", "city": location['city'], "location": location['location'], "start_date_raw": location['start_date'], "start_date": "", "estimated_attendance": location['estimated_attendance'], "latitude": location['latitude'], "longitude": location['longitude']}, table_name="locations")
    
    print "Saving USA locations"
    for location in usa_locations:
        print "Saving " + location['location']
        scraperwiki.sqlite.save(unique_keys=["location"], data={"contintent": "North America", "country": "USA", "state": location['state'], "city": location['city'], "location": location['location'], "start_date_raw": location['start_date'], "start_date": "", "estimated_attendance": location['estimated_attendance'], "latitude": location['latitude'], "longitude": location['longitude']}, table_name="locations")
    
    print "Saving California locations"
    for location in california_locations:
        print "Saving " + location['city']
        scraperwiki.sqlite.save(unique_keys=["location"], data={"contintent": "North America", "country": "USA", "state": "California", "city": location['city'], "location": location['city'] + ", California", "start_date_raw": location['start_date'], "start_date": "", "estimated_attendance": location['estimated_attendance'], "latitude": location['latitude'], "longitude": location['longitude']}, table_name="locations")

    return



def clean_attendance():
    
    records = scraperwiki.sqlite.select("* from locations where estimated_attendance is not null and estimated_attendance != ''")

    print "Removing commas from " + str(len(records)) + " attendance figures..."
    for record in records:
        print "Removing commas from " + record['location'] + "..."
        scraperwiki.sqlite.execute('update locations set estimated_attendance = "' + record['estimated_attendance'].replace(',', '') + '" where location = "' + record['location'] + '" and estimated_attendance = "' + record['estimated_attendance'] + '"')
        scraperwiki.sqlite.commit()
    
    return
'''

def clean_north_bay():
    
    records = scraperwiki.sqlite.select("* from locations where location='North Bay, Ontario'")

    for record in records:
        scraperwiki.sqlite.execute('update locations set start_date_raw = "" where location = "' + record['location'] + '"')
        scraperwiki.sqlite.commit()
    
    return

'''

def clean_dates():

    # converts hokey Wikipedia dates into ISO 8601 standard YYYY-MM-DD

    records = scraperwiki.sqlite.select("start_date_raw, location from `locations` where start_date_raw != '' order by location")
    i = 1
    t = len(records)
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']

    print "Cleaning dates for " + str(t) + " records..."

    for record in records:
        print "(" + str(i) + "/" + str(t) + ") Cleaning date for " + record['location'] + "..."
        date = str(record['start_date_raw'])
        y = '2011'
        i2 = 0
        for month in months:
            i2 = i2 + 1
            if date.find(month[0:3]) >= 0:
                m_num = '%02d' % i2
                break
        d = re.search('(\d+)', date.replace('2011','')).group(0)
        scraperwiki.sqlite.execute('update locations set start_date = "' + y + '-' + m_num + '-' + d.zfill(2) + '" where location = "' + record['location'] + '"')
        scraperwiki.sqlite.commit()
        i = i + 1

    return
