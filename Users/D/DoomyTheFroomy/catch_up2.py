from BeautifulSoup import BeautifulSoup
from collections import deque
import scraperwiki
import urllib
import re
import simplejson
import urllib2

# Blank Python
# http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3F%26sortby%3D19%26marketingtype%3D-1%26county%3D1019%26suchart%3D1%26objecttype%3D1%26parentcat%3D1%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3Dabc72mySUdA7vg3MS0lKt1390bdcde8e%26ext%3D.xml%22)%20&format=json&diagnostics=true&callback=

# "http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3F%26sortby%3D19%26marketingtype%3D-1%26county%3D1019%26suchart%3D1%26objecttype%3D1%26parentcat%3D1%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3Dabc72mySUdA7vg3MS0lKt1390bdcde8e%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'%20limit%20100&format=json&diagnostics=true"



###########################################
### Brandenburg ###########################
###########################################
########### Barnim ########################
queue_berlin = deque(["http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3F%26sortby%3D19%26marketingtype%3D-1%26county%3D1019%26suchart%3D1%26objecttype%3D1%26parentcat%3D1%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3Dabc72mySUdA7vg3MS0lKt1390bdcde8e%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'%20limit%20100&format=json&diagnostics=true"])
for queue_res in queue_berlin:
    catch_json = queue_res 
    try:
        results_json = simplejson.loads(scraperwiki.scrape(catch_json))
    
        query = results_json['query']
        
        results_query = query['results']
        # print results_query['div']
        for result_div in results_query['div']:
            # print result_div
            try:
                result_p = result_div['p']
                result_a = result_p['content']
                print result_a
                scraperwiki.sqlite.save(unique_keys=["id"], data={ "id":result_a, "Link": catch_json })
            except:
                print 'no address'
    
    except:
        print 'no result'









