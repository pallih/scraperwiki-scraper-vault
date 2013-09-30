import scraperwiki
import lxml.html
import simplejson
import demjson
import re
import yaml
# Blank Python

#scraperwiki.sqlite.execute('delete from `data`')
json_raw = scraperwiki.scrape("http://dl.dropbox.com/u/14865435/t1.txt")
json_raw = json_raw.decode('utf-8')
#json_raw = re.sub(r'({|,)([\w\d_]+?):', r'\1"\2":', json_raw)
#print json_raw
#json = simplejson.loads(json_raw, strict=False)
json = demjson.decode(json_raw, encoding='utf-8')
#print json
i=1
for j in json:
    k = json[j]
    scraperwiki.sqlite.save(unique_keys=['id'], 
        data={'id':i, \
            'name':k['name'],\
            'address':k['address'],\
            'type_id':k['typeId'],\
            'typeName':k['typeName'],\
            'lat':k['lat'],\
            'lng':k['lng'],\
            'internal_id':k['id']}, \
        table_name='data')
    i+=1

import scraperwiki
import lxml.html
import simplejson
import demjson
import re
import yaml
# Blank Python

#scraperwiki.sqlite.execute('delete from `data`')
json_raw = scraperwiki.scrape("http://dl.dropbox.com/u/14865435/t1.txt")
json_raw = json_raw.decode('utf-8')
#json_raw = re.sub(r'({|,)([\w\d_]+?):', r'\1"\2":', json_raw)
#print json_raw
#json = simplejson.loads(json_raw, strict=False)
json = demjson.decode(json_raw, encoding='utf-8')
#print json
i=1
for j in json:
    k = json[j]
    scraperwiki.sqlite.save(unique_keys=['id'], 
        data={'id':i, \
            'name':k['name'],\
            'address':k['address'],\
            'type_id':k['typeId'],\
            'typeName':k['typeName'],\
            'lat':k['lat'],\
            'lng':k['lng'],\
            'internal_id':k['id']}, \
        table_name='data')
    i+=1

