# David Jones, Climate Code Foundation, 2011-09-14
# GHCN v3 Metadata.  In particular, the data ranges for each station.

# REFERENCES
# [V3README] ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/v3/README

import scraperwiki

import itertools
import StringIO
import tarfile
import urllib

ghcnv3 = 'http://www1.ncdc.noaa.gov/pub/data/ghcn/v3/ghcnm.tavg.latest.qcu.tar.gz'

def id11(row):
    return row[:11]

def process_data(f):
    """Process a GHCN v3 .dat file."""
    for id,rows in itertools.groupby(f, id11):
        save = []
        for row in rows:
            year = int(row[11:15])
            element = row[15:19]
            for m,(v,flag) in enumerate((row[c:c+5],row[c+5:c+8]) for c in range(19,108,8)):
                if v == '-9999':
                    continue
                data = dict(id=id, element=element, year=year, flag=flag, v=v, month=m+1)
                save.append(data)
        scraperwiki.sqlite.save(['id', 'element', 'year', 'month'], save)

z = urllib.urlopen(ghcnv3).read()

tar = tarfile.open(mode='r:gz', fileobj=StringIO.StringIO(z))
for info in tar:
    if info.name.endswith('.dat'):
        # The data file
        process_data(tar.extractfile(info))

print "Scraped"
# David Jones, Climate Code Foundation, 2011-09-14
# GHCN v3 Metadata.  In particular, the data ranges for each station.

# REFERENCES
# [V3README] ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/v3/README

import scraperwiki

import itertools
import StringIO
import tarfile
import urllib

ghcnv3 = 'http://www1.ncdc.noaa.gov/pub/data/ghcn/v3/ghcnm.tavg.latest.qcu.tar.gz'

def id11(row):
    return row[:11]

def process_data(f):
    """Process a GHCN v3 .dat file."""
    for id,rows in itertools.groupby(f, id11):
        save = []
        for row in rows:
            year = int(row[11:15])
            element = row[15:19]
            for m,(v,flag) in enumerate((row[c:c+5],row[c+5:c+8]) for c in range(19,108,8)):
                if v == '-9999':
                    continue
                data = dict(id=id, element=element, year=year, flag=flag, v=v, month=m+1)
                save.append(data)
        scraperwiki.sqlite.save(['id', 'element', 'year', 'month'], save)

z = urllib.urlopen(ghcnv3).read()

tar = tarfile.open(mode='r:gz', fileobj=StringIO.StringIO(z))
for info in tar:
    if info.name.endswith('.dat'):
        # The data file
        process_data(tar.extractfile(info))

print "Scraped"
