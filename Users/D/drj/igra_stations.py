# David Jones, Climate Code Foundation, 2011-09-28

import scraperwiki

import StringIO
import urllib

scraperwiki.sqlite.execute("drop table meta;")
scraperwiki.sqlite.execute("""create table if not exists meta
    (id text, name text, Latitude real, Longitude real, Elevation real, wmo_identifier text)""")
scraperwiki.sqlite.commit()

# To get a nice logo on the ScraperWiki page.
dummy = urllib.urlopen("http://www.crh.noaa.gov/mpx/history/balloonparachuteinstrumentlaunch.jpg").read()

url = "http://www1.ncdc.noaa.gov/pub/data/igra/igra-stations.txt"
columns = dict(
    fips_country = (0,2,str),
    id = (4,9,str),
    wmo_identifier = (4,9,str),
    name = (11,46,str),
    Latitude = (47,53,float),
    Longitude = (54,61,float),
    Elevation = (62,66,float),
    GUAN = (67,68,str),
    LKS = (68,69,str),
    Composite = (69,70,str),
    first_year = (72,76,int),
    last_year = (77,81,int),
    )

data = []
for row in StringIO.StringIO(urllib.urlopen(url).read()):
    d = {}
    for k,(i,j,convert) in columns.items():
        d[k] = convert(row[i:j])
    data.append(d)
scraperwiki.sqlite.save(['id'], data, table_name='meta')

print "Scraped"# David Jones, Climate Code Foundation, 2011-09-28

import scraperwiki

import StringIO
import urllib

scraperwiki.sqlite.execute("drop table meta;")
scraperwiki.sqlite.execute("""create table if not exists meta
    (id text, name text, Latitude real, Longitude real, Elevation real, wmo_identifier text)""")
scraperwiki.sqlite.commit()

# To get a nice logo on the ScraperWiki page.
dummy = urllib.urlopen("http://www.crh.noaa.gov/mpx/history/balloonparachuteinstrumentlaunch.jpg").read()

url = "http://www1.ncdc.noaa.gov/pub/data/igra/igra-stations.txt"
columns = dict(
    fips_country = (0,2,str),
    id = (4,9,str),
    wmo_identifier = (4,9,str),
    name = (11,46,str),
    Latitude = (47,53,float),
    Longitude = (54,61,float),
    Elevation = (62,66,float),
    GUAN = (67,68,str),
    LKS = (68,69,str),
    Composite = (69,70,str),
    first_year = (72,76,int),
    last_year = (77,81,int),
    )

data = []
for row in StringIO.StringIO(urllib.urlopen(url).read()):
    d = {}
    for k,(i,j,convert) in columns.items():
        d[k] = convert(row[i:j])
    data.append(d)
scraperwiki.sqlite.save(['id'], data, table_name='meta')

print "Scraped"