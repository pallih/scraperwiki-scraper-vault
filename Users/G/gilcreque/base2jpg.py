sourcescraper = 'brevard_county_sheriff_inmate_photos_2'

import base64
import scraperwiki
import re


#needed for accessing query strings
import cgi
import os

query = os.getenv("QUERY_STRING")
breakout = re.split("[-.]", query)
id = breakout[0]
photo = breakout[1]

data = scraperwiki.sqlite.select(           
    '''photo'''+photo+'''_blob from brevard_county_sheriff_inmate_photos_2.swdata where id = '''+id+''' limit 1'''
)


ScraperWiki.httpresponseheader(Content-Type, image/png)

g = open(query, "w")
g.write(base64.decodestring(data))
g.close()
