import scraperwiki
import csv
import requests
import json
import re
import lxml.html

# Blank Python

data = scraperwiki.scrape("https://s3.amazonaws.com/kenyaehealth/healthfacilities.csv")
reader = csv.DictReader(data.splitlines())

for row in reader:
    #print "Constituency is %s" % row[2]
    if row['code']:
        print row['code']
        payload = {'fas': row['code']}
        headers = {'content-type': 'application/json',"Content-Length": "0",}
        r = requests.get("http://ehealth.or.ke/facilities/facility.aspx",params=payload)
        root = lxml.html.fromstring(r.content)
        head = root.head
        headstring = lxml.html.tostring(head)
        #print headstring
        #print re.search('\((.*?)\)',headstring).group(2)
        m = re.search('var point = (.+?);', headstring)
        if m:
            latlongstr = m.group(1)
            latlong  = re.search('\((.*?)\)',latlongstr).group(1)
            scraperwiki.sqlite.save(unique_keys=[], data={"code":row['code'],"latlong":latlong,"hospital":row['hospital']},table_name="ehealthnorth", verbose=2)


import scraperwiki
import csv
import requests
import json
import re
import lxml.html

# Blank Python

data = scraperwiki.scrape("https://s3.amazonaws.com/kenyaehealth/healthfacilities.csv")
reader = csv.DictReader(data.splitlines())

for row in reader:
    #print "Constituency is %s" % row[2]
    if row['code']:
        print row['code']
        payload = {'fas': row['code']}
        headers = {'content-type': 'application/json',"Content-Length": "0",}
        r = requests.get("http://ehealth.or.ke/facilities/facility.aspx",params=payload)
        root = lxml.html.fromstring(r.content)
        head = root.head
        headstring = lxml.html.tostring(head)
        #print headstring
        #print re.search('\((.*?)\)',headstring).group(2)
        m = re.search('var point = (.+?);', headstring)
        if m:
            latlongstr = m.group(1)
            latlong  = re.search('\((.*?)\)',latlongstr).group(1)
            scraperwiki.sqlite.save(unique_keys=[], data={"code":row['code'],"latlong":latlong,"hospital":row['hospital']},table_name="ehealthnorth", verbose=2)


