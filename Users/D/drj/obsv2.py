# Obs.v2
# David Jones, Climate Code Foundation, 2011-09-27
# Produce bulk (climate data) observations in GHCN V2 format.
# Which is obsolescent.

import scraperwiki

import cgi
import itertools
import json
import os
import sys
import urllib

scraperwiki.utils.httpresponseheader('Content-Type', 'text/plain')

qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

db = qs.get('db', 'canada-temperature-data')
element = qs.get('element', 'tmeanM')
mreq = int(qs.get('mreq', 240))

# With an obs(element,id) index, it's significantly faster to GROUP BY element,id
# than the other way around.
query = """select * from (select id,element,count(*) as n from obs where element='%s' group by element,id) join obs using (id,element)
where n >= %d order by id,year,month""" % (element,mreq)

url = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?" + urllib.urlencode(
    dict(format='jsondict', name=db, query=query))

def toid12(x):
    """Convert to a 12 character ID, by padding on right with spaces,
    then converting all spaces to 'V'."""

    return ("%-12.12s" % x).replace(' ', 'V')

rowfmt = "%s%04d" + 12*"%s" + "\n"
def JSONtoGHCNV2(j, out=sys.stdout):
    """Convert to GHCN format."""
    # Recall that GHCN format has one row per year.
    for (id,year),items in itertools.groupby(j, lambda s: (s['id'],s['year'])):
        id12 = toid12(id)
        # Because missing months are not recorded in the database;
        # *items* may not have 12 months represented.  We initialise
        # *row* to contain dummy values.
        row = ["-9999"] * 12
        for item in items:
            flag = item['f']
            # On flags.  By inspecting a few values, it seems that 'E'
            # is used when there are only a few days missing from the
            # month, and 'I' is used when there are many days missing
            # from the month.  In keeping with the WMO "10 missing day"
            # tradition, we retain the 'E' flagged values.
            # We could probably exclude/include flagged data at the query
            # stage.
            if flag not in ('', 'E'):
                continue
            # Note: "%5.0f" rounds to nearest integer and formats in a
            # 5 character field.
            row[item['month']-1] = "%5.0f" % (10*float(item['v']))
        if row != ["-9999"]*12:
            out.write(rowfmt % ((id12, year) + tuple(row)))

print query
print url
j = json.load(urllib.urlopen(url))
print len(j)
JSONtoGHCNV2(j)
