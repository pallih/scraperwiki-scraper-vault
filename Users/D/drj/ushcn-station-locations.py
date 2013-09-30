# USHCN Stations
# 2010-11-02, David Jones, Climate Code Foundation

import urllib

import scraperwiki


if 0: scraperwiki.sqlite.execute("""drop table swdata""")
scraperwiki.sqlite.commit()

# FTP maybe broken (at ScraperWiki?), so replace with HTTP URL.
base = "ftp://ftp.ncdc.noaa.gov/pub/data/ushcn/v2/monthly/"
base = "http://www1.ncdc.noaa.gov/pub/data/ushcn/v2/monthly/"

stationsurl = base + 'ushcn-v2-stations.txt'
ratingsurls = dict((c,base + 'ushcn-nws+surfacestations-ratings-' + c + '.txt')
  for c in ['1-2', '3-4-5'])

# Compile the ratings files into a dict, so that rating[id6] gives
# the rating for that site.
rating = {}
for c,url in ratingsurls.items():
    for row in scraperwiki.scrape(url).split('\n'):
        if not row:
            continue
        id6 = row[:6]
        if id6 in rating:
            print "Ambiguous rating:", id6
            rating[id6] = '?'
        else:
            rating[id6] = c

# The element types found in each row of the stations.txt file,
# expressed as a Python dictionary.
# dict[key] is a triple of (i,j,convert) where the value shall be
# convert(row[i:j]) (that is, i and j specify the columns, and *convert* is
# a function to call).
# (for tedious details, see readme.txt in the above ftp directory).
elements = dict(
  id6 = (0,6,str),
  Latitude = (7,15,float),
  Longitude = (16,25,float),
  Elevation = (26,32,float),
  state = (33,35,str),
  Name = (36,66,str),
  )

def iterstations():
    """Yield each station as a dict of metadata."""
    for i,row in enumerate(scraperwiki.scrape(stationsurl).split('\n')):
        if i%20 == 0:
            print "%4d" % i, row
        if not row:
            continue
        meta = dict((key,convert(row[i:j]))
          for key,(i,j,convert) in elements.items())
        meta['id'] = meta['id6']
        meta['rating'] = rating.get(meta['id6'])
        yield meta

scraperwiki.sqlite.save(['id'], list(iterstations()), table_name='meta')
print "Scraped"# USHCN Stations
# 2010-11-02, David Jones, Climate Code Foundation

import urllib

import scraperwiki


if 0: scraperwiki.sqlite.execute("""drop table swdata""")
scraperwiki.sqlite.commit()

# FTP maybe broken (at ScraperWiki?), so replace with HTTP URL.
base = "ftp://ftp.ncdc.noaa.gov/pub/data/ushcn/v2/monthly/"
base = "http://www1.ncdc.noaa.gov/pub/data/ushcn/v2/monthly/"

stationsurl = base + 'ushcn-v2-stations.txt'
ratingsurls = dict((c,base + 'ushcn-nws+surfacestations-ratings-' + c + '.txt')
  for c in ['1-2', '3-4-5'])

# Compile the ratings files into a dict, so that rating[id6] gives
# the rating for that site.
rating = {}
for c,url in ratingsurls.items():
    for row in scraperwiki.scrape(url).split('\n'):
        if not row:
            continue
        id6 = row[:6]
        if id6 in rating:
            print "Ambiguous rating:", id6
            rating[id6] = '?'
        else:
            rating[id6] = c

# The element types found in each row of the stations.txt file,
# expressed as a Python dictionary.
# dict[key] is a triple of (i,j,convert) where the value shall be
# convert(row[i:j]) (that is, i and j specify the columns, and *convert* is
# a function to call).
# (for tedious details, see readme.txt in the above ftp directory).
elements = dict(
  id6 = (0,6,str),
  Latitude = (7,15,float),
  Longitude = (16,25,float),
  Elevation = (26,32,float),
  state = (33,35,str),
  Name = (36,66,str),
  )

def iterstations():
    """Yield each station as a dict of metadata."""
    for i,row in enumerate(scraperwiki.scrape(stationsurl).split('\n')):
        if i%20 == 0:
            print "%4d" % i, row
        if not row:
            continue
        meta = dict((key,convert(row[i:j]))
          for key,(i,j,convert) in elements.items())
        meta['id'] = meta['id6']
        meta['rating'] = rating.get(meta['id6'])
        yield meta

scraperwiki.sqlite.save(['id'], list(iterstations()), table_name='meta')
print "Scraped"