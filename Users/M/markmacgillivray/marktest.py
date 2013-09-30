import scraperwiki

from urllib import urlopen
import json

data = json.loads(urlopen("http://bibsoup.net/test/pitman.json").read())

print data["records"]

scraperwiki.sqlite.save(unique_keys=["citekey"], data=data["records"]) 
import scraperwiki

from urllib import urlopen
import json

data = json.loads(urlopen("http://bibsoup.net/test/pitman.json").read())

print data["records"]

scraperwiki.sqlite.save(unique_keys=["citekey"], data=data["records"]) 
