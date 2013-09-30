import scraperwiki
from BeautifulSoup import BeautifulSoup
data=scraperwiki.scrape("http://posterous.com/getfile/files.posterous.com/james-nsqsp/BeVzgbhkyHrgQ99UMUNCclRzHy0WJwqdo8RIKtHELSF92T8ysWao6HnBMjgM/aggregates.csv")

for row, l in enumerate(data.splitlines()):
    parts=l.split(",")
    if len(parts)!=7: continue
    if row==0:
        keys=parts
    else:
        data={}
        for n, key in enumerate(keys):
            v=parts[n]
            if n!=0:
                v=int(v)
            data[key]=v
        scraperwiki.datastore.save(["CODE"], data) 

import scraperwiki
from BeautifulSoup import BeautifulSoup
data=scraperwiki.scrape("http://posterous.com/getfile/files.posterous.com/james-nsqsp/BeVzgbhkyHrgQ99UMUNCclRzHy0WJwqdo8RIKtHELSF92T8ysWao6HnBMjgM/aggregates.csv")

for row, l in enumerate(data.splitlines()):
    parts=l.split(",")
    if len(parts)!=7: continue
    if row==0:
        keys=parts
    else:
        data={}
        for n, key in enumerate(keys):
            v=parts[n]
            if n!=0:
                v=int(v)
            data[key]=v
        scraperwiki.datastore.save(["CODE"], data) 

