import scraperwiki
import urllib
import csv

try:
    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS Grassroots_Mapping_Metadata")
    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS Grassroots_Mapping_Data")
    scraperwiki.sqlite.execute("CREATE TABLE Grassroots_Mapping_Data ('dataset_id' integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 'dataset_name' string, 'latitude' string, 'longitude' string, 'resolution' string, 'zip_url' string, 'geo_tiff_url' string, 'kml' string, 'openlayers_url' string, 'flickr_url' string, 'stitch_value_notes' string, 'who_stiched' string, 'date' date, 'status' string)")
    scraperwiki.sqlite.execute("CREATE TABLE Grassroots_Mapping_Metadata ('metadata_id' integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,'timestamp' string, 'how_imagery_sent' string, 'what_wrong_equipment' string, 'what_needs_replace' string, 'imagery_location' string, 'number_of_images_taken' string, 'altitude' string, 'leader_email' string, 'team' string, 'site_number_visited_times' string, 'site_changes' string,'site_trouble_getting_out' string, 'flying_condition' string, 'map_use_desc' string, 'misc_notes' string, 'time_of_day' string, 'dataset_id' int, FOREIGN KEY(dataset_id) REFERENCES Grassroots_Mapping_Data(dataset_id) )")
except Exception, err:
    print('ERROR: %s\n' % str(err))
    pass

url = 'https://spreadsheets.google.com/pub?key=0AlY4Tg28DhosdGgtVk1fVmV5aG84WTNPbTQyY3dhc3c&hl=en&single=true&gid=0&output=csv'
response = urllib.urlopen(url)
csvData = response.readlines()

data = csv.DictReader(csvData, dialect='excel')

for row in data:
    
    datasetList = ( row['Dataset Name'], row['latitude'], row['longitude'], row['resolution'], row['packaged zip file URL'], row[' GeoTiff URL'], row['KML Google Earth/Maps'], row['OpenLayers tile set URL'], row['Link to photos on Flickr'], row['Stitch value notes'], row["Who stitched it or who's working on it"], row['Date'], row['Status'])
    scraperwiki.sqlite.execute("INSERT INTO Grassroots_Mapping_Data (dataset_name, latitude, longitude, resolution, zip_url, geo_tiff_url, kml, openlayers_url, flickr_url, stitch_value_notes, who_stiched, date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", datasetList)
    
    metadataList = ( row['Timestamp'], row['How is the imagery being sent?'], row['What went wrong with the equipment?'], row['What needs to be replaced?'], row['What location was the imagery captured at? GPS Latitude/ Longitude is best.'], row['How many images did you get, exactly?'], row['At roughly what altitude were you flying?'], row['Who led this trip? Email address please.'], row['Who was on the trip?'], row['How many times has the site been visited before?'], row["What's changed at the site?"], row['Did you have trouble getting out to the site?'], row['Tell us about flying conditions.'], row['What did you use to map?'], row['Misc. notes'], row['What time of day were the pictures taken?'], str(scraperwiki.sqlite.execute('SELECT MAX(dataset_id) FROM Grassroots_Mapping_Data')))
    scraperwiki.sqlite.execute("INSERT INTO Grassroots_Mapping_Metadata (timestamp, how_imagery_sent, what_wrong_equipment, what_needs_replace, imagery_location, number_of_images_taken, altitude, leader_email, team, site_number_visited_times, site_changes, site_trouble_getting_out, flying_condition, map_use_desc, misc_notes, time_of_day, dataset_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", metadataList)

scraperwiki.sqlite.commit()
