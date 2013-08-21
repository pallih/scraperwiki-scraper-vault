import scraperwiki

import urllib
import re
import json
import collections

i=99 ## set up a loop to run through all potential json calls
#only used to make unique channel id's
recordnum=0
while i>0:
    url="http://api.bell.ca/en/channels/"+str(i)+"/group.json" ## go through each json call
    htmltext=urllib.urlopen(url) ##open the page
    data=json.load(htmltext) ## json load the page
    
    if 'gname' in data and 'channels' in data: #only scrape if there is channel info, add in province filter

        package_name=data['gname']
        package_price=data['price']
        province=data['province']
        for item in data['channels']:
            if province != 'qc':
                recordnum+=1 #only used to make unique channel id's
                record = {"id":recordnum, "channel_name" : item['name'],"package" : package_name, "price" : package_price, "alc_price" : item['price_alacarte'], 
                "combo_addon_price" : item['price_combo_addon'], "channel_desc" : item['desc'], "province" : province} # column name and value
                scraperwiki.sqlite.save(["id"],record) # save the records one by one
                print i
            else:
                print "QC"

        ##for s in data['sets']:
        ##    extrasets = {"set_name" : s['sname'], "set_price_combo_addon" : s['price_combo_addon']}
        ##    record.update(extrasets)
            
        ##need to add set names and set prices, then join back to channel using datastore
        ## or perhaps "add to record" before saving to datastore
        
        i-=1 ## move on to next page
    
    else:
        print i,'no go'
        i-=1


