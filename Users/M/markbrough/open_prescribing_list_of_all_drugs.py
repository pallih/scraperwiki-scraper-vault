import scraperwiki
import urllib2
import json

# Blank Python

DRUGS_URL = "http://www.openprescribing.org/api/v1/product/?api_key=special-key&format=json&limit=1000&offset=%s"

def get_drugs():
    offset = 0
    keepgoing = True
    while keepgoing:
        drugs_list_req = urllib2.Request(DRUGS_URL % (offset))
        drugs_list_webfile = urllib2.urlopen(drugs_list_req)
        drugs_list = json.loads(drugs_list_webfile.read())
    
        
        if (("objects" in drugs_list) and (drugs_list["objects"])):
        
            for drug in drugs_list["objects"]:
                scraperwiki.sqlite.save(unique_keys=["bnf_code"],
                        data=drug,
                        table_name="drugs")
            offset +=1000
        else:
            keepgoing = False

get_drugs()
