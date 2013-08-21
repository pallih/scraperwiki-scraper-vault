import scraperwiki
import lxml.html
import os
import urllib
import base64

html = scraperwiki.scrape("http://www.brevardsheriff.com/dar/inmatephotos/index.html")
content = lxml.html.etree.HTML(html)
inmates = content.xpath("//a")

for inmate in inmates:           
    id = os.path.splitext(inmate.attrib['href'])[0]
    name = inmate.text
    photo1 = base64.b64encode(urllib.urlopen("http://www.brevardsheriff.com/dar/inmatephotos/Images/"+id+"-1.jpg").read())
    photo2 = base64.b64encode(urllib.urlopen("http://www.brevardsheriff.com/dar/inmatephotos/Images/"+id+"-2.jpg").read())
    reporturl = "http://www.brevardsheriff.com/dar/inmatephotos/"+id+".html"
    
    try:
        reporthtml = scraperwiki.scrape(reporturl)
    except :
        continue

    reportcontent = lxml.html.etree.HTML(reporthtml)
    #rgdob = reportcontent.xpath("/table[5]//td/center/center/text()")
    #arrdate = reportcontent.xpath("/table[5]//td/center/center/center/text()")
    #print arrdate

    scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id, "name":name, "photo1_blob":photo1, "photo2_blob":photo2, "report":reportcontent})