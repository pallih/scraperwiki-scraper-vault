import scraperwiki

# Blank Python
import simplejson
import urllib
import urllib2

u = "http://dbpedia.org/data/Ceramic_art.json"
#data = urlfetch.fetch(url=u)
json_data = simplejson.loads(urllib.urlopen(u).read())
print json_data[1]
for j in json_data["http://dbpedia.org/resource/Ceramic_art"]:
    if(j == "http://dbpedia.org/ontology/abstract"):
        print 

import scraperwiki

# Blank Python
import simplejson
import urllib
import urllib2

u = "http://dbpedia.org/data/Ceramic_art.json"
#data = urlfetch.fetch(url=u)
json_data = simplejson.loads(urllib.urlopen(u).read())
print json_data[1]
for j in json_data["http://dbpedia.org/resource/Ceramic_art"]:
    if(j == "http://dbpedia.org/ontology/abstract"):
        print 

