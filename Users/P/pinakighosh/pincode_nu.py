import scraperwiki
import lxml.html
url="http://www.eximguru.com/traderesources/pincode.aspx?&GridInfo=Pincode0"
#html=scraperwiki.scrape(url)
#root=lxml.html.fromstring(html)
data=[]
sl_no=1
err=[]
for i in range(10759):
#for i in range(3):
    url1=url+str(i+1+7329)
    print i+1+7329
    print url1
    try:
        html=scraperwiki.scrape(url1)
        root=lxml.html.fromstring(html)
        for i in root.cssselect("table.basicTable tr.sliststyle10"):
            data=[]
            for el in i.cssselect("tr.sliststyle10 td"):
                data.append(el.text_content())
            #print data
            scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"State":data[1],"Place":data[3],"Pincode":data[0]})
            sl_no+=1
        data=[]
        for i in root.cssselect("table.basicTable tr.sliststyle6"):
            for el in i.cssselect("tr.sliststyle6 td"):
                data.append(el.text_content())
            #print data 
            scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"State":data[1],"Place":data[3],"Pincode":data[0]})
            sl_no+=1
            data=[]
    except:
        err.append(url1)
        continue
print url1
                    import scraperwiki
import lxml.html
url="http://www.eximguru.com/traderesources/pincode.aspx?&GridInfo=Pincode0"
#html=scraperwiki.scrape(url)
#root=lxml.html.fromstring(html)
data=[]
sl_no=1
err=[]
for i in range(10759):
#for i in range(3):
    url1=url+str(i+1+7329)
    print i+1+7329
    print url1
    try:
        html=scraperwiki.scrape(url1)
        root=lxml.html.fromstring(html)
        for i in root.cssselect("table.basicTable tr.sliststyle10"):
            data=[]
            for el in i.cssselect("tr.sliststyle10 td"):
                data.append(el.text_content())
            #print data
            scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"State":data[1],"Place":data[3],"Pincode":data[0]})
            sl_no+=1
        data=[]
        for i in root.cssselect("table.basicTable tr.sliststyle6"):
            for el in i.cssselect("tr.sliststyle6 td"):
                data.append(el.text_content())
            #print data 
            scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"State":data[1],"Place":data[3],"Pincode":data[0]})
            sl_no+=1
            data=[]
    except:
        err.append(url1)
        continue
print url1
                    