## Source: 
## https://scraperwiki.com/scrapers/example_-_read_csv/
## http://stackoverflow.com/questions/343865/how-to-convert-from-utm-to-latlng-in-python-or-javascript/344083#344083
import scraperwiki
import csv

data = scraperwiki.scrape("http://www.lambeth.gov.uk/NR/rdonlyres/7BE75960-A928-49A1-8399-482CDABC3E1F/0/LambethFoodGrowingProjects.csv")
reader = csv.DictReader(data.splitlines()) 

for row in reader:
    #lat, long = utmToLatLng(30, float(row['Easting']), float(row['Northing']), True) 
    #row.update({'Latitude': lat})
    #row.update({'Longitude': long})

    #latlng = utmToLatLng(30, float(row['Easting']), float(row['Northing'])) 
    lat, long = scraperwiki.geo.os_easting_northing_to_latlng(float(row['Easting']), float(row['Northing']), grid='GB')
    coords = str(lat) + "," + str(long)
    row.update({'Latlng': coords})
    
    row['Orgtype'] = row['']
    del row['']
    scraperwiki.sqlite.save(unique_keys=['No_'], data=row)

