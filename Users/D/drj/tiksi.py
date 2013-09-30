# Note really a scraper yet, just a note for where you can get
# weather balloon data for Tiksi, and many many other weather
# balloon stations.
# README at http://www1.ncdc.noaa.gov/pub/data/igra/readme.txt

import scraperwiki

import gzip
import StringIO
import urllib

url = "http://www1.ncdc.noaa.gov/pub/data/igra/data-por/21824.dat.gz"
url = "http://www1.ncdc.noaa.gov/pub/data/igra/monthly-por/temp_00z.mly.gz"
compressed = urllib.urlopen(url).read()
g = gzip.GzipFile(fileobj=StringIO.StringIO(compressed))

def convertT(x):
    """Convert a temperature field in the monthly mean file
    to degrees Celsius."""
    return 0.1*int(x)

columns = dict(
    id = (0,5,str),
    wmo_identifier = (0,5,str),
    year = (6,10,int),
    month = (11,13,int),
    pressure_level = (14,18,int),
    tmeanM = (19,24,convertT),
    d = (25,27,int)
    )
for row in g.read().strip().split('\n'):
    d = {}
    for k,(i,j,convert) in columns.items():
        d[k] = convert(row[i:j])
    scraperwiki.sqlite.save(['id', 'year', 'month', 'pressure_level'], d)
    
print "Scraped"# Note really a scraper yet, just a note for where you can get
# weather balloon data for Tiksi, and many many other weather
# balloon stations.
# README at http://www1.ncdc.noaa.gov/pub/data/igra/readme.txt

import scraperwiki

import gzip
import StringIO
import urllib

url = "http://www1.ncdc.noaa.gov/pub/data/igra/data-por/21824.dat.gz"
url = "http://www1.ncdc.noaa.gov/pub/data/igra/monthly-por/temp_00z.mly.gz"
compressed = urllib.urlopen(url).read()
g = gzip.GzipFile(fileobj=StringIO.StringIO(compressed))

def convertT(x):
    """Convert a temperature field in the monthly mean file
    to degrees Celsius."""
    return 0.1*int(x)

columns = dict(
    id = (0,5,str),
    wmo_identifier = (0,5,str),
    year = (6,10,int),
    month = (11,13,int),
    pressure_level = (14,18,int),
    tmeanM = (19,24,convertT),
    d = (25,27,int)
    )
for row in g.read().strip().split('\n'):
    d = {}
    for k,(i,j,convert) in columns.items():
        d[k] = convert(row[i:j])
    scraperwiki.sqlite.save(['id', 'year', 'month', 'pressure_level'], d)
    
print "Scraped"