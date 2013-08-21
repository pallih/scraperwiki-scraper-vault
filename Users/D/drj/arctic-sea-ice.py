# David Jones, Climate Code Foundation

import scraperwiki

import itertools
import sys
import urllib2

print sys.version

url = "ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/Jan/N_01_area.txt"

def urlopen(url):
    return urllib2.urlopen(url)

datafiles = ['N_%02d_area.txt' % m for m in range(1,13)]

def data_url():
    """Return a stream for the 12 URLs for sea-ice data."""

    prefix = 'ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/'
    for mon,basename in zip(
      ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      datafiles):
        yield prefix + mon + '/' + basename


def single_data(file):
    """Process single datafile and return its data as a stream of
    (year,extent) pairs, where year is a fraction.
    """
    for line in file:
        if not line[0:4].isdigit():
            continue
        field = line.split()
        year = float(field[0])
        month = float(field[1])
        extent = float(field[4])
        # Convert to fractional year.
        year += (month-0.5)/12.0
        yield year,extent


l = list(itertools.chain(*(single_data(urlopen(url)) for url in data_url())))
l.sort()
print l

for item in l:
    scraperwiki.datastore.save(unique_keys=['t'], data=dict(zip('tv', item)))



