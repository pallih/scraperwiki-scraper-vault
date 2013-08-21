import sys, time, os
from mechanize import Browser
import scraperwiki
import urlparse
import lxml.html



br = Browser()
br.set_handle_robots(False)

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
i = 0
global_list =[]

for num in range(1,3):
    br.open("http://www.harrynorman.com/AgentResult.aspx?RecordType=3&0605=1&0040=1&0535=&AgoraPage={0}&AgoraItems=48&0520_order=ascending".format(num))
    
    
    nice_links = [l for l in br.links()
        if 'harrynorman' in l.url]
    #global_list = global_list + nice_links
    global_list.extend(nice_links)


    record = {}
   
    for link in nice_links:
        #print link.url
        i=i+1
        record['id'] = i
        record['url'] = link.url
        scraperwiki.sqlite.save(["id"], record)
    
print scraperwiki.sqlite.show_tables()
#print scraperwiki.sqlite.execute("select * from swdata")

#for globallink in global_list:
    #print globallink.url