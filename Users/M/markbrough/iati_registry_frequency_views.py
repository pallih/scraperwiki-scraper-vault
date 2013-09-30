import scraperwiki
import json
import cgi, os 
from functools import wraps
scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", ""))) 

def provide_data():
    if 'packagegroup_name' in paramdict:
        packagegroup_name = paramdict['packagegroup_name']
    else:
        content = str(json.dumps({"error":"no packagegroup_name provided"}))
        print return_content(content)
        exit()
    
    sourcescraper = 'iati_registry_updater_frequency_check'
    scraperwiki.sqlite.attach("iati_registry_updater_frequency_check", "src") 
    
    data = scraperwiki.sqlite.select("year, month from src.packagegroups_dates_data where packagegroup_name = '"+packagegroup_name+"' and year='2013'")
    if not data:
        content = str(json.dumps({error:"no data for that packagegroup_name"}))
        print return_content(content)
        exit()
    
    months = 0
    for d in data:
        months +=1
    if months>2:
        timeliness="monthly"
    elif months>0:
        timeliness="quarterly"
    else:
        timeliness="less than quarterly"
    
    content = str(json.dumps({"data": data, "timeliness":timeliness}))
    print return_content(content)

def return_content(content):
    if 'callback' in paramdict:
        content = str(paramdict['callback']) + '(' + content + ')'
    return content

provide_data()
import scraperwiki
import json
import cgi, os 
from functools import wraps
scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", ""))) 

def provide_data():
    if 'packagegroup_name' in paramdict:
        packagegroup_name = paramdict['packagegroup_name']
    else:
        content = str(json.dumps({"error":"no packagegroup_name provided"}))
        print return_content(content)
        exit()
    
    sourcescraper = 'iati_registry_updater_frequency_check'
    scraperwiki.sqlite.attach("iati_registry_updater_frequency_check", "src") 
    
    data = scraperwiki.sqlite.select("year, month from src.packagegroups_dates_data where packagegroup_name = '"+packagegroup_name+"' and year='2013'")
    if not data:
        content = str(json.dumps({error:"no data for that packagegroup_name"}))
        print return_content(content)
        exit()
    
    months = 0
    for d in data:
        months +=1
    if months>2:
        timeliness="monthly"
    elif months>0:
        timeliness="quarterly"
    else:
        timeliness="less than quarterly"
    
    content = str(json.dumps({"data": data, "timeliness":timeliness}))
    print return_content(content)

def return_content(content):
    if 'callback' in paramdict:
        content = str(paramdict['callback']) + '(' + content + ')'
    return content

provide_data()
