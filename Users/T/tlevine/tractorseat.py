"Import a CouchDB"
from urllib2 import urlopen
from json import loads
from scraperwiki.sqlite import save

def get(uniques=[],couchdburl=None,table_name="swdata"):
  if couchdburl==None:
    d=None
  else:
    url="%s/_all_docs?include_docs=true" % couchdburl
    d=[doc['doc'] for doc in loads(urlopen(url).read())['rows']]
    uniques.append("_id")
  save(uniques,d,table_name)

#Test/example
#get([],'http://chainsaw.iriscouch.com/postbank/','postbanks')"Import a CouchDB"
from urllib2 import urlopen
from json import loads
from scraperwiki.sqlite import save

def get(uniques=[],couchdburl=None,table_name="swdata"):
  if couchdburl==None:
    d=None
  else:
    url="%s/_all_docs?include_docs=true" % couchdburl
    d=[doc['doc'] for doc in loads(urlopen(url).read())['rows']]
    uniques.append("_id")
  save(uniques,d,table_name)

#Test/example
#get([],'http://chainsaw.iriscouch.com/postbank/','postbanks')