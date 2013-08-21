import scraperwiki
import lxml.html
idx = 0

def writedata(ids, valuekey):
    data = {'id':ids,'key':valuekey[0], 'value':valuekey[1]}
    scraperwiki.sqlite.save(unique_keys=['id'], data=data) 


html = scraperwiki.scrape("http://wiki.openstreetmap.org/wiki/Map_Features")
root = lxml.html.fromstring(html) 

tables = root.cssselect("table")
for i in range(1,len(tables)):
    trs = tables[i].cssselect("tr")
    for tr in trs:
        tds = tr.cssselect("td")
        if len(tds) > 0:
            k = tds[0].text_content().strip()
            v = tds[1].text_content().strip()
            if (v.find(",") >-1):
                vv = v.split(",")
                if type(vv[0]) == int:
                    for i in vv:
                        d = (k,str(vv[i]).strip())
                        writedata(idx,d)
                        idx +=1
            elif (v.find("0-") > -1):
                vv = v.split("0-")
                for i in range(0,int(vv[1])):
                    d = (k,str(i))
                    writedata(idx,d)
                    idx +=1
            elif (v.find(" to ") > -1):
                vv = v.split(" to ")
                if type(vv[0]) == int:
                    for i in range(vv[0],vv[1]):
                        d = (k,i)
                        writedata(idx,d)
                        idx +=1
            elif (v.find("/") > -1):
                vv = v.split("/")
                for i in vv:
                    if type(i) == int:
                        d = (k,i)
                    else:
                        d = (k,i.encode('utf-8').strip())
                    writedata(idx,d)
                    idx +=1
            else:
                d = (k,v.strip())
                writedata(idx,d)
                idx +=1




    
