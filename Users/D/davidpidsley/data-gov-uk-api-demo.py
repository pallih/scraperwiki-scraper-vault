# Blank Python
import urllib2
import json
import scraperwiki

fp = urllib2.urlopen('http://catalogue.data.gov.uk/api/2/rest/licenses')
results = json.loads(fp.read())
fp.close()

for license in results:
    title = license['title']
    
    record = { "title" : title } # column name and value
    scraperwiki.datastore.save(["title"], record) # save the records one by one# Blank Python
import urllib2
import json
import scraperwiki

fp = urllib2.urlopen('http://catalogue.data.gov.uk/api/2/rest/licenses')
results = json.loads(fp.read())
fp.close()

for license in results:
    title = license['title']
    
    record = { "title" : title } # column name and value
    scraperwiki.datastore.save(["title"], record) # save the records one by one