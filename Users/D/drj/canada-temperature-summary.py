# canada-temperature-summary
# Summary of the data held in the canada-temperature-data scraper
# David Jones, 2011-08-31, Climate Code Foundation

import scraperwiki

import itertools
import re

def bin_counts_by_station(ds):
    """For each station in the database *ds*, count the number of records (*l*).
    Return a dict of (*l*,*count*) pairs.
    """

    # Sequence of one entry dicts, denoting the length of each station
    lengths = scraperwiki.sqlite.select("count(*) from %s.swdata where element = 'tmeanM' group by id" % ds)
    # The same, as a simple sorted list of lengths
    slengths = sorted(d.values()[0] for d in lengths)
    # Use itertools groupby to convert to dict of (length, count) pairs.
    return dict(((l,len(list(seq))) for l,seq in itertools.groupby(slengths)))

def reverse_accumulate(d):
    """Given a dict *d* of (length,count) items, return an accumulate dictionary
    of (length,acc) items where for each length the associated *acc* is the sum
    of the counts for that length and all larger lengths.
    """

    r = {}
    a = 0
    for l,c in reversed(d.items()):
        a += c
        r[l] = a
    return r

def counts_by_year(ds):
    """Number of records for each year in the database."""

    # Sequence of 2 entry dicts.
    counts = scraperwiki.sqlite.select("year,count(year) from %s.swdata where element = 'tmeanM' group by year" % ds)
    # We need to avoid entries where year is not an integer.
    return dict((int(d['year']),d['count(year)']) for d in counts if re.match(r'^\d+$', str(d['year'])))

def logbins(d):
    """Bin keys into logarithmic bins.  A numeric key k will be assigned to
    integer bin ceil(ln2(1+k)), where ln2 is the logarithm base 2.
    """
    import math
    def ln2(x): return math.log(x)/math.log(2)
    return dict((int(math.ceil(ln2(1+k))),v) for k,v in d.iteritems())

# Taken from http://code.google.com/p/ccc-gistemp/source/browse/trunk/tool/popchart.py

chartprefix = 'http://chart.apis.google.com/chart'
def popchart(counts, title=None, yaxislabel='year+(CE)'):
    """Return googlechart URL.  *counts* is a sequence of count dicts.
    Each dict maps from year to count of rows for that year.
    """
    minyear = min(min(c) for c in counts)
    maxyear = max(max(c) for c in counts)
    most = max(max(c.values()) for c in counts)
    yscale = reasonable_scale(most)

    # Convert the counts to simple sequences (each sequence starting with
    # *minyear*.
    seqs = [[c.get(y, 0) for y in range(minyear,maxyear+1)]
      for c in counts]

    data = '|'.join(','.join(map(str, l)) for l in seqs)

    chdl=None
    try:
        chdl = '|'.join(inp.name for inp in inps)
    except:
        pass

    d = dict(cht='bvg',
      chd='t:'+data,
      chdl=chdl,
      chtt=title,
      chxt='x,y,x',
      chxl='2:|%s' % yaxislabel,
      chxp='2,50',
      chs='440x330',
      chds="1,%d" % yscale,
      chbh='a,0,2',
      chco='cc6611',
      chxr='0,%d,%d,10|1,0,%d' % (minyear,maxyear,yscale),
    )

    for key in ['chdl', 'chtt']:
        if not d[key]:
            del d[key]

    url = chartprefix + '?' + '&'.join(map('='.join, d.items()))
    return url

def reasonable_scale(x):
    """Calculate a limit (for the scale of the y-axis).  The result
    is either 1, 2, or 5 times some power of ten.  And is the smallest
    such number that is >= x.
    """

    x = int(x)
    if x < 2:
        return 1
    if x == 2:
        return 2
    x -= 1
    s = str(x)
    K = 10**(len(s)-1)
    if s < '15':
        # Note 1.5*K is always an integer.
        return int(1.5*K)
    if s < '2':
        return 2*K
    if s < '3':
        return 3*K
    if s < '5':
        return 5*K
    if s < '7':
        return 7*K
    return 10*K

datasource = 'canada-temperature-data'
scraperwiki.sqlite.attach(datasource, 'data')

# Convert from list containing single item dict to value.
n, = scraperwiki.sqlite.select("count(*) from data.swdata;")
n, = n.values()
print "<h1>%s</h1>" % datasource
n_id, = scraperwiki.sqlite.select("count (distinct id) from data.swdata;")
n_id, = n_id.values()
K = 17
nt, = scraperwiki.sqlite.select(
    "count(*) from (select id,element,count(*) as n from swdata where element = 'tmeanM' group by id,element) where n >= %d" %
    K)
nt, = nt.values()
print "<p>%d rows," % n, "%d stations," % n_id, "%d stations with %d years of temperature data.</p>" % (nt, K)

print "<div>"
c = bin_counts_by_station('data')
a = reverse_accumulate(c)
print "<img src='%s' style='float:left' />" % popchart([a,c], title='Station+lengths', yaxislabel='year+count')
d = counts_by_year('data') 
print "<img src='%s' style='float:left' />" % popchart([d], title='Station+count')
print "</div>"

print "<div>"
"""
scraperwiki.sqlite.attach('can-weather-stations-aux', 'aux')
ms = scraperwiki.sqlite.select("missing_months,count(*) from aux.swdata group by missing_months")
md = dict((m['missing_months'],m['count(*)']) for m in ms)
# Sometimes (I think when new stations are scraped), missing_months is None.
# So they appear here associated with the key None.
if None in md:
    print "<p>", md[None], "stations with unknown missing months.</p>"
del md[None]
md = logbins(md)
print "<img src='%s' style='float:left' />" % popchart([md], title="Missing+Months", yaxislabel='log2(1%2Bmonth+count)')
"""
print "</div>"# canada-temperature-summary
# Summary of the data held in the canada-temperature-data scraper
# David Jones, 2011-08-31, Climate Code Foundation

import scraperwiki

import itertools
import re

def bin_counts_by_station(ds):
    """For each station in the database *ds*, count the number of records (*l*).
    Return a dict of (*l*,*count*) pairs.
    """

    # Sequence of one entry dicts, denoting the length of each station
    lengths = scraperwiki.sqlite.select("count(*) from %s.swdata where element = 'tmeanM' group by id" % ds)
    # The same, as a simple sorted list of lengths
    slengths = sorted(d.values()[0] for d in lengths)
    # Use itertools groupby to convert to dict of (length, count) pairs.
    return dict(((l,len(list(seq))) for l,seq in itertools.groupby(slengths)))

def reverse_accumulate(d):
    """Given a dict *d* of (length,count) items, return an accumulate dictionary
    of (length,acc) items where for each length the associated *acc* is the sum
    of the counts for that length and all larger lengths.
    """

    r = {}
    a = 0
    for l,c in reversed(d.items()):
        a += c
        r[l] = a
    return r

def counts_by_year(ds):
    """Number of records for each year in the database."""

    # Sequence of 2 entry dicts.
    counts = scraperwiki.sqlite.select("year,count(year) from %s.swdata where element = 'tmeanM' group by year" % ds)
    # We need to avoid entries where year is not an integer.
    return dict((int(d['year']),d['count(year)']) for d in counts if re.match(r'^\d+$', str(d['year'])))

def logbins(d):
    """Bin keys into logarithmic bins.  A numeric key k will be assigned to
    integer bin ceil(ln2(1+k)), where ln2 is the logarithm base 2.
    """
    import math
    def ln2(x): return math.log(x)/math.log(2)
    return dict((int(math.ceil(ln2(1+k))),v) for k,v in d.iteritems())

# Taken from http://code.google.com/p/ccc-gistemp/source/browse/trunk/tool/popchart.py

chartprefix = 'http://chart.apis.google.com/chart'
def popchart(counts, title=None, yaxislabel='year+(CE)'):
    """Return googlechart URL.  *counts* is a sequence of count dicts.
    Each dict maps from year to count of rows for that year.
    """
    minyear = min(min(c) for c in counts)
    maxyear = max(max(c) for c in counts)
    most = max(max(c.values()) for c in counts)
    yscale = reasonable_scale(most)

    # Convert the counts to simple sequences (each sequence starting with
    # *minyear*.
    seqs = [[c.get(y, 0) for y in range(minyear,maxyear+1)]
      for c in counts]

    data = '|'.join(','.join(map(str, l)) for l in seqs)

    chdl=None
    try:
        chdl = '|'.join(inp.name for inp in inps)
    except:
        pass

    d = dict(cht='bvg',
      chd='t:'+data,
      chdl=chdl,
      chtt=title,
      chxt='x,y,x',
      chxl='2:|%s' % yaxislabel,
      chxp='2,50',
      chs='440x330',
      chds="1,%d" % yscale,
      chbh='a,0,2',
      chco='cc6611',
      chxr='0,%d,%d,10|1,0,%d' % (minyear,maxyear,yscale),
    )

    for key in ['chdl', 'chtt']:
        if not d[key]:
            del d[key]

    url = chartprefix + '?' + '&'.join(map('='.join, d.items()))
    return url

def reasonable_scale(x):
    """Calculate a limit (for the scale of the y-axis).  The result
    is either 1, 2, or 5 times some power of ten.  And is the smallest
    such number that is >= x.
    """

    x = int(x)
    if x < 2:
        return 1
    if x == 2:
        return 2
    x -= 1
    s = str(x)
    K = 10**(len(s)-1)
    if s < '15':
        # Note 1.5*K is always an integer.
        return int(1.5*K)
    if s < '2':
        return 2*K
    if s < '3':
        return 3*K
    if s < '5':
        return 5*K
    if s < '7':
        return 7*K
    return 10*K

datasource = 'canada-temperature-data'
scraperwiki.sqlite.attach(datasource, 'data')

# Convert from list containing single item dict to value.
n, = scraperwiki.sqlite.select("count(*) from data.swdata;")
n, = n.values()
print "<h1>%s</h1>" % datasource
n_id, = scraperwiki.sqlite.select("count (distinct id) from data.swdata;")
n_id, = n_id.values()
K = 17
nt, = scraperwiki.sqlite.select(
    "count(*) from (select id,element,count(*) as n from swdata where element = 'tmeanM' group by id,element) where n >= %d" %
    K)
nt, = nt.values()
print "<p>%d rows," % n, "%d stations," % n_id, "%d stations with %d years of temperature data.</p>" % (nt, K)

print "<div>"
c = bin_counts_by_station('data')
a = reverse_accumulate(c)
print "<img src='%s' style='float:left' />" % popchart([a,c], title='Station+lengths', yaxislabel='year+count')
d = counts_by_year('data') 
print "<img src='%s' style='float:left' />" % popchart([d], title='Station+count')
print "</div>"

print "<div>"
"""
scraperwiki.sqlite.attach('can-weather-stations-aux', 'aux')
ms = scraperwiki.sqlite.select("missing_months,count(*) from aux.swdata group by missing_months")
md = dict((m['missing_months'],m['count(*)']) for m in ms)
# Sometimes (I think when new stations are scraped), missing_months is None.
# So they appear here associated with the key None.
if None in md:
    print "<p>", md[None], "stations with unknown missing months.</p>"
del md[None]
md = logbins(md)
print "<img src='%s' style='float:left' />" % popchart([md], title="Missing+Months", yaxislabel='log2(1%2Bmonth+count)')
"""
print "</div>"