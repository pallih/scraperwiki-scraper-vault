import scraperwiki
import json

# Blank Python

country="mmr"
base="http://atlas.media.mit.edu/api/export/%s/all/show/1995/"%country

def get_data():
    h=scraperwiki.scrape(base)
    j=json.loads(h)
    return j["data"]

def create_unique(line):
    line["unique"]="%s-%s-%s"%(line["year"],line["abbrv"],line["name"])
    return line


data=map(create_unique, get_data())

for d in data:
    scraperwiki.sqlite.save(unique_keys=["unique"],data=d)
