import scraperwiki
import csv 

edata = scraperwiki.scrape("http://earthquake.usgs.gov/earthquakes/feed/csv/1.0/week")
reader = csv.DictReader(edata.splitlines())

for row in reader:
    if row['Latitude']: row['Latitude'] = float(row['Latitude'])
    if row['Longitude']: row['Longitude'] = float(row['Longitude'])
    if row['Depth']: row['Depth'] = float(row['Depth'])
    if row['Magnitude']: row['Magnitude'] = float(row['Magnitude'])
    if row['NbStations']: row['NbStations'] = int(row['NbStations'])
    if row['Gap']: row['Gap'] = int(row['Gap'])
    if row['Distance']: row['Distance'] = float(row['Distance'])
    if row['RMS']: row['RMS'] = float(row['RMS'])
    scraperwiki.sqlite.save(unique_keys=['DateTime', 'Latitude', 'Longitude', 'Depth', 'Magnitude', 'MagType', 'NbStations', 'Gap', 'Distance', 'RMS', 'Source', 'EventID', 'Version'], data=row)

