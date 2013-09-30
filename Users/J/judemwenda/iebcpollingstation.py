import scraperwiki
import csv
import requests
import json

# Blank Python

data = scraperwiki.scrape("https://s3.amazonaws.com/iebc/constituencies_export.csv")
reader = csv.DictReader(data.splitlines())

for row in reader:
    #print "Constituency is %s" % row[2]
    if row['constituen']:
        #print row['constituen']
        payload = {'constituency': row['constituen']}
        headers = {'content-type': 'application/json',"Content-Length": "0",}
        r = requests.get("http://vote.iebc.or.ke/pollingstation/",params=payload)
        const_dict = json.loads(r.content)
        #const_dict =  const_dict['results']
        for item in const_dict['results']:
            #print item
            scraperwiki.sqlite.save(unique_keys=[], data={"county":item['county'],"constituency":row['constituen'],"ward":item['ward'],"name":item['name'],"latitude":item['point']['lat'],"longitude":item['point']['lon']},table_name="iebcpollingstations", verbose=2)

    

import scraperwiki
import csv
import requests
import json

# Blank Python

data = scraperwiki.scrape("https://s3.amazonaws.com/iebc/constituencies_export.csv")
reader = csv.DictReader(data.splitlines())

for row in reader:
    #print "Constituency is %s" % row[2]
    if row['constituen']:
        #print row['constituen']
        payload = {'constituency': row['constituen']}
        headers = {'content-type': 'application/json',"Content-Length": "0",}
        r = requests.get("http://vote.iebc.or.ke/pollingstation/",params=payload)
        const_dict = json.loads(r.content)
        #const_dict =  const_dict['results']
        for item in const_dict['results']:
            #print item
            scraperwiki.sqlite.save(unique_keys=[], data={"county":item['county'],"constituency":row['constituen'],"ward":item['ward'],"name":item['name'],"latitude":item['point']['lat'],"longitude":item['point']['lon']},table_name="iebcpollingstations", verbose=2)

    

