import scraperwiki
import lxml.html
import time  

mylist = []
count = scraperwiki.sqlite.get_var("offset", 0)

scraperwiki.sqlite.attach("test123_4", "src")           
data = scraperwiki.sqlite.execute("select * from src.swdata limit 10000 offset "+str(count))    

print "Starting with offset: " + str(count)
print "Keys: " + str(data['keys'])
try:
    for row in data['data']:
        html = scraperwiki.scrape(row[0])
        root = lxml.html.fromstring(html)
        
        mydata = dict()
        mydata['panel_url'] = row[0]
    
        try:
            mydata['DeltaIsc'] = root.cssselect("span#ctl00_ctl00_cph1_MainContent_TabContainer1_TabSpecifications_PanelInfo1_DeltaIsc")[0].text
        except:
            mydata['DeltaIsc'] = 0
    
        try:
            mydata['DeltaVoc'] = root.cssselect("span#ctl00_ctl00_cph1_MainContent_TabContainer1_TabSpecifications_PanelInfo1_DeltaVoc")[0].text
        except:
            mydata['DeltaVoc'] = 0

        try:
            mydata['DeltaPmax'] = root.cssselect("span#ctl00_ctl00_cph1_MainContent_TabContainer1_TabSpecifications_PanelInfo1_DeltaPmax")[0].text
        except:
            mydata['DeltaPmax'] = 0
    
        mylist.append(mydata)
        count+=1
        time.sleep(0.5)
    scraperwiki.sqlite.save_var("offset", count)
    scraperwiki.sqlite.save(unique_keys=['panel_url'], data=mylist)
    scraperwiki.sqlite.commit()
    print " Normal Stopping with offset: " + str(count)
except Exception as e: 
    scraperwiki.sqlite.save_var("offset", count)
    scraperwiki.sqlite.save(unique_keys=['panel_url'], data=mylist)
    scraperwiki.sqlite.commit()
    print "Exception Stopping with offset: " + str(count)
    print "Unexpected error:" , str(e)
