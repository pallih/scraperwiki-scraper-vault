# scrape ESDS catalogue (from public IP)

import lxml.html
import re
import scraperwiki



def esds_scrape(sn):
    url='http://www.esds.ac.uk/findingData/snDescription.asp?sn='+ str(sn)
    root = lxml.html.parse(url).getroot()
    if re.search(' does not exist', lxml.html.tostring(root), flags=re.IGNORECASE):
        # unused or hidden or revoked or... - but metadata unavailable
        thisinfo= {"sn": sn, "available": 0}
        print "unavailable: " + str(sn);
        scraperwiki.sqlite.save(unique_keys=["sn"], data=thisinfo)
        return

    print "parsing: " + str(sn);
    #available

    ps = root.cssselect("p")
    #print "There are %d elements with tag div in this page" % len(ps)
    sn_record= {'sn': sn, "available":1 }
    for p in ps:
        fragment= lxml.html.tostring(p)    
        # strip <p> leading
        # if ^<b>title</b></p>
        #print fragment
        for m in re.finditer('<b>(.*?)</b>(.+?)<br/?>', fragment):
            key=re.sub('[^a-zA-Z0-9]','', m.group(1))
            key= key.lower()
            if re.match('<', key):
                break
            sn_record[key]= m.group(2)
            #print "match group: ", m.group(1) , "and then",  sn_record[key]
    scraperwiki.sqlite.save(unique_keys=["sn"], data=sn_record)




# thissn=1234 # 6750 hidden, 1234 ok
min= 1  
lastseen_max_sn= scraperwiki.sqlite.select("max(sn) as m from swdata where title != ''")

for i in lastseen_max_sn[0]: # should only ever be one
    max= lastseen_max_sn[0][i]

for thissn in reversed(range(min, max+100)):
    esds_scrape(thissn)
# scrape ESDS catalogue (from public IP)

import lxml.html
import re
import scraperwiki



def esds_scrape(sn):
    url='http://www.esds.ac.uk/findingData/snDescription.asp?sn='+ str(sn)
    root = lxml.html.parse(url).getroot()
    if re.search(' does not exist', lxml.html.tostring(root), flags=re.IGNORECASE):
        # unused or hidden or revoked or... - but metadata unavailable
        thisinfo= {"sn": sn, "available": 0}
        print "unavailable: " + str(sn);
        scraperwiki.sqlite.save(unique_keys=["sn"], data=thisinfo)
        return

    print "parsing: " + str(sn);
    #available

    ps = root.cssselect("p")
    #print "There are %d elements with tag div in this page" % len(ps)
    sn_record= {'sn': sn, "available":1 }
    for p in ps:
        fragment= lxml.html.tostring(p)    
        # strip <p> leading
        # if ^<b>title</b></p>
        #print fragment
        for m in re.finditer('<b>(.*?)</b>(.+?)<br/?>', fragment):
            key=re.sub('[^a-zA-Z0-9]','', m.group(1))
            key= key.lower()
            if re.match('<', key):
                break
            sn_record[key]= m.group(2)
            #print "match group: ", m.group(1) , "and then",  sn_record[key]
    scraperwiki.sqlite.save(unique_keys=["sn"], data=sn_record)




# thissn=1234 # 6750 hidden, 1234 ok
min= 1  
lastseen_max_sn= scraperwiki.sqlite.select("max(sn) as m from swdata where title != ''")

for i in lastseen_max_sn[0]: # should only ever be one
    max= lastseen_max_sn[0][i]

for thissn in reversed(range(min, max+100)):
    esds_scrape(thissn)
