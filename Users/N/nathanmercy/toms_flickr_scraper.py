import scraperwiki
import simplejson

import scraperwiki
import BeautifulSoup
import datetime
# Blank Python


#get api key from env variables
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    apikey=qsenv["OC_KEY"]
except:
    ockey=''

search_term='me'
page='1'
per_page ='500'

base_url='http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key='

#query api with this custom url
full_query=base_url+apikey+'&tags='+search_term+'&page='+page+'&per_page='+per_page

xml = scraperwiki.scrape(full_query)

#make an xml tree with beautiful soup
soup = BeautifulSoup.BeautifulSoup(xml)

#for each entry
for photo in soup.findAll('photo'):
    #get the stuff we need to construct a url as described here http://www.flickr.com/services/api/misc.urls.html
    print photo
    farm_id = photo['farm']
    server_id= photo['server']
    photo_id = photo['id']
    secret = photo['secret']
    size='m'
    link_url ='http://farm'+farm_id+'.staticflickr.com/'+server_id+'/'+photo_id+'_'+secret+'_'+size+'.jpg'
    scraperwiki.sqlite.save(unique_keys=["a"], data={"a":link_url})