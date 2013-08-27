import scraperwiki

#print scraperwiki.scrape('http://10.0.0.1:9004/Status'),

# simple datastore save
print scraperwiki.sqlite.save(unique_keys=['country'], data={'country':'uk'})

# these should work
# HTTP
print scraperwiki.scrape('http://www.flourish.org'),
# HTTPS
print scraperwiki.scrape('https://www.scraperwiki.com/'),

print scraperwiki.scrape("ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/Jan/N_01_area.txt"),

# this/these should hang and not work
# Status ports
print scraperwiki.scrape('http://10.0.0.1:9001/Status'),
print scraperwiki.scrape('http://88.211.55.91:9001/Status'),import scraperwiki

#print scraperwiki.scrape('http://10.0.0.1:9004/Status'),

# simple datastore save
print scraperwiki.sqlite.save(unique_keys=['country'], data={'country':'uk'})

# these should work
# HTTP
print scraperwiki.scrape('http://www.flourish.org'),
# HTTPS
print scraperwiki.scrape('https://www.scraperwiki.com/'),

print scraperwiki.scrape("ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/Jan/N_01_area.txt"),

# this/these should hang and not work
# Status ports
print scraperwiki.scrape('http://10.0.0.1:9001/Status'),
print scraperwiki.scrape('http://88.211.55.91:9001/Status'),import scraperwiki

#print scraperwiki.scrape('http://10.0.0.1:9004/Status'),

# simple datastore save
print scraperwiki.sqlite.save(unique_keys=['country'], data={'country':'uk'})

# these should work
# HTTP
print scraperwiki.scrape('http://www.flourish.org'),
# HTTPS
print scraperwiki.scrape('https://www.scraperwiki.com/'),

print scraperwiki.scrape("ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/Jan/N_01_area.txt"),

# this/these should hang and not work
# Status ports
print scraperwiki.scrape('http://10.0.0.1:9001/Status'),
print scraperwiki.scrape('http://88.211.55.91:9001/Status'),