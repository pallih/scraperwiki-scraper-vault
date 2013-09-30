# Blank Python
# Python
import urllib2
import json
import scraperwiki

fp = urllib2.urlopen('http://catalogue.data.gov.uk/api/1/rest/package')
results = json.loads(fp.read())
fp.close()

for package in results:
    print package

    record = { "package" : package} # column name and value
    scraperwiki.datastore.save(["package"], record) # save the records one by one# Blank Python
# Python
import urllib2
import json
import scraperwiki

fp = urllib2.urlopen('http://catalogue.data.gov.uk/api/1/rest/package')
results = json.loads(fp.read())
fp.close()

for package in results:
    print package

    record = { "package" : package} # column name and value
    scraperwiki.datastore.save(["package"], record) # save the records one by one