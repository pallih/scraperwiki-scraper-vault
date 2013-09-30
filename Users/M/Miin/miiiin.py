import scraperwiki
import lxml.html
import string
import re

# This returns a list of the letters A-Z
letters = list(string.ascii_uppercase)

# Which language we want to scrape (set to 'cn' or 'en')
lang = 'cn'

# What the first part of the URL is
base_url = 'http://www.artlinkart.com'

# The regions/categories under which artists are 
regions = ['beijing', 'shanghai', 'rest_of_china', 'overseas']


for region in regions:

    for letter in letters:

        url = base_url + '/' + lang + '/artist/geographically/' + region + '/' + letter
        print 'Scraping ' + region.capitalize() + ' artists under: ' + letter + '...'

        html = scraperwiki.scrape(url)

        root = lxml.html.fromstring(html)

        for dt in root.cssselect("dl.subnav_artist dt"):
            if(dt[0].tag == 'a'):
                
                artist_url = base_url + dt[0].get('href')
                artist_id = re.search('([^/]+)/?$', artist_url).group(0)
                artist_name = dt[1].text
                print 'Saving artist: ' + artist_name + '...'
                
                scraperwiki.sqlite.save(unique_keys=["artist_id"], data={"artist_id": artist_id, "artist_name_" + lang: artist_name, "region": region, "letter": letter}, table_name='artists')



import scraperwiki
import lxml.html
import string
import re

# This returns a list of the letters A-Z
letters = list(string.ascii_uppercase)

# Which language we want to scrape (set to 'cn' or 'en')
lang = 'cn'

# What the first part of the URL is
base_url = 'http://www.artlinkart.com'

# The regions/categories under which artists are 
regions = ['beijing', 'shanghai', 'rest_of_china', 'overseas']


for region in regions:

    for letter in letters:

        url = base_url + '/' + lang + '/artist/geographically/' + region + '/' + letter
        print 'Scraping ' + region.capitalize() + ' artists under: ' + letter + '...'

        html = scraperwiki.scrape(url)

        root = lxml.html.fromstring(html)

        for dt in root.cssselect("dl.subnav_artist dt"):
            if(dt[0].tag == 'a'):
                
                artist_url = base_url + dt[0].get('href')
                artist_id = re.search('([^/]+)/?$', artist_url).group(0)
                artist_name = dt[1].text
                print 'Saving artist: ' + artist_name + '...'
                
                scraperwiki.sqlite.save(unique_keys=["artist_id"], data={"artist_id": artist_id, "artist_name_" + lang: artist_name, "region": region, "letter": letter}, table_name='artists')



