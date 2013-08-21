import scraperwiki
import json
import datetime

purge = scraperwiki.scrape("http://graph.facebook.com/237878386325008")

websiteData = json.loads(purge)

"""
print websiteData
print type(websiteData)
print websiteData['username']
"""

def storeData(websiteData):
    lastNum = 0

    try:
        scraperwiki.sqlite.execute("""\
            create table storage (id INTEGER PRIMARY KEY AUTOINCREMENT)""")
    except:
        print "Table already exists."
        
    else:
        websiteData['dailyLikes'] = 0

    print lastNum 
    print ' <--Current last number'
    
    websiteData['accessTime'] = datetime.datetime.now()
    del websiteData['id']
    
    
    print 'New Daily Likes:'
    
    
    

    scraperwiki.sqlite.save(unique_keys=[], \
        data = websiteData,\
        table_name='storage')



print __name__

purge = scraperwiki.scrape("http://graph.facebook.com/237878386325008")

dictPurge = json.loads(purge)

storeData(dictPurge)

# Blank Python
