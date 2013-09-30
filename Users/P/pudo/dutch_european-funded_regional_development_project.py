from pprint import pprint
from urllib2 import urlopen
from itertools import count
import scraperwiki
import json

URL = "http://www.europaomdehoek.nl/GeoStart/ajax/getItemById.php?id=%s"

def flatten(in_):
    out = {}
    for k, v in in_.items():
        if isinstance(v, dict):
            for ik, iv in v.items():
                out[k + '_' + ik] = flatten(iv) 
        else:
            out[k] = v
    return out

for i in count(270):
    try:
        data = scraperwiki.scrape(URL % i)
        if 'Undefined offset' in data:
            continue
        obj = flatten(json.loads(data))
        scraperwiki.sqlite.save(unique_keys=["id"], data=obj)
    except Exception, e:
        print e
from pprint import pprint
from urllib2 import urlopen
from itertools import count
import scraperwiki
import json

URL = "http://www.europaomdehoek.nl/GeoStart/ajax/getItemById.php?id=%s"

def flatten(in_):
    out = {}
    for k, v in in_.items():
        if isinstance(v, dict):
            for ik, iv in v.items():
                out[k + '_' + ik] = flatten(iv) 
        else:
            out[k] = v
    return out

for i in count(270):
    try:
        data = scraperwiki.scrape(URL % i)
        if 'Undefined offset' in data:
            continue
        obj = flatten(json.loads(data))
        scraperwiki.sqlite.save(unique_keys=["id"], data=obj)
    except Exception, e:
        print e
