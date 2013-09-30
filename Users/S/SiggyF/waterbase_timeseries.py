import scraperwiki
import csv         
import datetime 

observationtype_cfname = {
    22: 'sea_surface_wind_wave_significant_height',
    23: 'sea_surface_wind_wave_from_direction',
    24: 'sea_surface_wind_wave_period'
    }


# Store all data in memory
data = {}
# Loop over all wave observation types
scraperwiki.sqlite.attach('waterbase')
rs = scraperwiki.sqlite.execute('SELECT * FROM location_observationtype WHERE observationtype_id >= ? AND observationtype_id < ? ORDER BY location_id', (22,25))
for obsrow in rs['data']:
    # Store in a dictionary by key
    obsrecord = dict(zip(rs['keys'], obsrow))
    # Build a url 
    # This webservice is unsupported by rws. 
    # there is a php script that does the same, but this one seems to respond faster.
    url = 'http://live.waterbase.nl/wswaterbase/cgi-bin/wbGETDATA?ggt=id{observationtype_id}&loc={location_id}&from=201001010000&to=201501010000'.format(**obsrecord)
    
    # Scrape the url
    csvdata = scraperwiki.scrape(url)

    # Skip the header
    lines = csvdata.splitlines()[3:]
    # The fieldnames
    fieldnames = lines.pop(0).split(';')
    # Read the csv file
    reader = csv.reader(lines, delimiter=';')

    # Loop over the csv file
    for csvrow in list(reader):
        # Parse the date, ignore timezone for now
        try:
            date = datetime.datetime.strptime(csvrow[2] + ' ' + csvrow[3], '%Y-%m-%d %H:%M')
        except Exception as error:
            print csvrow
            print 'Ignoring:', error
            continue

        # Get the value, if it doesn't exist, create it.
        # Store all related wave data in one record in a table...
        value = data.get((obsrecord['location_id'], date), {})
        # update the value with the cfname
        value[observationtype_cfname[obsrecord['observationtype_id']]] = float(csvrow[5])
        # store the value
        data[(obsrecord['location_id'], date)] = value

# Loop over the data in memory
# If this runs out of memory, create outer loop over locations...
for key, value in data.items():
    # Create a copy, to save memory
    record = value.copy()
    record['location_id'] = key[0]
    record['date'] = key[1]
    scraperwiki.sqlite.save(unique_keys=['location_id', 'date'], data=record, table_name='waves')import scraperwiki
import csv         
import datetime 

observationtype_cfname = {
    22: 'sea_surface_wind_wave_significant_height',
    23: 'sea_surface_wind_wave_from_direction',
    24: 'sea_surface_wind_wave_period'
    }


# Store all data in memory
data = {}
# Loop over all wave observation types
scraperwiki.sqlite.attach('waterbase')
rs = scraperwiki.sqlite.execute('SELECT * FROM location_observationtype WHERE observationtype_id >= ? AND observationtype_id < ? ORDER BY location_id', (22,25))
for obsrow in rs['data']:
    # Store in a dictionary by key
    obsrecord = dict(zip(rs['keys'], obsrow))
    # Build a url 
    # This webservice is unsupported by rws. 
    # there is a php script that does the same, but this one seems to respond faster.
    url = 'http://live.waterbase.nl/wswaterbase/cgi-bin/wbGETDATA?ggt=id{observationtype_id}&loc={location_id}&from=201001010000&to=201501010000'.format(**obsrecord)
    
    # Scrape the url
    csvdata = scraperwiki.scrape(url)

    # Skip the header
    lines = csvdata.splitlines()[3:]
    # The fieldnames
    fieldnames = lines.pop(0).split(';')
    # Read the csv file
    reader = csv.reader(lines, delimiter=';')

    # Loop over the csv file
    for csvrow in list(reader):
        # Parse the date, ignore timezone for now
        try:
            date = datetime.datetime.strptime(csvrow[2] + ' ' + csvrow[3], '%Y-%m-%d %H:%M')
        except Exception as error:
            print csvrow
            print 'Ignoring:', error
            continue

        # Get the value, if it doesn't exist, create it.
        # Store all related wave data in one record in a table...
        value = data.get((obsrecord['location_id'], date), {})
        # update the value with the cfname
        value[observationtype_cfname[obsrecord['observationtype_id']]] = float(csvrow[5])
        # store the value
        data[(obsrecord['location_id'], date)] = value

# Loop over the data in memory
# If this runs out of memory, create outer loop over locations...
for key, value in data.items():
    # Create a copy, to save memory
    record = value.copy()
    record['location_id'] = key[0]
    record['date'] = key[1]
    scraperwiki.sqlite.save(unique_keys=['location_id', 'date'], data=record, table_name='waves')